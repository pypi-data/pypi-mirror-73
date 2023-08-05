""" Module for automatic updates.





    This module implements utilities used for automatically updating the
    PyInstaller frozen executables. The system, from the point of view of
    the executable, works in the following steps:

    1. Download a JSON file describing the release. The JSON file should represent
    a list of downloadable files, each file being either a full executable script
    for a given platform and release or a bsdiff4 patch from a previous release
    which can be used to reconstruct the full executable for a given platform and release
    given the full executable of the previous release. Each file is represented by
    an element in the list of the following form::

        {
            # Git tag of the release as produced by `git describe --tags`
            "version": "release/v0.9-26-g0e8e006",

            # Url where the release may be downloaded from
            "url":  "https://logic.ff.cuni.cz/nomvallex/releases/vallex-cli-0.9.26-linux64.patch-0.8.0",

            # Download size in bytes
            "size": 99861795,

            # Git tag of the patched version or empty if not a patch
            "delta_from": "release/v0.8",

            # The platform tag (one of `linux64`, `linux32`, `win64`, `win32`, `arm7hf`, `macos`)
            "platform": "linux64"
        }

    2. Find a series of downloads of the least possible files which will allow to reconstruct
    the latest released code from the current version (see :func:`find_path`).

    4. Download each file from this series together with its signature, verify the signature and,
    if applicable, use `bsdiff4.patch`, to reconstruct the current version from these files

    The module also provides utilities to maintain a directory with the releases and with the
    releases.json file. The directory is organized, e.g., as follows::

        releases.json

        vallex-cli-0.1-linux64
        vallex-cli-0.1-linux64.sig
        vallex-cli-0.1-win64.exe
        vallex-cli-0.1-win64.exe.sig

        vallex-cli-0.2-linux64
        vallex-cli-0.2-linux64.sig
        vallex-cli-0.2-win64.exe
        vallex-cli-0.2-win64.exe.sig
        vallex-cli-0.2-linux64.patch-0.1
        vallex-cli-0.2-linux64.patch-0.1.sig
        vallex-cli-0.2-win64.exe.patch-0.1
        vallex-cli-0.2-win64.exe.patch-0.1.sig

        ...

    with the file names having the form

        vallex-cli-``RELEASE_SEMVER``-``PLATFORM``[``PLATFORM SUFFIX``][.patch-``PATCH_BASE_SEMVER``][.sig].

"""

import bisect
import enum
import hashlib
import io
import json
import os
import platform
import stat
import sys
import tempfile
import urllib.request

import bsdiff4  # type: ignore
import nacl.signing  # type: ignore
import nacl.encoding  # type: ignore
import nacl.exceptions  # type: ignore

from collections import defaultdict
from functools import wraps
from pathlib import Path
from typing import Callable, Dict, List, NamedTuple, NewType, Optional, Tuple, TypeVar

from vallex import __version__
from vallex.config import GitVersion, SemVer, SemverComponent, parse_git_description, __semver__

#############################################################################
# Type Aliases
#############################################################################

VerifyKey = TypeVar('VerifyKey')  # nacl.signing.VerifyKey
"""A nacl verify (public) key."""

SignKey = TypeVar('SignKey')  # nacl.signing.SigningKey
"""A nacl sign (private) key."""

HexVerifyKey = NewType('HexVerifyKey', str)
"""A hex-encoded nacl verify (public) key."""

HexSignKey = NewType('HexSignKey', str)
"""A hex-encoded nacl sign (private) key."""

Size = NewType('Size', int)
"""A size-type """

Platform = NewType('Platform', str)
"""A type for storing platform information."""

URL = NewType('URL', str)
"""A type for storing URLs."""

#############################################################################
# Exceptions
#############################################################################


class NoUpdateAvaiable(Exception):
    """
       An exception raised by operations requiring updates
       when there are no updates available.
    """

    def __str__(self):
        return "No Update Available"


