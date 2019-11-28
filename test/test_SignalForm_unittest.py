import unittest
import numpy
from pysubsync.SignalForm import SignalForm
from pysubsync.SchemeForm import SchemeForm
from .Stamps import STAMPS, SIMPLIFIED_STAMPS, TRIMMED_STAMPS, INVERTED_STAMPS, INVERTE_DEXTENDED_STAMPS


class TestSum(unittest.TestCase):
    def test_phaseShift(self):
        """tests if the phaseshift algorithm works
        """
        sig = numpy.ones(20).astype(bool)
        shifted_sig = numpy.insert(numpy.zeros(50), 50, sig)
        SigA = SignalForm(sig)
        SigB = SignalForm(shifted_sig)
        self.assertEqual(SignalForm.phaseShift(SigA, SigB), 50)


if __name__ == '__main__':
    unittest.main()
