from .typings import Union

ZIP_STORED:int = 0

PK_ZIP_FIRST_HALF_HEADER = b"PK"

ODF_MIMETYPE_FILENAME = "mimetype"
ODF_MIMETYPE_ENCODING = "ascii"
ODF_MIMETYPE_FILENAME_RAW = ODF_MIMETYPE_FILENAME.encode("ascii", "strict")
assert len(ODF_MIMETYPE_FILENAME_RAW) == 8 and len(ODF_MIMETYPE_FILENAME_RAW) == len(ODF_MIMETYPE_FILENAME)


def mime_string_from_odf_zip_raw(
   raw_data:bytes,
   errors:str = "strict"
) -> Union[str, None]:
    # https://docs.oasis-open.org/office/OpenDocument/v1.3/os/part2-packages/OpenDocument-v1.3-os-part2-packages.html#__RefHeading__752809_826425813
    # NOTE This expects that the data provided is the absolute start of the
    # stream being parsed, and will only attempt to return `None` based on this fact.
    # It is the responsibility of the user if/when it may be necessary,
    # to ensure that the trailing part of the stream would result in
    # proper zip file formatting as the odf format specifies;
    # as it is possible for zip file data to be
    # segmented amongst multiple streams, or to be large enough that
    # it would be desirable to only check a portion of it.

    if not raw_data.startswith(PK_ZIP_FIRST_HALF_HEADER):
        return None

    # Not checking the bit flags at offset 8
    # as that level of granularity is unnecessary

    comp_method = int.from_bytes(raw_data[10:10+2], 'little', signed=False)
    if comp_method != ZIP_STORED:
        return None

    decomp_len = int.from_bytes(raw_data[18:18+4], 'little', signed=False)
    if decomp_len <= 0 or decomp_len >= 0xFFFFFFFF:
        # Some compressors may leave a size feild at 0 if its stored,
        # or if it didn't know the size during archiving.
        # A size of 0xFFFFFFFF indicates its a zip64 format size.
        decomp_len = None
    comp_len = int.from_bytes(raw_data[22:22+4], 'little', signed=False)
    if comp_len <= 0 or comp_len >= 0xFFFFFFFF:
        # Some compressors may leave a size feild at 0 if its stored,
        # or if it didn't know the size during archiving.
        # A size of 0xFFFFFFFF indicates its a zip64 format size.
        comp_len = None

    if comp_len and decomp_len and comp_len != decomp_len:
        # Thats not right
        return None

    name_len = int.from_bytes(raw_data[26:26+2], 'little', signed=False)
    if name_len != len(ODF_MIMETYPE_FILENAME_RAW):
        return None

    extra_len = int.from_bytes(raw_data[28:28+2], 'little', signed=False)
    if extra_len != 0:
        # Extra data is not allowed, otherwise it would be in the place the mimetype is expected to be
        return None

    if raw_data[30:30+name_len] != ODF_MIMETYPE_FILENAME_RAW:
        return None

    raw_content = raw_data[30+name_len:]
    if not raw_content:
        return None

    expect_content_len = comp_len
    if not expect_content_len:
        try:
            # Read up to the next PK header.
            # Weather its a zip64 header or the next file header
            # if the lengths from the header arn't set,
            # then the only way to know that we got the whole
            # mimetype captured is to search for the next instance of b"PK".
            # Weather that index is the header for the next file or
            # an entry for zip64 data,
            # we know the index the current files content must stop at.
            # Also, as full
            # (both the ascii encoded values of `b'PK'` and
            # the appropriate 2 bytes after)
            # cannot be a proper ascii encoded string,
            # a false match would only happen for a corrupt
            # or incompatible stream anyway.
            expect_content_len = raw_content.index(PK_ZIP_FIRST_HALF_HEADER)
        except ValueError:
            return None

    b = raw_content[:expect_content_len]
    if not b:
        return None
    return b.decode("ascii", errors)
