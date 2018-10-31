# todo: finish addapting functions


#
#
class timeline:
    def __init__(self, masterLine=0):
        self.masterLine = [masterLine]

    # creates a fork
    # lineId(int)*, parent(int)*, offset(int)*, endpoint(int)*
    # none/console output(str)
    def forkLine(self, lineId, parent, offset, endpoint):
        setattr(self, lineId, [parent, offset, endpoint])

    #
    #
    #
    def removeLine(self, lineId):
        delattr(self, lineId)

    # remove a tl
    # lineId(int)*
    # none
    def pruneTl(self, lineId):
        for i in self.tl:
            if i[0] == lineId:
                self.tl.pop(i.index())
        for i in self.scn:
            if i.scp[0][1] == lineId:
                i.unplotTl()

    # add time to the end of a tl
    # lineId(int)*, time to add(int)*
    # none
    def extendTl(self, lineId, timeToAdd):
        f = getattr(self, lineId)
        f[-1] += timeToAdd
        setattr(self, lineId, f)

    # get the total offset of a tl
    # lineId(int)*, off(int)
    # offset(int)
    # def getTotalOffsetTl(self, lineId, off=0):
    #     for i in self.tl:
    #         if i[0] == lineId:
    #             off += i[3]
    #             if i[1] == 0:
    #                 return off
    #             else:
    #                 self.getTotalOffsetTl(i[1], off)
