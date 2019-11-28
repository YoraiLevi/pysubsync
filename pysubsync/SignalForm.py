import numpy
from .SchemeForm import SchemeForm


class SignalForm():
    """SignalForm represents a wave form of an input signal"""
    def __init__(self, signal, start=0, end=0, precision=1):
        """Init
        Parameters
        ----------
        signal : numpy.array
            a container that stores the sample values of the signal at equal time deltas. Must be numpy compatible
        start : int, optional
            start time, by default 0
        end : int, optional
            end time, by default 0
        precision : int, optional
            the number of samples each sample represents, by default 1
        """
        self._signal = signal
        self.start = start
        self.end = end
        self.precision = precision

    @classmethod
    def fromScheme(cls, scheme, precision=1):
        """Creates a corresponding SignalForm from a SchemeForm instance

        Parameters
        ----------
        scheme : SchemeForm
            A scheme to generate the signal from
        precision : int, optional
            the number of samples each sample represents, by default 1

        Returns
        -------
        SignalForm
            A signal corrsponding to the given scheme
        """
        tStart = scheme.tStart
        tEnd = scheme.tEnd
        deltaT = tEnd-tStart
        samples = int((deltaT+1)/precision)
        t = numpy.linspace(tStart, tEnd, samples, endpoint=True)
        signal = numpy.zeros(samples, dtype=bool)
        for start, end in scheme.stamps:
            signal = numpy.logical_or(
                signal, numpy.logical_and(start <= t, t <= end))
        return cls(signal, tStart, tEnd, precision)

    @classmethod
    def phaseShift(cls, signalA, signalB):
        """calculates the phase shift between 2 signals

        Parameters
        ----------
        signalA : SignalForm
        signalB : SignalForm

        Returns
        -------
        float
            phase shift of signalB compared to SignalA
        """
        if signalA.precision == signalB.precision:
            precision = signalB.precision
            correlation = numpy.correlate(signalB._signal.astype(
                int), signalA._signal.astype(int), 'full')
            peakIndex = numpy.argmax(correlation)
            shift = peakIndex+1-signalA._signal.size
            return shift*precision
        raise "prescition mismatch"
