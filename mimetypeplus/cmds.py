"""
cmds

Local command line based utilities for mime type checking.
"""

#pylint:disable=pointless-string-statement

from shutil import which
from subprocess import check_output

from .typings import * #pylint:disable=wildcard-import,unused-wildcard-import

"""
Holds either the system's path to the 'file' command's executable,
or None, if it wasn't found.
"""
FILE_CMD:Union[LiteralString, None] = cast(LiteralString, which("file"))
"""
Holds either the system's path to the 'mimetype' command's executable,
or None, if it wasn't found.
"""
MIMETYPE_CMD:Union[LiteralString, None] = cast(LiteralString, which("mimetype"))
"""
Holds either the system's path to the 'xdg-mime' command's executable,
or None, if it wasn't found.
"""
XDGMIME_CMD:Union[LiteralString, None] = cast(LiteralString, which("xdg-mime"))

def file_cmd_mime_type_from_path(path:Union[Path, PathLike, str]) -> Union[str, None]:
    """
    file_cmd_mime_type_from_path
    Runs the system's 'file' command (if found) on the given path.

    Arguments:
        path - The local path to the file on the system.

    Returns:
        None if the type is not found, or 'file' is not acessable in the current environment,
        or a string of the mime type.
    """
    if FILE_CMD is None:
        return None

    try:
        path = Path(path)
        path = path.expanduser().resolve()
    except TypeError:
        return None

    if not path.exists() or not path.is_file():
        return None

    args = [FILE_CMD, "--mime-type", "-b", str(path)]
    guess = check_output(args, shell=True, text=True).strip()
    return guess if guess != "" else None

def mimetype_cmd_mime_type_from_path(path:Union[Path, PathLike, str]) -> Union[str, None]:
    """
    mimetype_cmd_mime_type_from_path
    Runs the system's 'mimetype' command (if found) on the given path.

    Arguments:
        path - The local path to the file on the system.

    Returns:
        None if the type is not found, or 'mimetype' is not acessable in the current environment,
        or a string of the mime type.
    """
    if MIMETYPE_CMD is None:
        return None

    try:
        path = Path(path)
        path = path.expanduser().resolve()
    except TypeError:
        return None

    if not path.exists() or not path.is_file():
        return None

    args = [MIMETYPE_CMD, "-i", "-b", str(path)]
    guess = check_output(args, shell=True, text=True).strip()
    return guess if guess != "" else None

def xdgmime_cmd_mime_type_from_path(path:Union[Path, PathLike, str]) -> Union[str, None]:
    """
    xdgmime_cmd_mime_type_from_path
    Runs the system's 'xdg-mime' command (if found) on the given path.

    Arguments:
        path - The local path to the file on the system.

    Returns:
        None if the type is not found, or 'xdg-mime' is not acessable in the current environment,
        or a string of the mime type.
    """
    if XDGMIME_CMD is None:
        return None

    try:
        path = Path(path)
        path = path.expanduser().resolve()
    except TypeError:
        return None

    if not path.exists() or not path.is_file():
        return None

    args = [XDGMIME_CMD, "query", "filetype", str(path)]
    guess = check_output(args, shell=True, text=True).strip()
    return guess if guess != "" else None
