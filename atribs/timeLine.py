# todo: finish addapting functions


#
#
class timeline:
    def __init__(self, masterLine=0):
        self.master = [masterLine]

    # creates a fork
    # lineId(int)*, parent(int)*, offset(int)*, endpoint(int)*
    # none/console output(str)
    def forkLine(self, lineId, parent, offset, endpoint):
        setattr(self, lineId, [parent, offset, endpoint])

    #
    #
    #
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
                off += getattr(self, line)[1]
                if getattr(self, line)[0] == "master":
                    return off
                else:
                    self.getTotalOffsetTl(line[0], off)


f = timeline(200)
