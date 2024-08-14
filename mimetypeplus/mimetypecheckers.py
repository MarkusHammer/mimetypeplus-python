"""
mimetypecheckers

Type checker utilities for the MimeType module
"""

#pylint:disable=unused-import,wildcard-import,unused-wildcard-import,pointless-string-statement

from mimetypes import (
    guess_extension as guess_extension_text,
    guess_type as guess_type_path_URI,
    init as mimetypes_init
)

from .cmds import *
from .typings import *

"""True if the 'magic' module was imported."""
MAGICMIME_AVAILABLE: bool  # DO NOT MODIFY, READ ONLY
try:
    from magic import from_buffer as magic_from_buffer, from_file as magic_from_path
    MAGICMIME_AVAILABLE = True
except ImportError:
    MAGICMIME_AVAILABLE = False

"""True if the 'puremagic' module was imported."""
PUREMAGICMIME_AVAILABLE: bool  # DO NOT MODIFY, READ ONLY
try:
    from puremagic import (from_file as puremagic_from_path,    #type:ignore
                           from_string as puremagic_from_buffer,
                           PureError
                          )
    PUREMAGICMIME_AVAILABLE = True
except ImportError:
    PUREMAGICMIME_AVAILABLE = False

mimetypes_init()

XML_DOCTYPE_HEADERS = {
    "<!doctypehtml>": "text/html",
    "<!doctypehtm>": "text/htm",
    "<!doctypexml>": "text/xml",
    "<?xml": "text/xml",
}
def mime_string_from_xml_content(content_snippet:str) -> Union[str, None]:

    """
    mime_string_from_xml_content
    Gets the mime type from the given text content of a xml file if possible.
    Usually usefull for correcting self reported content types of pages retrieved from the web;
    which may return a plain text mimetype even though the content may be a type of xml.

    Arguments:
        content_snippet - The beginning snippet of the content as a string.

    Returns:
        String with a correct mimetype if possible, otherwise None.
    """

    content_snippet = content_snippet[:min(50, len(content_snippet)-1)].replace(" ", "").lower()
    for k, v in XML_DOCTYPE_HEADERS.items():
        if content_snippet.startswith(k):
            return v
    return None

def mime_string_from_path(
                          path:Union[str, PathLike, Path],
                          strict:bool = False,
                          *,
                          no_local_checks:bool = False
                         ) -> Union[str, None]:

    """
    mime_string_from_path
    Gets the mime type from the given local path.

    Arguments:
        path - The path to be checked.
        strict - Allow for non standard types to be included in some types of checking.
        no_local_checks - Skips checks that requires a path to be available on the local filesystem.
            Allows for URIs to be checked safely.

    Returns:
        String with a correct mimetype if possible, otherwise None.
    """

    mime:str = ""

    if PUREMAGICMIME_AVAILABLE and not no_local_checks:
        try:
            mime = puremagic_from_path(path, mime = True).strip() #type: ignore
        except PureError: #type:ignore
            pass

    if mime == "" and MAGICMIME_AVAILABLE:
        mime = magic_from_path(path, mime=True).strip() #type:ignore

    if mime == "" and not no_local_checks:
        guess = file_cmd_mime_type_from_path(path)
        mime = guess if guess is not None else ""

    if mime == "" and not no_local_checks:
        guess = mimetype_cmd_mime_type_from_path(path)
        mime = guess if guess is not None else ""

    if mime == "" and not no_local_checks:
        guess = xdgmime_cmd_mime_type_from_path(path)
        mime = guess if guess is not None else ""

    if mime == "":
        guess = guess_type_path_URI(str(path), strict)[0]
        mime = guess.strip() if guess is not None else ""

    return mime if mime != "" else None

def mime_string_from_data(
                          buffer:Union[bytes, str],
                          *, hint_path:Union[str, PathLike, None] = None,
                          encoding: str = "utf8",
                          errors:str = "strict"
                         ) -> Union[None, str]:

    """
    mime_string_from_data
    Gets the mime type from the given data.

    Arguments:
        buffer - Either bytes or a string.
        hint_path - A optional path to the data if located on the system.
            Used to make some typechecks more accurate.
        encoding - The presumed encoding of the data if it is a string.
            This does not have to be accurate in cases where the content is expected
            to be a binary format, and the content is already bytes.
            This is used to encode strings, or decode bytes into the oppsite form,
            allowing for more type checksers to be used.
        errors - See the encoding argument. Used in the same context,
            but indicates how to handle encoding/decoding errors.
            Values match the values used in the str.encode and bytes.decode errors argument.

    Returns:
        String with a correct mimetype if possible, otherwise None.
    """

    mime:str = ""

    #strictly the buffer converted into bytes, if possible
    bytes_content:Union[bytes,None] = None
    try:
        if isinstance(buffer, str):
            bytes_content = cast(str, buffer).encode(encoding, errors)
        else:
            bytes_content = buffer
    except (UnicodeEncodeError, UnicodeError):
        bytes_content = None

    #strictly the buffer converted into a string, if possible
    str_content:Union[str,None] = None
    try:
        if not isinstance(buffer, str):
            str_content = cast(bytes, buffer).decode(encoding, errors)
        else:
            str_content = buffer
    except (UnicodeDecodeError, UnicodeError):
        str_content = None

    if mime == "" and PUREMAGICMIME_AVAILABLE:
        try:
            mime = puremagic_from_buffer( #type:ignore
                                         buffer,
                                         mime = True,
                                         filename = hint_path
                                        ).strip()
        except PureError: #type:ignore
            pass

    if mime == "" and MAGICMIME_AVAILABLE:
        mime = magic_from_buffer(bytes_content, mime=True).strip() #type:ignore

    if mime == "" and hint_path is not None:
        found = mime_string_from_path(hint_path)
        mime = found if found is not None else ""

    if mime == "" and str_content is not None:
        mime = "text/"

    mime = mime.strip().lower()
    if str_content is not None and mime.startswith("text/"):
        xml_check = mime_string_from_xml_content(str_content)
        if xml_check is not None:
            mime = xml_check.strip()

    return mime if mime != "" and mime.count("/") == 1 else None
