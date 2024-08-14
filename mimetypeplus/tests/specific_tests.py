"""
Tests the MimeType class and how it responds to preset values.
"""

#pylint:disable=wildcard-import,unused-wildcard-import


import unittest

from ..mimetypeplus import *

class PresetTests(unittest.TestCase):
    """
    Tests the MimeType class and how it responds to preset inputs.
    """

    def test_tuple_in(self):
        """
        Tests tuple input.
        """
        main = "application"
        sub = "something"
        preset = MimeType((main, sub))

        self.assertFalse(preset.is_empty())
        self.assertTrue(preset.is_valid())

        self.assertEqual(preset.maintype, main)
        self.assertEqual(preset.subtype, sub)

        self.assertEqual(preset.suffix, "")
        self.assertEqual(preset.facet, "")
        self.assertTupleEqual(tuple(preset), (main, sub))

        self.assertFalse(preset.experimental_facet)
        self.assertFalse(preset.vendor_facet)
        self.assertFalse(preset.personal_facet)


    def test_str_in(self):
        """
        Tests string input.
        """
        preset = MimeType("application/something")

        self.assertFalse(preset.is_empty())
        self.assertTrue(preset.is_valid())

        self.assertEqual(preset.maintype, "application")
        self.assertEqual(preset.subtype, "something")

        self.assertEqual(preset.suffix, "")
        self.assertEqual(preset.facet, "")
        self.assertTupleEqual(tuple(preset), ("application", "something"))

        self.assertFalse(preset.experimental_facet)
        self.assertFalse(preset.vendor_facet)
        self.assertFalse(preset.personal_facet)

    def test_blank(self):
        """
        Tests blank input.
        """
        preset = MimeType()

        self.assertTrue(preset.is_empty())
        self.assertTrue(preset.is_valid())

        self.assertEqual(preset.maintype, MimeType.WILDCARD_SEQUENCE)
        self.assertEqual(preset.subtype, MimeType.WILDCARD_SEQUENCE)

        self.assertEqual(preset.suffix, "")
        self.assertEqual(preset.facet, "")
        self.assertTupleEqual(
                              tuple(preset),
                              (MimeType.WILDCARD_SEQUENCE, MimeType.WILDCARD_SEQUENCE)
                             )

        self.assertFalse(preset.experimental_facet)
        self.assertFalse(preset.vendor_facet)
        self.assertFalse(preset.personal_facet)

    def test_suffix(self):
        """
        Tests the suffix property.
        """
        preset = MimeType(("application", "something+else"))

        self.assertFalse(preset.is_empty())
        self.assertTrue(preset.is_valid())

        self.assertEqual(preset.maintype, "application")
        self.assertEqual(preset.subtype, "something+else")

        self.assertEqual(preset.suffix, "else")
        self.assertEqual(preset.facet, "")

        self.assertFalse(preset.experimental_facet)
        self.assertFalse(preset.vendor_facet)
        self.assertFalse(preset.personal_facet)

        preset.suffix = "different"

        self.assertEqual(preset.suffix, "different")
        self.assertEqual(preset.facet, "")

    def test_facet(self):
        """
        Tests the facet property.
        """
        preset = MimeType(("application", "its.something"))

        self.assertFalse(preset.is_empty())
        self.assertTrue(preset.is_valid())

        self.assertEqual(preset.maintype, "application")
        self.assertEqual(preset.subtype, "its.something")

        self.assertEqual(preset.suffix, "")
        self.assertEqual(preset.facet, "its")

        self.assertFalse(preset.experimental_facet)
        self.assertFalse(preset.vendor_facet)
        self.assertFalse(preset.personal_facet)

        preset.facet = MimeType.VENDOR_FACET

        self.assertEqual(preset.suffix, "")
        self.assertEqual(preset.facet, MimeType.VENDOR_FACET)

        self.assertFalse(preset.experimental_facet)
        self.assertTrue(preset.vendor_facet)
        self.assertFalse(preset.personal_facet)

        preset.facet = MimeType.EXPEREMENTAL_FACET

        self.assertEqual(preset.suffix, "")
        self.assertEqual(preset.facet, MimeType.EXPEREMENTAL_FACET)

        self.assertTrue(preset.experimental_facet)
        self.assertFalse(preset.vendor_facet)
        self.assertFalse(preset.personal_facet)

        preset.facet = MimeType.PERSONAL_FACET

        self.assertEqual(preset.suffix, "")
        self.assertEqual(preset.facet, MimeType.PERSONAL_FACET)

        self.assertFalse(preset.experimental_facet)
        self.assertFalse(preset.vendor_facet)
        self.assertTrue(preset.personal_facet)

if __name__ == "__main__":
    unittest.main()