class BadSignature(Exception):
    """
       An exception raised when verifying a :mod:`nacl` signature fails.
    """

    def __str__(self):
        return "Bad Signature"


class NetworkError(Exception):
    """
       An exception raised when a network error occurs.
    """

    def __str__(self):
        return "Network Error"

#############################################################################
# Public APIs
#############################################################################


def get_current_platform() -> Platform:
    """
        Determines the current platform and returns the result as a string:
    """
    if sys.platform.startswith('linux'):
        if platform.machine() == 'arm7hf':
            return Platform('arm7hf')
        if platform.architecture()[0] == '64bit':
            return Platform('linux64')
        if platform.architecture()[0] == '32bit':
            return Platform('linux32')
        return Platform('linux')
    if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
        if platform.architecture()[0] == '64bit':
            return Platform('win64')
        if platform.architecture()[0] == '32bit':
            return Platform('win32')
        return Platform('win')
    if sys.platform == 'darwin':
        return Platform('macos')
    return Platform('unknown')


PLATFORM_SUFFIXES = {
    'arm7hf': '',
    'linux64': '',
    'linux32': '',
    'win64': '.exe',
    'win32': '.exe',
    'macos': ''
}
"""Executable file name suffixes on the different platforms"""


def transform_exceptions(method):
    """
        A decorator which wraps `method` into a try-except block,
        catching instances of :class:`nacl.exceptions.BadSignature` or
        :class:`urllib.request.HTTPError` and reraises them as
        :class:`BadSignature` or :class:`NetworkError` respectively.
    """
    @wraps(method)
    def decorated(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except nacl.exceptions.BadSignatureError as ex:
            raise BadSignature(str(ex))
        except urllib.request.HTTPError as ex:
            raise NetworkError(str(ex))
    return decorated


class Updater:
    """
        A helper class for performing application updates.

        Example use::

            from vallex.config import Config, SCRIPT, __version__

            # Load configuration
            config = Config()

            # Create an Updater instance
            updater = Updater(config.release_key, config.release_url, SCRIPT, __version__)

            # Download update meta-data
            updater.check_for_updates()

            # If an update is available
            if updater.available_update():

                # Download the update & verify it
                updater.download_update()

                # Overwrite the current executable
                # with the newly downloaded update
                # and restart it
                updater.apply_update()

    """

    def __init__(self, hex_verify_key: HexVerifyKey, release_url: URL, current_exe: Path, current_version_tag: GitVersion):
        """
            Initialize an Updater instance.

            Parameters
            ----------

                hex_verify_key:         the hex-encoded verify key used to check the integrity of updates
                release_url:            the url pointing to the releases.json file containing update metadata
                current_exe:            the location of the current app executable
                current_version_tag:    the ``git describe --tags`` style version tag of the current app
        """
        self.verify_key = nacl.signing.VerifyKey(hex_verify_key, encoder=nacl.encoding.HexEncoder)
        self.url = release_url
        self.current_version_tag = current_version_tag
        self.current_version = parse_git_description(current_version_tag)
        self.platform = get_current_platform()
        self.releases: Optional[PatchGraph] = None
        self.current_exe = current_exe
        self.update: bytes = b''

    @transform_exceptions
    def download_update(self, progress_cb: Optional[Callable[[float, str], None]] = None):
        """
            Downloads the latest available update.

            If possible, downloads a series of patches and reconstructs the new release from the
            current app executable which minimizes the amount of data to download.

            If the optional `progress_cb` callback is provided, it is called for every 1Kb downloaded
            with the first argument being the fraction of the total download size finished and the second
            argument the name of the file currently being downloaded.

            Raises:
                NoUpdateAvaiable    if there is no update available (e.g. we are up to date)
                BadSignature        if one of the downloaded files failed integrity checks
                NetworkError        if the download fails due to a network error
        """
        if not self.available_update() or not self.releases:
            raise NoUpdateAvaiable
        self.update, _ = reconstruct_release(self.verify_key, self.releases, self.current_exe, self.releases.latest_release()['version'], progress_cb)

    def apply_update(self):
        """
            Applies the update previously downloaded by :meth:`Updater.download_update` and restarts the
            application.

            Raises:
                NoUpdateAvaiable    if no update was downloaded (i.e. the :meth:`Updater.download_update` was ot successfully called before)
        """
        if not self.update:
            raise NoUpdateAvaiable
        backup = self.current_exe.with_name(self.current_exe.name+'.backup.'+str(self.current_version))
        self.current_exe.rename(backup)
        self.current_exe.write_bytes(self.update)
        self.current_exe.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        os.execl(self.current_exe, self.current_exe.name)

    def available_update(self) -> Optional[Tuple[SemVer, Size]]:
        """
            Returns the latest available version strictly greater than the current version and the
            size in bytes which will need to be downloaded in order to reconstruct the latest version.
            If no such version exists, returns None

            If :meth:`Updater.check_for_updates` was not called before, it is called first
            to get the metadata info.
        """
        if not self.releases:
            self.check_for_updates()
        if not self.releases:
            return None
        if self.releases.latest_version() > self.current_version:
            target = self.releases.latest_release()['version']
            _, size = self.releases.find_path(target)
            return self.releases.latest_version(), size
        return None

    @transform_exceptions
    def check_for_updates(self):
        """
            Downloads metadata about available releases from the update server.

            Raises:
                BadSignature        if the downloaded metadata file fails integrity checks
                NetworkError        if the download fails due to a network error
        """
        self.releases = PatchGraph(self.current_version_tag, json.loads(validate_download(self.verify_key, self.url)), self.platform)


class ReleaseChannel:
    """
        A helper class for managing release metadata and patches. For example use
        see :module:`vallex.cli.commands.release`.
    """

    def __init__(self, hex_sign_key: str, base_url: URL, release_dir: Path):
        """
            Initialize a ReleaseChannel instance.

            Parameters
            ----------

                hex_sign_key:         the hex-encoded key used to sign the release files and release metadata
                base_url:             the url where the release files & ``releases.json`` are accessible
                release_dir:          the local directory where the release files & ``releases.json`` are stored
        """
        self.sign_key = nacl.signing.SigningKey(hex_sign_key, encoder=nacl.encoding.HexEncoder)
        self.base_url = base_url
        self.release_dir = release_dir

    @transform_exceptions
    def add_release(self, source: Path, version: GitVersion, platform: Platform):
        """
            Creates a new release whose content is in `source`. The arguments `version`
            and `platform` specify the release version (``git describe --tags`` style)
            and the platform for which the release is, respectively.

            The function creates bsdiff4-style patches to reduce data downloads,
            updates the metadata file ``releases.json`` appropriately and signs everything
            using the signing key.
        """
        add_release(self.sign_key, self.base_url, self.release_dir, source, version, platform)

    @transform_exceptions
    def available_versions(self) -> Dict[Platform, List[Tuple[SemVer, str, Size]]]:
        """
            Provides info about the available releases. The info is provided as a dictionary
            keyed by platform where each platform contains a list of triples ``(VERSION, TYPE, SIZE)``,
            where ``VERSION`` is the semantic version of the release, ``TYPE`` is either ``full``
            in case of a full release or ``patch for PATCHED_VERSION`` if it is a patch based
            on the ``PATCHED_VERSION``, and ``SIZE`` is the size of the download.
        """
        releases = sorted(json.loads(verify_local_file(self.sign_key.verify_key, self.release_dir/'releases.json')), key=lambda x: parse_git_description(x['version']), reverse=True)
        ret: Dict[Platform, List[Tuple[SemVer, str, Size]]] = defaultdict(list)
        for rel in releases:
            ret[rel['platform']].append((parse_git_description(rel['version']), 'full' if not rel['delta_from'] else 'patch for '+str(parse_git_description(rel['delta_from'])), rel['size']))
        return ret

    def cleanup(self) -> List[Tuple[str, SemVer, str, Size]]:
        """
            Removes releases from the json file which do not exist on disk.

            Returns a list of the missing files [a list of tuples (filename, version, full/patch, size)].
        """
        if not (self.release_dir/'releases.json').exists():
            return []

        old_releases = json.loads(verify_local_file(self.sign_key.verify_key, self.release_dir/'releases.json'))  # type: ignore

        # Filter the list of releses so that only those which actually
        # exist on disk are included
        new_releases = []
        missing_releases = []
        for rel in old_releases:
            name = rel['url'].split('/')[-1]
            if (self.release_dir/name).exists():
                new_releases.append(rel)
            else:
                missing_releases.append((name, parse_git_description(rel['version']), 'full' if not rel['delta_from'] else 'patch for '+str(parse_git_description(rel['delta_from'])), rel['size']))

        # Update the ``releases.json`` file
        release_contents = bytes(json.dumps(new_releases), encoding='utf-8')
        sig = sign(self.sign_key, release_contents)
        (self.release_dir/'releases.json').write_bytes(release_contents)
        (self.release_dir/'releases.json.sig').write_text(sig)
        return missing_releases

    @classmethod
    def generate_hex_key_pair(cls) -> Tuple[HexSignKey, HexVerifyKey]:
        """
            A static method to generate a pair of hex-encoded (sign,verify) keys.
        """
        key = nacl.signing.SigningKey.generate()
        return str(key.encode(encoder=nacl.encoding.HexEncoder), encoding='utf-8'), str(key.verify_key.encode(encoder=nacl.encoding.HexEncoder), encoding='utf-8')  # type: ignore


#############################################################################
# Private APIs
#############################################################################

def validate_download(verify_key: VerifyKey, url: URL, progress_cb: Optional[Callable[[int, str], None]] = None) -> bytes:
    """
        Downloads the file from `url` together with its signature which
        should be downloadable from the same url to which ``.sig`` is appended
        and then verifies the signature.

        If the optional `progress_cb` callback is provided, it is called for every 1Kb downloaded
        with the first argument being the number of bytes downloaded and the second argument the
        name of the file being downloaded.

        Returns:
            The downloaded file.

        Raises:
            :class:`nacl.exceptions.BadSignatureError` if the signature could not be verified.
    """
    name = url.split('/')[-1]
    if progress_cb:
        progress_cb(0, name+".sig")
    sig_req = urllib.request.Request(url+'.sig')
    sig = urllib.request.urlopen(sig_req).read()
    sig = nacl.encoding.HexEncoder.decode(sig)

    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req)
    if progress_cb:
        content = io.BytesIO()
        size = 0
        while True:
            buf = r.read(1000)
            if not buf:
                break
            content.write(buf)
            size += len(buf)
            progress_cb(size, name)
        return verify_key.verify(content.getvalue(), sig)  # type: ignore
    return verify_key.verify(r.read(), sig)  # type: ignore


