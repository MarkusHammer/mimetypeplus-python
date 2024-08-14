"""
tools

The tools used in the MimeType module
"""

#pylint:disable=wildcard-import,unused-wildcard-import

from .typings import *

def singlify_str(*in_strs:LiteralString) -> LiteralString:
    """
    singlify_str
    Gets a singlified string of all the characters in the given strings (in no particular order).

    Returns:
        A LiteralString with only one instance of every character
        in the given string (in no particular order).
    """
    return cast(LiteralString, "".join(set("".join(in_strs))))
