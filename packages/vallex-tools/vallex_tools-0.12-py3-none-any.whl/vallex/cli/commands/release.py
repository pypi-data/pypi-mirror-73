import logging

from pathlib import Path

from vallex.cli.lib import main_command, option, root, sub_command, choices_parser
from vallex.config import __version__, SCRIPT
from vallex.term import STATUS, YELLOW, WHITE, GREEN, FG, RED
from vallex.log import log

try:
    import nacl.signing  # type: ignore
    import nacl.encoding  # type: ignore
    from vallex.updater import ReleaseChannel, sign, verify_local_file, Updater
    _HAVE_UPDATER = True
except Exception as ex:
    _HAVE_UPDATER = False
    _UPDATER_ERROR = ex
    log("cli:release", logging.DEBUG, "Could not import updater", _UPDATER_ERROR)


@main_command()
def main(options={}):
    """Commands used to manage release channels. """


@option('--sign-key', str, help='Path to a file containing the hex-encoded key to sign the release with.')
@option('--platform', str, help='The platform for which the release is done.')
@option('--rel-version', str, help='The version of the release as a git-describe tag.')
@option('--base-url', str, help='The base url of the release channel.')
@sub_command()
def add(release_dir, source, options={}):
    """Adds the release located in `source` to the release channel `release_dir` (the path to the dir where releases.json is located.)"""
    if not _HAVE_UPDATER:
        STATUS.print(FG(RED) | "Updater functionality not available (nacl or bsdiff library not present?)")
        log("cli:release", logging.ERROR, "Could not import updater", _UPDATER_ERROR)
        return -1

    sign_key = Path(options['sign-key']).read_text()
    channel = ReleaseChannel(sign_key, options['base-url'], Path(release_dir))
    channel.add_release(Path(source), options['rel-version'], options['platform'])


@option('--sign-key', str, help='Path to a file containing the hex-encoded key to sign the release with.')
@sub_command()
def cleanup(release_dir, options={}):
    """Removes releases which are not on disk from the releases.json file. The argument`release_dir` should be the path to the dir where releases.json is located."""
    if not _HAVE_UPDATER:
        STATUS.print(FG(RED) | "Updater functionality not available (nacl or bsdiff library not present?)")
        log("cli:release", logging.ERROR, "Could not import updater", _UPDATER_ERROR)
        return -1

    sign_key = Path(options['sign-key']).read_text()
    channel = ReleaseChannel(sign_key, '', Path(release_dir))
    missing = channel.cleanup()
    for name, ver, tp, sz in missing:
        if tp == 'full':
            STATUS.print(FG(WHITE) | ver, sz // (1024*1024), "Mb", "[", name, "]")
        else:
            STATUS.print(FG(GREEN) | ver, "("+tp+")", sz // (1024*1024), "Mb", "[", name, "]")
    STATUS.print("")
    STATUS.print(FG(WHITE) | "Total missing size:", FG(GREEN) | str(sum([sz for (_, _, _, sz) in missing]) // (1024*1024)), "Mb")


@sub_command()
def generate_keys(sign_key_path, verify_key_path, options={}):
    """Generates a sign,verify key-pair used to sign releases and stores them in `sign_key_path` and `verify_key_path`"""
    if not _HAVE_UPDATER:
        STATUS.print(FG(RED) | "Updater functionality not available (nacl or bsdiff library not present?)")
        log("cli:release", logging.ERROR, "Could not import updater", _UPDATER_ERROR)
        return -1
    sign, verify = ReleaseChannel.generate_hex_key_pair()
    Path(sign_key_path).write_text(sign)
    Path(verify_key_path).write_text(verify)


@option('--sign-key', str, help='Path to a file containing the hex-encoded key to sign the release with. (Used to check integrity of metadata)')
@sub_command()
def list_local(release_dir, options={}):
    """Shows a list of available releases in the channel `release_dir`"""
    if not _HAVE_UPDATER:
        STATUS.print(FG(RED) | "Updater functionality not available (nacl or bsdiff library not present?)")
        log("cli:release", logging.ERROR, "Could not import updater", _UPDATER_ERROR)
        return -1
    sign_key = Path(options['sign-key']).read_text()
    channel = ReleaseChannel(sign_key, '', Path(release_dir))
    for platform, rels in channel.available_versions().items():
        STATUS.print(FG(YELLOW) | platform)
        for ver, tp, sz in rels:
            if tp == 'full':
                STATUS.print("  ", FG(WHITE) | ver, sz // (1024*1024), "Mb")
            else:
                STATUS.print("  ", FG(GREEN) | ver, "("+tp+")", sz // (1024*1024), "Mb")


@option('--release-key', str, help='Path to a file containing the hex-encoded key to verify releases with.')
@option('--url', str, help='Path to a file containing the hex-encoded key to verify releases with.')
@option('--platform', str, help='Platform to show updates for', parser=choices_parser(['win64', 'linux64']))
@sub_command()
def list_remote(options={}):
    if not _HAVE_UPDATER:
        STATUS.print(FG(RED) | "Updater functionality not available (nacl or bsdiff library not present?)")
        log("cli:release", logging.ERROR, "Could not import updater", _UPDATER_ERROR)
        return -1
    if 'release-key' in options:
        release_key = Path(options['sign-key']).read_text()
    else:
        release_key = root.config.release_key
    release_url = options.get('url', root.config.release_url)
    updater = Updater(release_key, release_url, SCRIPT, __version__)
    if 'platform' in options:
        updater.platform = options['platform']
    updater.check_for_updates()
    for rel in updater.releases.releases:
        if not rel['delta_from']:
            STATUS.print(rel['version'], int(rel['size']/10**6), 'MB', rel['url'])


@option('--sign-key', str, help='Path to a file containing the hex-encoded key to sign the file with.')
@sub_command(name='sign')
def sign_cmd(file, options={}):
    """Signs the `file` using the key `sign-key` and stores the signature in `file`.sig"""
    if not _HAVE_UPDATER:
        STATUS.print(FG(RED) | "Updater functionality not available (nacl or bsdiff library not present?)")
        log("cli:release", logging.ERROR, "Could not import updater", _UPDATER_ERROR)
        return -1
    sign_key = nacl.signing.SigningKey(Path(options['sign-key']).read_text(), encoder=nacl.encoding.HexEncoder)
    contents = Path(file).read_bytes()
    sig = sign(sign_key, contents)
    Path(file+'.sig').write_text(sig)


@option('--verify-key', str, help='Path to a file containing the hex-encoded key to verify the signature with.')
@sub_command()
def verify(file, options={}):
    """Verifies that the signature in `file`.sig is a valid signature of `file` with the key `sign-key`"""
    if not _HAVE_UPDATER:
        STATUS.print(FG(RED) | "Updater functionality not available (nacl or bsdiff library not present?)")
        log("cli:release", logging.ERROR, "Could not import updater", _UPDATER_ERROR)
        return -1
    verify_key = nacl.signing.VerifyKey(Path(options['sign-key']).read_text(), encoder=nacl.encoding.HexEncoder)
    contents = Path(file).read_bytes()
    try:
        verify_local_file(verify_key, file)
        print("OK")
    except:
        print("FAIL")
        return -1
