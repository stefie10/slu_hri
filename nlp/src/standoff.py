
class TextStandoff:
    def __init__(self, text, range):
        self.entireText = text

        self.range = range
        
    def asPrimitives(self):
        return (self.entireText, self.range)
    
    @staticmethod
    def fromPrimitives(args):
        return TextStandoff(*args)
        
    def isNull(self):
        return self.range == (0, 0)
    
    @property
    def text(self):
        start, end = self.range
        return self.entireText[start:end]
    @property
    def length(self):
        start, end = self.range
        return end - start
    @property
    def end(self):
        start, end = self.range
        return end
    @property
    def start(self):
        start, end = self.range
        return start

    def overlaps(self, standoff):
        if self.start < standoff.end and standoff.start < self.end:
            return True
        else:
            return False
    def contains(self, standoff):
        start, end = standoff
        return self.start <= start and self.end >= end
    def before(self, standoff):
        if self.end <= standoff.start:
            return True
        else:
            return False
    def degreeOfOverlap(self, standoff):
        """
        Returns the size of the overlapping range of two tags. Returns
        zero if they do not overlap.
        """
        start, end = standoff
        if self.overlaps(standoff):
            return min(end, self.end) - max(start, self.start)
        else:
            return 0

    def __iter__(self):
        return iter((self.start, self.end))
    def toXml(self, standoff):
        standoff.setAttribute("start", str(self.start))
        standoff.setAttribute("end", str(self.end))

    

class Standoff(TextStandoff):
    def isNull(self):
        return self.range == (0, 0)

    def __init__(self, session, instructionIdx, range):
        self.session = session
        self.instructionIdx = instructionIdx
        self.range = range
        self.entireText = self.session.routeInstructions[self.instructionIdx]

