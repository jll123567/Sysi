"""Timeline definition"""
# TODO: cleanup this mess of a tl system
# reason: object attributes should not be added and dropped on a per instance basis
# suggested solution: use a dictionary


class timeline:
    """Structure for defining the order of scenes.
        Each attribute of a timeline(tl) is a line.
        Each line has a lineName(its name) a parent an offset off of that parent and a length.
        Master is an exception, it only has a length.
    """
    def __init__(self, masterLineLength=0):
        """MasterLineLength: int"""
        self.master = [masterLineLength]

    def forkLine(self, lineName, parent, offset, length):
        """Create a new line with the following parameters."""
        setattr(self, lineName, [parent, offset, length])

    def removeLine(self, lineName):
        """Remove the line with the Name <lineName>."""
        if lineName is not "master":
            delattr(self, lineName)
        else:
            print("you cannot remove master")

    def extendTl(self, lineName, timeToAdd):
        """Extend the length of the line <lineName> with <timeToAdd>."""
        newTime = getattr(self, lineName)
        newTime[-1] += timeToAdd
        setattr(self, lineName, newTime)

    # get the total offset of a tl
    # lineName(int)*, off(int)
    # offset(int)
    def getTotalOffsetTl(self, lineName, off=0):
        """Recursively get and return the total offset of <lineName> from master.
            Try not to touch <off>.
        """
        for line in dir(self):
            if line == lineName:
                if line == "master":
                    return off
                else:
                    off += getattr(self, line)[1]
                    return self.getTotalOffsetTl(getattr(self, line)[0], off)


def fullTlRemoval(uni):
    """Remove all timeline data in a universe.
        Returns the modified universe.
    """
    for idx in uni.scn.__len__():
        uni.scn[idx].unPlotTl()
    uni.tl = None
    return uni
