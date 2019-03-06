""""""
import object

class state(object.data):
    """"""
    def __init__(self, SOMName, prs, tag=None):
        # super().__init__(tag)
        self.storage = prs
        if tag is None:
            self.tag = {"id": None, "name": None, "dataType": "SOMState", "SOMName":SOMName}
        else:
            self.tag = tag


class SOMManger:
    """"""
    def __init__(self, states=None, currentStateName="", previousState=None):
        if states is None:
            self.states = []
        else:
            self.states = states
        if previousState is None:
            currentState = saveCurrentSOMState()
            self.previousState = currentState
            self.states.sppend(currentState)
            self.currentStateName = currentState.tag["SOMName"]
            del currentState
        else:
            self.previousState = previousState
            self.currentStateName = currentStateName

    def addState(self, state):
        """"""

    def removeState(self, name):
        """"""




def changeSOMState(self, stateName):
    """"""
def saveCurrentSOMState(self):
    """"""

def revertSOMStateToDefault(self):
    """"""
