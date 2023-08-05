import configparser
import datetime
import enum
import logging
import os
import platform
import re
import subprocess
import sys

from pathlib import Path
from typing import List, NamedTuple, NewType, Optional, Union, Tuple

if getattr(sys, 'frozen', False):
    # We are in the packed executable case, and we can't
    # rely on ``__file__``. Instead, we need to get the
    # directory where the python code is unpacked from
    # sys._MEIPASS (set by PyInstaller)
    VALLEX_PACKAGE_PATH = Path(sys._MEIPASS) / 'vallex'  # type: ignore
    FROZEN = True
    SCRIPT_DIR = Path(sys.executable).parent
    SCRIPT = Path(sys.executable)
else:
    VALLEX_PACKAGE_PATH = Path(__file__).parent
    FROZEN = False
    SCRIPT_DIR = VALLEX_PACKAGE_PATH
    SCRIPT = Path(__file__).parent / 'main.py'

GitVersion = NewType('GitVersion', str)
"""A type for storing ``git describe --tags`` style tag."""

try:
    git_hash, git_tag, git_date = (Path(__file__).parent/'__version__').read_text(encoding='utf-8').split('\n')
except:
    git_hash, git_tag, git_date = 'Unknown', 'Unknown', 'Unknown'


class SemVer(NamedTuple):
    """
        A triple representing a `semver <https://semver.org>`_-style version, i.e. ``major.minor.patch``.
    """
    MAJOR: int = 0
    MINOR: int = 0
    PATCH: int = 0

    def __str__(self):
        if not self.PATCH:
            if not self.MINOR:
                return str(self.MAJOR)
            return str(self.MAJOR)+'.'+str(self.MINOR)
        return '.'.join(map(str, self))

    @property
    def level(self):
        """Returns the index of the last non-zero component or zero"""
        if self.PATCH:
            return SemverComponent.PATCH
        if self.MINOR:
            return SemverComponent.MINOR
        return SemverComponent.MAJOR


class SemverComponent(enum.IntEnum):
    """
        The components of a semver triple.
    """
    MAJOR = 0
    MINOR = 1
    PATCH = 2


def parse_git_description(desc: GitVersion) -> SemVer:
    """
        Parses a git tag as produced by ``git describe --tags``. The tag should be of the form::

            release/vMAJOR[.MINOR[-PATCH-GIT_HASH]]

        e.g.::

            release/v0.9-26-g0e8e006

        or::

            release/v0.9

        Returns:
            The semver derived from the tag as a triple (MAJOR, MINOR, PATCH)
    """

    ver = desc[len('release/v'):]
    if desc == 'Unknown':
        major = '-1'
        minor = '0'
        patch = '0'
    elif '-' in ver:
        main, aux = ver.split('-', maxsplit=1)
        major, minor = main.split('.')
        patch = aux.split('-')[0]
    else:
        if '.' in ver:
            major, minor = ver.split('.')
        else:
            major, minor = ver, '0'
        patch = '0'

    return SemVer(MAJOR=int(major), MINOR=int(minor), PATCH=int(patch))


def parse_iso_datetime(dt: str):
    """
        Parse (some flavours of) ISO 8601 formatted strings.
        (See https://stackoverflow.com/a/38085175/2151570)
    """
    if dt.endswith('Z'):
        dt = dt[:-1]+"+0000"
    # this regex removes all colons and all
    # dashes EXCEPT for the dash indicating + or - utc offset for the timezone
    conformed_timestamp = re.sub(r"[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))", '', dt)
    datetime.datetime.strptime(conformed_timestamp, "%Y%m%dT%H%M%S.%f%z")


__appname__ = 'PyVallex'
"""Application name"""
__version__ = GitVersion(git_tag)
"""Git version tag of the code in the package (as shown by `git describe --tags`)"""
__version_info__ = git_hash, GitVersion(git_tag), git_date
"""A triple describing the version of the package in more detail: git hash, git version tag, date of latest commit in git"""
__semver__ = parse_git_description(GitVersion(git_tag))
"""A semver triple (major, minor, patch) obtained from the git tag """

