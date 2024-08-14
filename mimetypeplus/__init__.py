"""
A module containing the MimeType class, allowing for easy managing of mimetypes in python.
Main source: https://datatracker.ietf.org/doc/html/rfc6838#section-4
"""

from .mimetypeplus import MimeType, MAGICMIME_AVAILABLE, PUREMAGICMIME_AVAILABLE

__version__ = "1.0.0.0"
__all__ = ["MimeType", "MAGICMIME_AVAILABLE", "PUREMAGICMIME_AVAILABLE"]
