# Diffuse: security helpers for local files and child processes.

import errno
import os
import stat

from typing import BinaryIO, Final, List, Optional


MAX_FILE_BYTES: Final[int] = 512 * 1024 * 1024
MAX_VCS_OUTPUT_BYTES: Final[int] = 512 * 1024 * 1024
_WINDOWS_REPARSE_POINT: Final[int] = 0x400
_FLATPAK_HOST_COMMANDS: Final[dict[str, str]] = {
    'bzr': '/usr/bin/bzr',
    'co': '/usr/bin/co',
    'cvs': '/usr/bin/cvs',
    'darcs': '/usr/bin/darcs',
    'git': '/usr/bin/git',
    'hg': '/usr/bin/hg',
    'mtn': '/usr/bin/mtn',
    'rlog': '/usr/bin/rlog',
    'svn': '/usr/bin/svn',
}


def _is_reparse_point(file_stat: os.stat_result) -> bool:
    attributes = getattr(file_stat, 'st_file_attributes', 0)
    return bool(attributes & _WINDOWS_REPARSE_POINT)


def validate_regular_file(path: str, max_bytes: int = MAX_FILE_BYTES) -> os.stat_result:
    """Reject links, reparse points, special files, and oversized inputs."""
    file_stat = os.lstat(path)
    if stat.S_ISLNK(file_stat.st_mode) or _is_reparse_point(file_stat):
        raise OSError(errno.ELOOP, 'Refusing to follow a symbolic link or reparse point', path)
    if not stat.S_ISREG(file_stat.st_mode):
        raise OSError(errno.EINVAL, 'Refusing to open a non-regular file', path)
    if file_stat.st_size > max_bytes:
        raise OSError(errno.EFBIG, f'File exceeds the {max_bytes}-byte safety limit', path)
    return file_stat


def read_file_bytes(path: str, max_bytes: int = MAX_FILE_BYTES) -> bytes:
    validate_regular_file(path, max_bytes)
    flags = os.O_RDONLY | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, 'rb') as stream:
        return read_stream_limited(stream, max_bytes)


def write_file_bytes(path: str, data: bytes) -> None:
    if os.path.lexists(path):
        validate_regular_file(path, max(len(data), MAX_FILE_BYTES))
    flags = (
        os.O_WRONLY | os.O_CREAT | os.O_TRUNC |
        getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    )
    descriptor = os.open(path, flags, 0o666)
    with os.fdopen(descriptor, 'wb') as stream:
        stream.write(data)


def read_stream_limited(stream: BinaryIO, max_bytes: int) -> bytes:
    chunks = []
    size = 0
    while True:
        chunk = stream.read(min(1024 * 1024, max_bytes - size + 1))
        if not chunk:
            return b''.join(chunks)
        chunks.append(chunk)
        size += len(chunk)
        if size > max_bytes:
            raise OSError(errno.EFBIG, f'Process output exceeds the {max_bytes}-byte safety limit')


def _inside(path: str, root: Optional[str]) -> bool:
    if root is None:
        return False
    try:
        real_root = os.path.realpath(root)
        return os.path.commonpath((os.path.realpath(path), real_root)) == real_root
    except ValueError:
        return False


def resolve_executable(command: str, forbidden_root: Optional[str] = None) -> str:
    """Resolve an executable without implicitly searching an untrusted cwd."""
    expanded = os.path.expandvars(os.path.expanduser(command))
    if os.path.dirname(expanded):
        candidate = os.path.abspath(expanded)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
        raise FileNotFoundError(errno.ENOENT, 'Executable was not found', command)

    extensions = ['']
    if os.name == 'nt':
        path_extensions = os.environ.get('PATHEXT', '.COM;.EXE;.BAT;.CMD')
        extensions = [ext.lower() for ext in path_extensions.split(';')]
        if os.path.splitext(expanded)[1].lower() in extensions:
            extensions = ['']

    for entry in os.environ.get('PATH', os.defpath).split(os.pathsep):
        if not entry:
            continue
        directory = os.path.realpath(os.path.expandvars(os.path.expanduser(entry)))
        if _inside(directory, forbidden_root):
            continue
        for extension in extensions:
            candidate = os.path.join(directory, expanded + extension)
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return os.path.abspath(candidate)
    message = 'Executable was not found in trusted PATH entries'
    raise FileNotFoundError(errno.ENOENT, message, command)


def flatpak_host_command(command: List[str]) -> List[str]:
    """Allow only known VCS tools when legacy host spawning is explicitly enabled."""
    if not command or command[0] not in _FLATPAK_HOST_COMMANDS:
        raise OSError(errno.EPERM, 'Flatpak host command is not allowlisted')
    return [
        '/usr/bin/flatpak-spawn', '--host', '--clear-env',
        '--env=PATH=/usr/bin:/bin', _FLATPAK_HOST_COMMANDS[command[0]],
        *command[1:],
    ]
