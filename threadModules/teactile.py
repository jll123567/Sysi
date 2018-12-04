# handles touch with two different classes. one for each point of contact and one to hold each point(node)
# Module type: def
import object


# handles touch and feel
# sensory Nodes(snsNode)
class tact:
    def __init__(self, snsNds):
        self.snsNds = snsNds

    #
    #
    #
    def package(self):
        nodeList = []
        for node in self.snsNds:
            nodeList.append(node.flatten())
        return object.data(nodeList, {"name": "tread.tact.package", "id": None, "dataType": "thread.tact.package"})


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

    #
    #
    #
    def package(self):
        return object.data(self.flatten(), {"name": "tread.tact.snsNode.package", "id": None,
                                            "dataType": "thread.tact.snsNode.package"})

    #
    #
    #
    def flatten(self):
        return [self.position, self.pressure, self.relTemp]