_CONFIG_TEMPLATE = (VALLEX_PACKAGE_PATH/('example-'+__appname__.lower()+'.ini')).read_text(encoding='utf-8')
"""Example config file contents"""

try:
    RELEASE_VERIFY_KEY = (Path(__file__).parent/'release_key.pub').read_text()
    """Public key used to verify release signatures. """
except:
    RELEASE_VERIFY_KEY = None  # type: ignore
    """Public key used to verify release signatures. (Not Found)"""

DEFAULT_RELEASE_LIST = 'https://logic.ff.cuni.cz/nomvallex-beta/_updates/releases.json'
"""URL pointing to a description of available releases for automatic updates """


class Config:
    """
        A class for holding/loading configuration info

    """
    _CFG_NAME = __appname__.lower()+'.ini'

    def _get_option(self, section: str, option: str, default):
        """
            Resolves an option value by coalescing values from
            overrides (provided in the constructor), the config
            object and the provided default value.

            Args:
                section:    the name of the section the option is in
                            (e.g. ``"logging"`` for the ``[logging]`` section)
                option:     the option name
                default:    the default value which is returned if there are
                            no overrides and no values provided in the section

            Returns: the option value
        """
        return self.overrides.get(section+'.'+option, self.cfg.get(section, option, fallback=default))

    @classmethod
    def _get_svn_version_info(cls, path: Path) -> Tuple[str, str, str]:
        """
            A helper method to get svn version information from a
            svn repository using the svn executable.

            Args:
                path:   the path where the repository is located

            Returns: The triple (revision id, revision date, revision url)

            Note: Requires the svn executable to be located in ``/usr/bin/svn``
            or available on the path.
        """
        if Path('/usr/bin/svn').exists():
            svn_executable = '/usr/bin/svn'
        else:
            svn_executable = 'svn'
        with subprocess.Popen([svn_executable, "info"], stdout=subprocess.PIPE, encoding='utf-8', cwd=path, stderr=subprocess.PIPE) as svn_proc:
            data = svn_proc.stdout.read().strip().split('\n')  # type: ignore
            rev_id = data[6].split(':', maxsplit=1)[1].strip()
            rev_date = data[-1].split(':', maxsplit=1)[1].strip()
            rev_url = data[2].split(':', maxsplit=1)[1].strip()
            return rev_id, rev_date, rev_url

    @classmethod
    def _get_git_version_info(cls, path: Path) -> Tuple[str, str, str]:
        """
            A helper method to get git version information from a
            git repository using the git executable.

            Args:
                path:   the path where the repository is located

            Returns: The triple (revision id, revision date, svn revision info);
                     some of these may be set to unknown

            Note: Requires the git executable to be located in ``/usr/bin/git``
            or available on the path.
        """
        if Path('/usr/bin/git').exists():
            git_executable = '/usr/bin/git'
        else:
            git_executable = 'git'
        with subprocess.Popen([git_executable, "log"], stdout=subprocess.PIPE, encoding='utf-8', cwd=path, stderr=subprocess.PIPE) as git_proc:
            rev_date = 'Unknown'
            for ln in git_proc.stdout.readlines():  # type: ignore
                if ln.startswith('Date: '):
                    rev_date = ln.split(':', maxsplit=1)[1].strip()
                if ln.strip().startswith('git-svn-id'):
                    _, svn_info = ln.split(':', maxsplit=1)
                    url, _ = svn_info.strip().split(' ', maxsplit=1)
                    rev_id = url.strip().split('@')[-1].strip()
                    return rev_id, rev_date, "Unknown"
        return 'Unknown', "Unknown", "Unknown"

    def get_repo_version(self, path: Optional[Path] = None) -> Tuple[str, str, str]:
        """
            Uses the git & svn commands to try to find out version of data in `path`. If
            the optional argument `path` is not given, defaults to the 'aktualni_data/data-txt'
            subdirectory of :attr:`Config.vallex_repo`.

            Returns:  A triple, the first being the svn revision id (or ``Unknown``),
                      the second the date of last change (or ``Unknown``) and the third
                      the repo url (or ``Unknown``).
        """
        if not path and self.vallex_repo:
            path = self.vallex_repo/'aktualni_data'/'data-txt'
        if not path:
            return 'Unknown', 'Unknown', "Unknown"
        try:
            return self._get_svn_version_info(path)
        except Exception as ex:
            pass
        try:
            return self._get_git_version_info(path)
        except Exception as ex:
            pass
        return 'Unknown', 'Unknown', "Unknown"

    @property
    def config_paths(self) -> List[Path]:
        """
            A list of locations (including the config file name) from which configuration is read.
            Configuration settings in later elements override those in previous ones.
        """

        # First test whether env provides paths; if so, it overrides all
        env_paths = [Path(p.strip()) for p in os.getenv('PY_VALLEX_CONFIG', '').split(':') if p.strip()]
        if env_paths:
            return [p for p in env_paths]

        # On Linux and not MAC OS unices look for pyvallex.ini in ~/.config
        # or $XDG_CONFIG_HOME
        if 'darwin' not in sys.platform and 'win' not in sys.platform:
            env_paths.append(Path(os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config"))))

        if FROZEN:
            env_paths.append(SCRIPT_DIR)

        # A config file in the current directory overrides the
        # one found in home
        env_paths.append(Path('.'))

        return [(p/self._CFG_NAME).absolute() for p in env_paths]

    def config_found(self) -> bool:
        """
            Returns true if a config file exists in at least one of the default search paths.
        """
        for config_location in self.config_paths:
            if config_location.exists():
                return True
        return False

    def __init__(self, config_path: Optional[Union[str, Path]] = None, search_default_locations=True, overrides: Optional[dict] = None):
        """
            Loads configuration from the default locations (unless `search_default_locations` is ``False``)
            and those specified in `config_paths`. Optionally settings may be overriden by putting
            the overriding values into the `overrides` dictionary.
        """

        self.cfg = configparser.ConfigParser()
        self.overrides = overrides or dict()

        self.cfg_paths: List[Path] = []
        if search_default_locations:
            self.cfg_paths = self.config_paths
        if config_path:
            self.cfg_paths.append(Path(config_path))

        self.cfg.read([str(p) for p in self.cfg_paths])

        self.release_url = self._get_option('update', 'channel', DEFAULT_RELEASE_LIST)
        self.release_key = self._get_option('update', 'release_key', RELEASE_VERIFY_KEY)

        self.lexicon_dirs = [Path(p.strip()).absolute() for p in self._get_option('data', 'lexicon-dirs', '').split('\n') if p.strip()]
        self.vallex_repo: Optional[Path] = self._get_option('data', 'vallex-repo', None)

        self.update_lexicon_dirs()
        self.update_lexicon_lists()

        self.web_host = str(self._get_option('web', 'host', 'localhost'))
        self.web_port = int(self._get_option('web', 'port', '8080'))
        self.web_db = Path(str(self._get_option('web', 'db', 'web-db'))).absolute()
        self.web_ui_config = Path(str(self._get_option('web', 'webui-config', 'webui-config.json'))).absolute()
        self.web_mode = str(self._get_option('web', 'mode', 'client'))

        if self.web_mode == 'client':
            default_dist_dir = (Path(__file__).parent/'server'/'frontend'/'dist').absolute()
        else:
            default_dist_dir = (Path(__file__).parent/'server'/'frontend'/'dist-server').absolute()
        self.web_dist_dir = Path(str(self._get_option('web', 'dist-dir', str(default_dist_dir)))).absolute()

        if not self.web_ui_config.exists():
            self.web_ui_config = (Path(__file__).parent/'server'/'frontend'/'webui-config.json').absolute()

        # Logging
        self.default_log_level = self._get_option('logging', 'level', 'INFO').upper()
        self.log_file = Path(str(self._get_option('logging', 'file', 'vallex-cli.log'))).absolute()
        self.log_filters = {
            component.replace('.', ':'): str(self.cfg.get('logging', component, fallback='INFO')).upper()
            for component in self.cfg.options('logging')
            if component not in ['file', 'level']
        } if self.cfg.has_section('logging') else {}

    def update_lexicon_dirs(self):
        if self.vallex_repo:
            self.vallex_repo = Path(self.vallex_repo).absolute()
            if not self.lexicon_dirs and self.vallex_repo.is_dir():
                if (self.vallex_repo/'aktualni_data'/'data-txt').is_dir():
                    self.lexicon_dirs = [self.vallex_repo/'aktualni_data'/'data-txt']
                else:
                    self.lexicon_dirs = [self.vallex_repo]

    def update_lexicon_lists(self):
        self.lexicons = list(filter(lambda x: x is not None, [self.resolve_lex_path(p.strip()) for p in self._get_option('data', 'lexicons', '').split('\n') if p.strip()]))
        if not self.lexicons and self.lexicon_dirs:
            self.lexicons = sum([[p.absolute() for p in d.glob('*.txt') if not p.name.startswith('_')] for d in self.lexicon_dirs], [])
        self.web_lexicons = list(filter(lambda x: x is not None, [self.resolve_lex_path(p.strip()) for p in self._get_option('web', 'web_lexicons', '').split('\n') if p.strip()]))
        if not self.web_lexicons:
            self.web_lexicons = self.lexicons

    @property
    def script_dirs(self):
        if self.vallex_repo:
            return [self.vallex_repo/'scripts']

    def resolve_lex_path(self, path: Union[str, Path]):
        """
            Finds an absolute path to a lexicon, searching for it
            in the lexicon dirs.

            Arg:
                path: file name of the lexicon

            Returns: The absolute path to the lexicon. If the provided
            path is already absolute and exists, returns it as is.
            Otherwise it searches for the path in lexicon dirs.
            If no lexicon is found, returns None.
        """
        p = Path(path)
        if p.exists():
            return p.absolute()
        elif not p.is_absolute():
            for d in self.lexicon_dirs:
                if (d/path).exists():
                    return (d/path).absolute()
        return None

    def __str__(self):
        """
            Returns a string representation of the configuration suitable for
            writing to the configuration ini file.
        """
        if FROZEN:
            return "\n".join([
                "[data]",
                "lexicon-dirs = "+"\n               ".join([str(d) for d in self.lexicon_dirs]),
                "vallex-repo  = "+str(self.vallex_repo),
                "lexicons     = "+"\n               ".join([str(l) for l in self.lexicons]),
                "",
                "[update]",
                "channel      = "+str(self.release_url),
                "release_key  = "+str(self.release_key),
                "",
                "[logging]",
                "level        = "+str(self.default_log_level),
                "file         = "+str(self.log_file),
            ] + [component.replace(':', '.') + " = " + level for component, level in self.log_filters.items()])

        return "\n".join([
            "[data]",
            "lexicon-dirs = "+"\n               ".join([str(d) for d in self.lexicon_dirs]),
            "vallex-repo  = "+str(self.vallex_repo),
            "lexicons     = "+"\n               ".join([str(l) for l in self.lexicons]),
            "",
            "[web]",
            "host         = "+self.web_host,
            "port         = "+str(self.web_port),
            "db           = "+str(self.web_db),
            "webui-config = "+str(self.web_ui_config),
            "web_lexicons = "+"\n               ".join([str(l) for l in self.web_lexicons]),
            "mode         = "+self.web_mode,
            "dist-dir     = "+str(self.web_dist_dir),
            "",
            "[update]",
            "channel      = "+str(self.release_url),
            "release_key  = "+str(self.release_key),
            "",
            "[logging]",
            "level        = "+str(self.default_log_level),
            "file         = "+str(self.log_file),
        ] + [component.replace(':', '.') + " = " + level for component, level in self.log_filters.items()])