def sign(sign_key: SignKey, data: bytes) -> str:
    """
        Signs `data` using the key `sign_key` and returns the HexEncoded signature.
    """
    sig = sign_key.sign(data)  # type: ignore
    return str(nacl.encoding.HexEncoder.encode(sig.signature), encoding='utf-8')


def verify_local_file(verify_key: VerifyKey, file: Path) -> bytes:
    """
        Reads the file `file` and uses `verify_key` to verify its signature.
        The HexEncoded signature is read from the same path as file with just +'.sig'
        appended.

        Returns:
            The contents of the file.

        Raises:
            :class:`nacl.exceptions.BadSignatureError` if the signature could not be verified.
    """
    sig = nacl.encoding.HexEncoder.decode(file.with_name(file.name+'.sig').read_bytes())
    return verify_key.verify(file.read_bytes(), sig)  # type: ignore


Vertex = NewType('Vertex', str)


class PatchGraph:
    """
        A patch graph corresponding the list of releases. Each vertex corresponds to
        a single release. Each edge from A to B, corresponds to either:

            1. a patch which can be used to reconstruct release B from release A.

            2. an url pointing to the release B (in case there is no patch available
            to reconstruct B from A, one can download the full release, if available)

        Each edge is labeled with the size of the corresponding patch/release,
        the download url and the edge type (:attr:`PATCH <PatchGraph.EdgeType.PATCH>`
        or :attr:`FULL <PatchGraph.EdgeType.FULL>` corresponding to case
        1 or 2 respectively).

        The graph is represented as a dict, indexed by vertices where the value is a
        list of outgoing edges.
    """

    class EdgeType(enum.Enum):
        """The edge type (see :class:`PatchGraph` )"""
        FULL = 'full'
        """Edge represents a full release. """
        PATCH = 'patch'
        """Edge represents a patch. """

    class EdgeData(NamedTuple):
        """Additional data attached to edges (see :class:`PatchGraph`)"""
        url: URL
        type_: 'PatchGraph.EdgeType'

    class Edge(NamedTuple):
        """
            Type representing an outging edge in the patch graph, with
            `vertex` being the target vertex, `size` the size of the
            download and `data` containing additional edge labels.
        """
        vertex: Vertex
        size: Size
        data: 'PatchGraph.EdgeData'

    class NotFound(Exception):
        """
            Exception used to indicate that there is no path allowing to reconstruct
            a target version from a start version.
        """

        def __init__(self, src, target):
            self._target = target
            self._src = src

        def __str__(self):
            return "Cannot reconstruct "+str(self._target)+" from "+str(self._src)

    def __init__(self, current_version: Vertex, releases: List[Dict[str, str]], platform: Platform):
        """
            Constructs a patch graph from a list of releases. The graph will
            additionally contain edges of the :attr:`PatchGraph.EdgeType.FULL`
            from the `current_version` vertex to every full release
            (one can get from the current version to any release which provides
            a full download by just downloading the full release.)
        """
        self._releases = sorted([r for r in releases if r['platform'] == platform], key=lambda x: parse_git_description(GitVersion(x['version'])), reverse=True)
        self.root = current_version
        self.vertices: Dict[Vertex, List[PatchGraph.Edge]] = defaultdict(list)
        for rel in self.releases:
            if not rel['delta_from']:
                self.vertices[self.root].append(
                    self.Edge(
                        vertex=Vertex(rel['version']),
                        size=Size(rel['size']),
                        data=self.EdgeData(url=URL(rel['url']), type_=self.EdgeType.FULL)
                    )
                )
            else:
                self.vertices[rel['delta_from']].append(
                    self.Edge(
                        vertex=Vertex(rel['version']),
                        size=Size(rel['size']),
                        data=self.EdgeData(url=URL(rel['url']), type_=self.EdgeType.PATCH)
                    )
                )

    @property
    def releases(self):
        return self._releases

    def find_path(self, target_version: Vertex, source_version: Optional[Vertex] = None) -> Tuple[List[EdgeData], Size]:
        """
            Uses Dijkstra's algorithm to find a series of files (either patches or full executables)
            with minimum total size which can be used to reconstruct the target version `target_version`
            from a source version `source_version`.
        """
        if source_version is None:
            source_version = self.root
        iso_lines: Dict[Vertex, Tuple[Size, Optional[Vertex], Optional[PatchGraph.EdgeData]]] = {}
        work: List[Tuple[Size, Vertex, Optional[Vertex], Optional[PatchGraph.EdgeData]]] = [(Size(0), source_version, None, None)]
        while work:
            size, vertex, prev, prev_e_data = work.pop(0)
            iso_lines[vertex] = (size, prev, prev_e_data)
            if vertex == target_version:
                break
            for n_vertex, n_size, e_data in self.vertices[vertex]:
                if n_vertex in iso_lines:
                    if iso_lines[n_vertex][0] <= size+n_size:
                        continue
                    iso_lines[n_vertex] = (Size(size+n_size), vertex, e_data)
                else:
                    iso_lines[n_vertex] = (Size(size+n_size), vertex, e_data)
                bisect.insort_left(work, (Size(size+n_size), n_vertex, vertex, e_data))

        if target_version not in iso_lines:
            raise self.NotFound(source_version, target_version)
        path: List[PatchGraph.EdgeData] = []
        current: Optional[Vertex] = target_version
        size = iso_lines[target_version][0]
        while current:
            path = [iso_lines[current][2]] + path  # type: ignore
            current = iso_lines[current][1]
        return path[1:], size

    def latest_release(self, semver_level: SemverComponent = SemverComponent.PATCH):
        """
            Returns the latest release whose semver component `semver_level` is zero.
            By default returns the latest patch release.
        """
        if semver_level == SemverComponent.PATCH:
            return self.releases[0]
        for rel in self.releases:
            semver = parse_git_description(rel['version'])
            if semver[semver_level+1] == 0:
                return rel
        return None

    def latest_version(self, semver_level: SemverComponent = SemverComponent.PATCH) -> SemVer:
        """
            Returns the version of latest release whose semver component `semver_level` is zero.
            By default returns the latest patch release.
        """
        if semver_level == SemverComponent.PATCH:
            return parse_git_description(self.releases[0]['version'])
        for rel in self.releases:
            semver = parse_git_description(rel['version'])
            if semver[semver_level+1] == 0:
                return semver
        return SemVer(0, 0, 0)


