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
        """Add state to self.states."""
        self.states.append(state)

    def removeState(self, stateName):
        """Remove state named stateName from self.states."""
        self.states.pop(self.resolveStateNameToIndex(stateName))

    def renameState(self, currentName, newName):
        """Change SOMName of state with currentName to newName."""
        self.states[self.resolveStateNameToIndex(currentName)].tag["SOMName"] = newName

    def makeDefault(self, stateName, renameForCurrentDefault):
        """Rename the state with the name "Default" to renameForCurrentDefault and state with stateName to "Default" """
        self.renameState("Default", renameForCurrentDefault)
        self.renameState(stateName, "Default")

    def resolveStateNameToIndex(self, stateName):
        """find and return the index of the state with the SOMName stateName"""
        idx = 0
        for state in self.states:
            if state.tag["SOMName"] == stateName:
                break
            idx += 1
        return idx


# ADD THESE FUNCTIONS TO YOUR OBJECT
# THEY MUST BE BOUND METHODS

def changeSOMState(self, stateName):
    """"""
def saveCurrentSOMState(self):
    """"""

def revertSOMStateToDefault(self):
    """"""
