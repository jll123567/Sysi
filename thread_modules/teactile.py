# handles touch with two different classes. one for each point of contact and one to hold each point(node)
# Module type: def
import sys_objects


# handles touch and feel
# sensory Nodes(snsNode)
class tact:
    def __init__(self, snsNds):
        self.snsNds = snsNds

    # packs the tactile nodes into a dta
    # none
    # tact dta([snsNodes], tags)
    def package(self):
        nodeList = []
        for node in self.snsNds:
            nodeList.append(node.flatten())
        return sys_objects.data(nodeList, {"name": "tread.tact.package", "id": None, "dataType": "thread.tact.package"})


# sensory nodes
# position([float, float, float]), pressure(float), relTemp(float)
class snsNode:
    def __init__(self, position=None, pressure=0.0, relTemp=0.0):
        if position is None:
            self.position = [0.0, 0.0, 0.0]
        else:
            self.position = position
        self.pressure = pressure
        self.relTemp = relTemp

    # packs the node into a dta
    # none
    # snsNode dta([pos, pres, reTmp], tags)
    def package(self):
        return sys_objects.data(self.flatten(), {"name": "Thread.tact.snsNode.package", "id": None,
                                                 "dataType": "Thread.tact.snsNode.package"})

    # flattens the node to a list
    # none
    # [pos, pres, reTmp]
    def flatten(self):
        return [self.position, self.pressure, self.relTemp]