def reconstruct_release(verify_key: VerifyKey, patch_graph: PatchGraph, source: Path, target: Vertex, progress_cb: Optional[Callable[[float, str], None]] = None) -> Tuple[bytes, Size]:
    """
        Reconstructs the release version `target` from the current version
        (root version of patch_graph) by finding a series for patches to download,
        downloading them and successively applying them to the current version
        located in `source`.

        If the optional `progress_cb` callback is provided, it is called for every 1Kb downloaded
        with the first argument being the fraction of the total download size finished and the second
        argument the name of the file currently being downloaded.
    """
    path, size = patch_graph.find_path(target)
    ret = source.read_bytes()
    downloaded = Size(0)
    for url, edge_type in path:
        if progress_cb:
            def partial_prog_cb(sz, name): return progress_cb((downloaded+sz)/size, name)
        else:
            partial_prog_cb = None  # type: ignore
        rel = validate_download(verify_key, url, progress_cb=partial_prog_cb)
        downloaded = Size(downloaded + len(rel))
        if edge_type == PatchGraph.EdgeType.PATCH:
            ret = bsdiff4.patch(ret, rel)
        else:
            ret = rel
    return ret, downloaded


def make_signed_release(sign_key: SignKey, path: Path, patch_base: Optional[Path] = None) -> Tuple[bytes, str]:
    """
        Prepares a release from the executable at `path`. This consists of, optionally, creating a patch
        and then signing the executable (or the patch) with the signing key `sign_key`.

        Returns:
            A tuple whose first element is the content of the release (either the patch or the content of `path`)
            and second element is the (hex-encoded) signature.
    """
    if patch_base:
        _, temp_path = tempfile.mkstemp(suffix='.patch')
        patch_path = Path(temp_path)
        bsdiff4.file_diff(patch_base, path, patch_path)
        data = patch_path.read_bytes()
        patch_path.unlink()
    else:
        data = path.read_bytes()
    return data, sign(sign_key, data)


