from .helpers import unpackTupleList,packList2Tuple
class SchemeForm():
    """A helper class for managing events' time stamps"""        
    def __init__(self, stamps, tStart=0, tEnd=0, trim=True, simplify=True):
        """[summary]

        Parameters
        ----------
        stamps : list[tuple(int,int)]
            a list of tuple(int,int) each representing an event from tuple[0] to tuple[1]
        tStart : int, optional
            start time of the interval, by default 0
        tEnd : float, optional
            end time of the interval, by default 0
        trim : bool, optional
            A flag, decides if to trimp excess events out of the given time interval, by default True
        simplify : bool, optional
            A flag, decides of to reduce zero length events and merge overlapping ones, by default True
        """
        self.tStart = tStart
        self.tEnd = tEnd if tEnd else max(
            [stamp[1] for stamp in stamps]+[tStart])
        self.stamps = sorted(stamps, key=lambda x: x[0])
        if trim:
            self._trim()
        if simplify:
            self._simplify()

    def _simplify(self):
        """Removes 0 length events and merges overlapping ones
        """                                
        #reduce 0 length events
        self.stamps = list(filter(lambda x: x[1]-x[0] != 0, self.stamps))
        simplified = []
        i = 0
        while(i < len(self.stamps)):
            start = self.stamps[i][0]
            end = self.stamps[i][1]
            if(i < len(self.stamps)-1 and self.stamps[i+1][0] > end):
                #if the next event is not overlapping
                i += 1
            else:
                #if the next event is overlapping
                markedEnd = end
                offset = 1
                while(i+offset < len(self.stamps) and self.stamps[i+offset][0] <= markedEnd):
                    #is the next event also overlaps? merge EVERYTHING!
                    end = max(end, self.stamps[i+offset][1])
                    offset += 1
                i += offset
            #finally add the simplified event
            simplified.append((start, end))
        self.stamps = simplified

    def _trim(self):
        """trims events outside the intervals away
        """        
        trimmed = []
        for start, end in self.stamps:
            if not (end < self.tStart or start > self.tEnd):
                trimmed.append((max(start, self.tStart), min(end, self.tEnd)))
        self.stamps = trimmed

    def invert(self):
        """Provides the 'negative' of the events in the given time interval
        
        Returns
        -------
        SchemeForm
            A negative form of SchemeForm instance
        """        
        templst = [self.tStart]+unpackTupleList(self.stamps)+[self.tEnd]
        invertedStamps = packList2Tuple(templst)
        return SchemeForm(stamps=invertedStamps, tStart=self.tStart, tEnd=self.tEnd)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.tStart == other.tStart \
                and self.tEnd == other.tEnd \
                and self.stamps == other.stamps
        return False

    def __repr__(self):
        return "<{type} Tstart={tStart},Tend={tEnd},deltaT={deltaT} with {lenstamps} stamps>".format(type=type(self), tStart=self.tStart, tEnd=self.tEnd, deltaT=self.tEnd-self.tStart, lenstamps=len(self.stamps), stamps=self.stamps)
