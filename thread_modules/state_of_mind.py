""""""
import object


class state(object.data):
    """"""

    def __init__(self, SOMName, prs, tag=None):
        # super().__init__(tag)
        self.storage = prs
        if tag is None:
            self.tag = {"id": None, "name": None, "dataType": "SOMState", "SOMName": SOMName}
        else:
            self.tag = tag

    def rename(self, newName):
        """Change SOMName of state with currentName to newName."""
        self.tag["SOMName"] = newName

    def update(self, prs):
        self.storage = prs


class SOMManger:
    """"""

    def __init__(self, states=None, currentStateName="", previousState=None):
        if states is None:
            self.states = []
        else:
            self.states = states
        self.previousState = previousState
        self.currentStateName = currentStateName

    def addState(self, newState):
        """Add state to self.states."""
        self.states.append(newState)

    def removeState(self, stateName):
        """Remove state named stateName from self.states."""
        self.states.pop(self.resolveStateNameToIndex(stateName))

    def makeDefault(self, stateName, renameForCurrentDefault):
        """Rename the state with the name "Default" to renameForCurrentDefault and state with stateName to "Default" """
        self.states[self.resolveStateNameToIndex("Default")].rename(renameForCurrentDefault)
        self.states[self.resolveStateNameToIndex(stateName)].rename("Default")

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

def changeSOMState(self, stateName, makePreviousDefault=True):
    """"""
    import Sysh.thread_modules.state_of_mind as ___  # Shitty name to avoid conflicts in namespace

    def matchName(SOMName, SOMMInstance):
        """"""
        for tmpState in SOMMInstance.states:
            if tmpState.tag["SOMName"] == SOMName:
                return True
        return False

    SOMMangerInstance = self.trd.somm
    SOMMangerInstance.currentStateName = stateName
    if not matchName("previous", SOMMangerInstance):
        SOMMangerInstance.addState(___.state("previous", self.prs))
    else:
        SOMMangerInstance.states[SOMMangerInstance.resolveStateNameToIndex("previous")].update(self.prs)
    SOMMangerInstance.previousState = SOMMangerInstance.states[SOMMangerInstance.resolveStateNameToIndex("previous")]
    if makePreviousDefault:
        SOMMangerInstance.makeDefault("previous", "previous")
    self.prs = SOMMangerInstance.states[SOMMangerInstance.resolveStateNameToIndex("stateName")]
    self.trd.somm = SOMMangerInstance
    del ___


def saveCurrentSOMState(self):
    """"""


def revertSOMStateToDefault(self):
    """"""