def generate_release_name(base: str, version: SemVer, platform: Platform) -> str:
    """
        Generates a release name from the base name `base`. The format is as follows:

          base-MAJOR.MINOR.PATCH-PLATFORM[.SUFFIX]
    """
    return '-'.join([base, str(version), platform])+PLATFORM_SUFFIXES[platform]


def add_release(sign_key: SignKey, base_url: URL, release_dir: Path, path: Path, version: GitVersion, platform: Platform) -> None:
    """
        Creates a new release from the executable `path` whose git-tag is `version` and platform tag is `platform`. It saves the release
        into the `release_dir` directory, signs it with the hex-encoded key `hex_private_key` and updates the ``releases.json`` file contained
        in that directory with the new release.

        A patch to the previous patch-level release is also created. Additionally, if the release is a minor release, a patch
        to the previous minor release is created. Finally if it is a major release a patch to the previous major release is also created.

        E.g. for version ``1.5.2`` a patch to ``1.5.1`` is created. For version ``1.5`` a patch to, e.g., ``1.4.9`` is created as well as a patch
        to ``1.4``. Finally for version ``2`` patches to (e.g.) ``1.9.12``, ``1.9`` and ``1`` are created.
    """

    # Load the ``releases.json`` file if present
    if (release_dir/'releases.json').exists():
        releases = sorted(json.loads(verify_local_file(sign_key.verify_key, release_dir/'releases.json')), key=lambda x: parse_git_description(x['version']), reverse=True)  # type: ignore
    else:
        releases = []

    # Create the base filename of the new release
    new_semver = parse_git_description(version)
    new_name = generate_release_name(path.name, new_semver, platform)

    # The target_level is the least level we want to generate a
    # patch to
    target_patch_level = new_semver.level

    # patch_level is the level we are currently generating a patch to
    current_patch_level = SemverComponent.PATCH

    # a list of metadata for the generated patches (to add to releases.json)
    patches = []

    # The list of patch_bases available. A patch_base must be a
    # full release (not r['delta_from]). To be eligible, it must,
    # moreover, match the platform and be an earlier release than new_semver
    # TODO: We currently assume that full releases for each patch
    # base are available; we could try to reconstruct them instead
    available = [r for r in releases if
                 r['platform'] == platform and
                 not r['delta_from'] and
                 parse_git_description(r['version']) < new_semver]

    for rel in available:
        ver = parse_git_description(rel['version'])

        # If ver.level < current_patch_level there is no release
        # on the current patch level to generate a patch to
        # (e.g. if v1.0.2 was a successor to v1, then there
        # would be no eligible release (v1.0.1) on the patch and minor
        # patch levels and we would proceed to generating a patch to v1, i.e. on the)
        if ver.level < current_patch_level:
            current_patch_level = ver.level

        # If the candidate release ver is of the relevant patch level
        # generate a patch to it
        if ver.level == current_patch_level:
            name = rel['url'].split('/')[-1]
            if not (release_dir/name).exists():
                continue
            patch, patch_sig = make_signed_release(sign_key, path, patch_base=release_dir/name)
            (release_dir/(new_name+'.patch-'+str(ver))).write_bytes(patch)
            (release_dir/(new_name+'.patch-'+str(ver)+'.sig')).write_text(patch_sig)
            patches.append({
                'url': base_url+'/'+new_name+'.patch-'+str(ver),
                'version': version,
                'platform': platform,
                'delta_from': rel['version'],
                'size': len(patch)
            })
            if current_patch_level <= target_patch_level:
                break
            current_patch_level -= 1  # type: ignore

    releases.extend(patches)

    # Create the full release
    full, full_sig = make_signed_release(sign_key, path)
    (release_dir/new_name).write_bytes(full)
    (release_dir/(new_name+'.sig')).write_text(full_sig)
    releases.append({
        'url': base_url+'/'+new_name,
        'version': version,
        'platform': platform,
        'delta_from': '',
        'size': len(full),
        'sha512': hashlib.sha512(full).hexdigest()
    })

    # Update the ``releases.json`` file
    release_contents = bytes(json.dumps(releases), encoding='utf-8')
    sig = sign(sign_key, release_contents)
    (release_dir/'releases.json').write_bytes(release_contents)
    (release_dir/'releases.json.sig').write_text(sig)
