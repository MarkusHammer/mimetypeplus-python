from zipfile import ZipFile

from .ziptypesraw import ZIP_STORED, ODF_MIMETYPE_FILENAME
from .typings import Union

def mime_string_from_odf_zip_parsed(parsed_zip:'ZipFile',
                                    errors:str = "strict") -> Union[str, None]:
    nl = parsed_zip.namelist()
    if not nl or nl[0] != ODF_MIMETYPE_FILENAME:
        # Its required for an odf mimetype file to be the first file in the archive.
        return None
    info = parsed_zip.getinfo(ODF_MIMETYPE_FILENAME)
    if info.extra:
        # Its explicitly required for the mimetype file to not contain any extra data
        return None
    if info.compress_type != ZIP_STORED:
        # Its explicitly required for the mimetype file to be stored (without compression)
        return None
    b = None
    with parsed_zip.open(info, "r") as mt:
        b = mt.read(-1)
    if b is None:
        return None
    return b.decode("ascii", errors)
