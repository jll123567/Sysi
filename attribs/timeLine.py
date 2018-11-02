# Timeline management
# module type: attrib


# defines a timeline
# master([int]), line([str, int, int], ...)
# input
#   masterLine(int)
class timeline:
    def __init__(self, masterLine=0):
        self.master = [masterLine]

    # creates a fork
    # lineId(int)*, parent(int)*, offset(int)*, endpoint(int)*
    # none/console output(str)
    def forkLine(self, lineId, parent, offset, endpoint):
        setattr(self, lineId, [parent, offset, endpoint])

    # remove a line
    # lineId(str)
    # none/ console output(str)
    def removeLine(self, lineId):
        if lineId is not "master":
            delattr(self, lineId)
        else:
            print("you cannot remove master")

    # add time to the end of a tl
    # lineId(int)*, time to add(int)*
    # none
    def extendTl(self, lineId, timeToAdd):
        newTime = getattr(self, lineId)
        newTime[-1] += timeToAdd
        setattr(self, lineId, newTime)

    # get the total offset of a tl
    # lineId(int)*, off(int)
    # offset(int)
    def getTotalOffsetTl(self, lineId, off=0):
        for line in dir(self):
            if line == lineId:
                if line == "master":
                    return off
                else:
                    off += getattr(self, line)[1]
                    return self.getTotalOffsetTl(getattr(self, line)[0], off)


# remove all timeline data in a universe
#   btw uni.tl will be set to None not timeline()
# uni(uni)
# formatted uni(uni)
def fullTlRemoval(uni):
    for idx in uni.scn.__len__():
        uni.scn[idx].unPlotTl()
    uni.tl = None
    return uni


# info at run
if __name__ == "__main__":
    print("Timeline management\nmodule type: attrib")
