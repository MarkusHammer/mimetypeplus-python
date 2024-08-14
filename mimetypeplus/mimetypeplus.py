"""
mimetypeplus

A module containing the MimeType class, allowing for easy managing of mimetypes in python.
Main source: https://datatracker.ietf.org/doc/html/rfc6838#section-4
"""

#pylint:disable=wildcard-import,unused-wildcard-import

from string import (digits as DIGITS, ascii_letters as ALPHA)

from .typings import *
from .mimetypecheckers import *
from .tools import *

class MimeType():
    """
    MimeType
    
    A convenient way to manage and manipulate mime types,
    as well as identifying the types of, and extentions for mime types.
    
    Main source: https://datatracker.ietf.org/doc/html/rfc6838#section-4
    """

    # this is meant to be called when the class is defined,
    # hence it's uncommon placement
    mimetypes_init()

    DEFAULT_TEXT_EXTENTION:LiteralString = "txt"
    DEFAULT_BINARY_EXTENTION:LiteralString = "bin"

    EXPEREMENTAL_FACET:LiteralString = "x"
    VENDOR_FACET:LiteralString = "vnd"
    PERSONAL_FACET:LiteralString = "prs"

    STRICTLY_ALLOWED_CHARACTERS:LiteralString = DIGITS + ALPHA + "!#$&-^_.+"
    WILDCARD_SEQUENCE:LiteralString = ""
    ALLOWED_CHARACTERS:LiteralString = singlify_str(STRICTLY_ALLOWED_CHARACTERS, WILDCARD_SEQUENCE)

    @staticmethod
    def from_xml_content(content_snippet:str) -> Union['MimeType', None]:
        """
        from_xml_content
        Creates a MimeType object from the given text content of a xml file if possible.
        Usually usefull for correcting self reported content types of pages retrieved from the web;
        which may return a plain text mimetype even though the content may be a type of xml.

        Arguments:
            content_snippet - The beginning snippet of the content as a string.

        Returns:
            MimeType object with a correct mimetype if possible, otherwise None.
        """
        string = mime_string_from_xml_content(content_snippet)
        return MimeType(string) if string is not None else None

    @staticmethod
    def from_path(path:Union[str, PathLike], strict:bool = False) -> Union['MimeType', None]:
        """
        from_path
        Creates a MimeType object from the given local path.

        Arguments:
            path - The path to be checked.
            strict - Allow for non standard types to be included in some types of checking.

        Returns:
            MimeType object with a correct mimetype if possible, otherwise None.
        """
        string = mime_string_from_path(path, strict=strict)
        return MimeType(string) if string is not None else None

    @staticmethod
    def from_uri(uri:str, strict:bool = False) -> Union['MimeType', None]:
        """
        from_uri
        Creates a MimeType object from the given uri.

        Arguments:
            uri - The uri to be checked.

        Returns:
            MimeType object with a correct mimetype if possible, otherwise None.
        """
        string = mime_string_from_path(uri, strict=strict, no_local_checks=True)
        return MimeType(string) if string is not None else None
    from_url = from_uri

    @staticmethod
    def from_data(buffer:Union[bytes, str],
                  *,
                  hint_path:Union[str, PathLike, None] = None,
                  encoding: str = "utf8",
                  errors:str = "strict"
                 ) -> Union['MimeType', None]:
        """
        from_data
        Creates a MimeType object from the given data.

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
            MimeType object with a correct mimetype if possible, otherwise None.
        """
        string = mime_string_from_data(buffer,
                                       hint_path = hint_path,
                                       encoding = encoding,
                                       errors = errors
                                      )
        return MimeType(string) if string is not None else None

    def __init__(self,
                 mime:Union['MimeType', str, Tuple[str, str], Iterable[str]] = "",
                 *,
                 maintype: str = "",
                 subtype: str = "",
                ):
        """
        __init__ Creates a MimeType object.

        Keyword Arguments:
            mime -- The object to base the mime type off of.
                Accepts full strings, 2 string tuples,
                iterables (expected to return only 2 strings), or another MimeType object.
            maintype -- Used to override the maintype, if not an empty string.
            subtype -- Used to override the subtype, if not an empty string.
        """
        self.__maintype: str = MimeType.WILDCARD_SEQUENCE
        self.__subtype: str = MimeType.WILDCARD_SEQUENCE

        if isinstance(mime, MimeType):
            mime = tuple(mime)
        elif isinstance(mime, str):
            mime = tuple(mime.split("/"))
        elif isinstance(mime, Iterable):
            mime = tuple(x.strip("/") for x in mime)

        assert len(mime) in (1,2), "BAD MIME CONVERSION ERROR"

        self.maintype = mime[0]
        if len(mime) == 2:
            self.subtype = mime[1]

        if maintype != "":
            self.maintype = maintype
        if subtype != "":
            self.subtype = subtype

    @property
    def maintype(self) -> str:
        """
        maintype
        The 'main' part of the mimetype.
        """
        return self.__maintype
    @maintype.setter
    def maintype(self, value: str):
        value = (value).strip().lower()
        if value == "":
            value = MimeType.WILDCARD_SEQUENCE
        self.__maintype = value

    @property
    def subtype(self) -> str:
        """
        subtype
        The 'sub' part of the mimetype.
        """
        return self.__subtype
    @subtype.setter
    def subtype(self, value: str):
        value = (value).strip().lower()
        if value == "":
            value = MimeType.WILDCARD_SEQUENCE
        self.__subtype = value

    @property
    def suffix(self) -> str:
        """
        suffix
        The 'suffix' part of the mimetype (the section of the subtype after the last '+'), if any.
        A blank string if not set.
        """
        index = self.subtype.rfind("+")
        if index < 0:
            return ""
        else:
            return self.subtype[index+1:]
    @suffix.setter
    def suffix(self, value: str):
        index = self.subtype.rfind("+")
        if index < 0:
            self.subtype += f"+{value}"
        else:
            self.subtype = self.subtype[:index+1] + value
    structure = suffix
    syntax = suffix

    @property
    def facet(self) -> str:
        """
        facet
        The 'facet' part of the mimetype (the section of the subtype before the first '.'), if any.
        A blank string if not set.
        """
        index = self.subtype.find(".")
        if index < 0:
            return ""
        else:
            return self.subtype[:index]
    @facet.setter
    def facet(self, value: str):
        index = self.subtype.find(".")
        if index < 0:
            self.subtype += f"{value}."
        else:
            self.subtype = value + self.subtype[index:]

    @property
    def experimental_facet(self) -> bool:
        """
        True if the mimetype is marked as experemental (using the facet of the type).
        """
        return self.facet == MimeType.EXPEREMENTAL_FACET

    @property
    def vendor_facet(self) -> bool:
        """
        True if the mimetype is marked as vendor (using the facet of the type).
        """
        return self.facet == MimeType.VENDOR_FACET

    @property
    def personal_facet(self) -> bool:
        """
        True if the mimetype is marked as personal (using the facet of the type).
        """
        return self.facet == MimeType.PERSONAL_FACET

    def encode(self) -> str:
        """
        encode
        
        Returns:
            The MimeType object as a string.
        """
        return f"{self.maintype}/{self.subtype}"
    __str__ = encode
    __repr__ = encode

    def is_empty(self) -> bool:
        """
        is_empty
        
        Returns:
            True if both the main and subtype are empty (unset), otherwise false.
        """
        main_wild = self.maintype == MimeType.WILDCARD_SEQUENCE
        sub_wild = self.subtype == MimeType.WILDCARD_SEQUENCE
        return main_wild and sub_wild
    def __bool__(self):
        """
        Returns:
            True if not empty.
        """
        return not self.is_empty()

    def is_valid(self, strict:bool = True) -> bool:
        """
        is_valid

        Keyword Arguments:
            strict - If true, strictly only the characters stated to be used
            in mimetypes will be consitered valid.

        Returns:
            True if all characters used in the mimetype are allowed
            as stated in the official specification (RFC docs),
            and optionally a few other commonly used characters in mime types.
        """
        charset = (MimeType.STRICTLY_ALLOWED_CHARACTERS if strict else MimeType.ALLOWED_CHARACTERS)
        testcollection = ""
        if self.maintype != MimeType.WILDCARD_SEQUENCE:
            testcollection += self.maintype
        if self.subtype != MimeType.WILDCARD_SEQUENCE:
            testcollection += self.subtype
        for char in testcollection:
            if not char in charset:
                return False
        return True

    def to_extention(self, strict:bool = False) -> Union[str, None]:
        """
        to_extention

        Keyword Arguments:
            strict - When true, excludes commoly used but non standard types.

        Returns:
            A string of the expected extention for the type if found,
            otherwise None.
        """
        if not self.is_empty():
            ext = guess_extension_text(
                                       str(self).replace(MimeType.WILDCARD_SEQUENCE, ""),
                                       strict=strict
                                      )
            if ext is not None:
                ext = ext.lstrip(".")
            elif self.maintype == "text":
                ext = MimeType.DEFAULT_TEXT_EXTENTION
            elif self.maintype != MimeType.WILDCARD_SEQUENCE:
                ext = MimeType.DEFAULT_BINARY_EXTENTION
            return ext
        else:
            return None

    def __eq__(self,
               other:Union['MimeType', str, Tuple[str, str], Iterable[str], object]
              ) -> Union[bool, NotImplementedType]:
        if not isinstance(other, (MimeType, tuple, str, Iterable)):
            return NotImplemented
        return tuple(self) == tuple(MimeType(other))

    def __iter__(self):
        yield self.maintype
        yield self.subtype
