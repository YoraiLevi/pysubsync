import copy
import numpy
from scipy import stats
import pysubs2
from pysubs2.time import make_time
from .SchemeForm import SchemeForm
from .SignalForm import SignalForm
from .helpers import unpackTupleList, packList2Tuple

import matplotlib.pyplot as plt


class Subtitles(pysubs2.ssafile.SSAFile):
    """Class to represent subtitle file"""
    def shiftFrom(self, startTime, h=0, m=0, s=0, ms=0, frames=None, fps=None):
        """Shifts all subtitles from startTime(in ms) by the given time/fps"""
        delta = make_time(h=h, m=m, s=s, ms=ms, frames=frames, fps=fps)
        for ev in self:
            if(ev.start >= startTime):
                ev.start += delta
                ev.end += delta

    def runTime(self):
        """calculates the start and end time of the subtitles"""
        start = min([ev.start for ev in self]+[0])
        end = max(ev.end for ev in self)
        return start, end

    def _schemes(self):
        """Creates 'SchemeForm' representation of on times and off times of events the subtitle events
        """
        def createTimeStamps():
            stamps = []
            for ev in self:
                stamps.append((ev.start, ev.end))
            return stamps

        stamps = createTimeStamps()
        start, end = self.runTime()
        onScheme = SchemeForm(stamps, start, end)
        offScheme = onScheme.invert()
        return onScheme, offScheme

    def _signals(self, precision=1):
        """Creates 'SignalForm' representation of subtitles"""
        onScheme, offScheme = self._schemes()
        onSignal = SignalForm.fromScheme(onScheme, precision=precision)
        offSignal = SignalForm.fromScheme(offScheme, precision=precision)
        return onSignal, offSignal

    def _anomalies(self, harshness):
        """Searches for periods of time where anomalies may occure
        Anomalies are periods of time with uncommon, rare where nothing seem to happen(silence or sound)"""
        def findAnomalies(scheme):
            def deltaT(scheme):
                return [stamps[1]-stamps[0] for stamps in scheme.stamps]
            anomalies = []
            samples = deltaT(scheme)
            for i in numpy.where((stats.zscore(samples) > harshness) == True)[0]:
                anomalies.append(scheme.stamps[i])
            return anomalies
        onScheme, offScheme = self._schemes()
        return findAnomalies(onScheme), findAnomalies(offScheme)

    def sync(self, goldSubtitles, precision=100, harshness=4):
        """Attempts to syncronize these subtitles to the goldSubtitle timings
            tries to finds more oddities throughout the run time 

        Parameters
        ----------
        goldSubtitles : Subtitles
            the subtitle file to sync based on
        precision : int, optional
            decides the number of samples to be used in processing. 1 is maximum number of samples to be used (default is 100)
        harshness : float, optional
            value by which to determine if there are more unsyncronized portions throughout the run time of the subtitles

        Returns
        -------
        void
        """
        OnAnomalies, OffAnomalies = self._anomalies(harshness=harshness)
        tStart, Tend = self.runTime()
        sumShift = 0
        for AnomalyBegin, AnomalyEnd in OffAnomalies:
            start, end = AnomalyBegin-sumShift, Tend-sumShift
            trimmedSubtitles = Subtitles.trimmed(self, start, end)
            onShift, offShift = Subtitles.calculatePhaseShift(
                goldSubtitles, trimmedSubtitles, precision=precision)
            sumShift += onShift
            self.shiftFrom(start, ms=-onShift)

    def _oldsync(self, goldSubtitles, precision=100):
        """Attempts to syncronize these subtitles to the goldSubtitle timings

        Parameters
        ----------
        goldSubtitles : Subtitles
            the subtitle file to sync based on
        precision : int, optional
            decides the number of samples to be used in processing. 1 is maximum number of samples to be used (default is 100)

        Returns
        -------
        void
        """
        onShift, offShift = Subtitles.calculatePhaseShift(
            goldSubtitles, self, precision=precision)
        self.shift(ms=-onShift)

    @classmethod
    def trimmed(cls, subtitles, start, end):
        """Cuts a portion of 'subtitles'

        Parameters
        ----------
        subtitles : Subtitles
            the Subtitles to cut from
        start : float
            the start time of the interval
        end : float
            the end time of the interval

        Returns
        -------
        Subtitles
            a Subtitle object trimmed from start to end, without external portions
        """
        copySubs = copy.deepcopy(subtitles)
        copySubs.events = [ev for ev in copySubs if not (
            end < ev.start or start > ev.end)]
        for ev in copySubs:
            if not (end < ev.start or start > ev.end):
                ev.start = max(start, ev.start)
                ev.end = min(end, ev.end)
        return copySubs

    @staticmethod
    def calculatePhaseShift(subtitlesA, subtitlesB, precision=100):
        """Calculates the time delay between SubtitleB and SubtitleA

        Parameters
        ----------
        subtitlesA : Subtitles
            A subtitle file to compare against
        subtitlesB : Subtitles
            A subtitle file to compare
        precision : int, optional
            decides the number of samples to be used in processing. 1 is maximum number of samples to be used (default is 100)

        Returns
        -------
        tuple(int, int)
            the time delay between SubtitleB compared to SubtitleA for when they're vising and not
        """
        onA, offA = subtitlesA._signals(precision)
        onB, offB = subtitlesB._signals(precision)
        onShift = SignalForm.phaseShift(onA, onB)
        offShift = SignalForm.phaseShift(offA, offB)
        return onShift, offShift


load = Subtitles.load
