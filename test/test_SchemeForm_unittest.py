import unittest
from pysubsync.SchemeForm import SchemeForm
from .Stamps import STAMPS, SIMPLIFIED_STAMPS, TRIMMED_STAMPS, INVERTED_STAMPS, INVERTE_DEXTENDED_STAMPS


class TestSchemeForm(unittest.TestCase):
    def test_simplify(self):
        for key, stamps in STAMPS.items():
            scheme = SchemeForm(stamps, trim=False, simplify=True)
            self.assertEqual(SIMPLIFIED_STAMPS[key], scheme.stamps)

    def test_trim(self):
        for key, stamps in STAMPS.items():
            scheme = SchemeForm(stamps, 2, 22, trim=True, simplify=True)
            self.assertEqual(TRIMMED_STAMPS[key], scheme.stamps)

    def test_invert(self):
        for key, stamps in STAMPS.items():
            scheme = SchemeForm(stamps)
            self.assertEqual(INVERTED_STAMPS[key], scheme.invert().stamps)

    def test_invertExtendedPeriod(self):
        for key, stamps in STAMPS.items():
            scheme = SchemeForm(stamps, tEnd=50)
            self.assertEqual(
                INVERTE_DEXTENDED_STAMPS[key], scheme.invert().stamps)

    def test_invertTwice(self):
        """checks if (x^-1)^-1 == x for schemeForm"""
        for key, stamps in STAMPS.items():
            scheme = SchemeForm(stamps)
            self.assertEqual(
                SIMPLIFIED_STAMPS[key], scheme.invert().invert().stamps)

    def test_invertTwiceExtendedPeriod(self):
        """checks if (x^-1)^-1 == x for schemeForm"""
        for key, stamps in STAMPS.items():
            scheme = SchemeForm(stamps, tEnd=50)
            self.assertEqual(
                SIMPLIFIED_STAMPS[key], scheme.invert().invert().stamps)

    def test_invertedStamp(self):
        for key, stamps in INVERTED_STAMPS.items():
            scheme = SchemeForm(stamps)
            self.assertEqual(scheme.stamps, stamps)

    def test_invertedExtendedStamp(self):
        for key, stamps in INVERTE_DEXTENDED_STAMPS.items():
            scheme = SchemeForm(stamps)
            self.assertEqual(scheme.stamps, INVERTE_DEXTENDED_STAMPS[key])


if __name__ == '__main__':
    unittest.main()
