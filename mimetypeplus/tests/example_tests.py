"""
Tests the MimeType class and how it responds to example paths and files.
"""

import unittest

from ..mimetypeplus import MimeType
from ..typings import cast

class ExampleTests(unittest.TestCase):
    """
    Tests the MimeType class and how it responds to example paths and files.
    """

    EXAMPLE_URL = "https://www.example.com/index.html"
    def test_example_url(self):
        """
        Tests URL input (and type checking).
        """
        mime = cast(MimeType, MimeType.from_uri(ExampleTests.EXAMPLE_URL))
        self.assertIsNotNone(mime)
        self.assertEqual(mime.maintype, "text")

    def test_self_file_path(self):
        """
        Tests file path input (and type checking).
        """
        mime = cast(MimeType, MimeType.from_path(__file__))
        self.assertIsNotNone(mime)
        self.assertEqual(mime.maintype, "text")

    def test_self_file_content_binary(self):
        """
        Tests binary data input (and type checking).
        """
        content = None
        with open(__file__, "rb") as f:
            content = f.read(-1)

        mime = cast(MimeType, MimeType.from_data(content))
        self.assertIsNotNone(mime)
        self.assertEqual(mime.maintype, "text")

    def test_self_file_content_text(self):
        """
        Tests string data input (and type checking).
        """
        content = None
        with open(__file__, "rt", encoding="utf8") as f:
            content = f.read(-1)

        mime = cast(MimeType, MimeType.from_data(content))
        self.assertIsNotNone(mime)
        self.assertEqual(mime.maintype, "text")

if __name__ == "__main__":
    unittest.main()
