"""Classes for the stateOfMind system"""
import object


class state(object.data):
    """an individual state,
    acts as a prs with a name encoded as a data
    """
    def __init__(self, stateName, prs, tag=None):
        super().__init__(tag)
        self.storage = prs
        if tag is None:
            self.tag = {"id": None, "name": None, "dataType": "SOMState", "stateName": stateName}
        else:
            self.tag = tag

    def rename(self, newName):
        """Change stateName of state with currentName to newName."""
        self.tag["stateName"] = newName


class SOMManger:
    """holder of states to be referenced from the thread"""

    def __init__(self, states=None):
        if states is None:
            self.states = []
        else:
            self.states = states

    @staticmethod
    def newState(stateName, prs, tag=None):
        """return a new instance of state"""
        return state(stateName, prs, tag)

    def addState(self, stateToAdd):
        """Add state to self.states."""
        self.states.append(stateToAdd)

    def removeState(self, stateName):
        """Remove state named stateName from self.states."""
        self.states.pop(self.resolveStateNameToIndex(stateName))

    def makeDefault(self, stateName, renameForCurrentDefault):
        """Rename the state with the name "Default" to renameForCurrentDefault and state with stateName to "Default" """
        self.states[self.resolveStateNameToIndex("Default")].rename(renameForCurrentDefault)
        self.states[self.resolveStateNameToIndex(stateName)].rename("Default")

    def makePrevious(self, stateName, renameForPrevious):
        """Rename the state with the name "Previous" to renameForPrevious and state with stateName to "Previous" """
        self.states[self.resolveStateNameToIndex("Previous")].rename(renameForPrevious)
        self.states[self.resolveStateNameToIndex(stateName)].rename("Previous")

    def makeCurrent(self, stateName):
        """Rename the state with the name "Current" to renameForCurrent and state with stateName to "Current" """
        self.states[self.resolveStateNameToIndex("Previous")].\
            update(self.states[self.resolveStateNameToIndex("Current")].storage)
        self.states[self.resolveStateNameToIndex(stateName)].rename("Current")

    def resolveStateNameToIndex(self, stateName):
        """find and return the index of the state with the stateName stateName"""
        idx = 0
        for stateInstance in self.states:
            if stateInstance.tag["stateName"] == stateName:
                break
            idx += 1
        return idx


# ADD THESE FUNCTIONS TO YOUR OBJECT
# THEY MUST BE BOUND METHODS
# Todo: explain type binding

def changeSOMState(self, stateName, makePreviousDefault=True):
    """change the current state of the StateOfMindManager and update the prs"""
    SOMMangerInstance = self.trd.somm
    SOMMangerInstance.currentStateName = stateName
    if not matchName("Previous", SOMMangerInstance):
        SOMMangerInstance.addState(SOMMangerInstance.newState("Previous", self.prs))
    else:
        SOMMangerInstance.states[SOMMangerInstance.resolveStateNameToIndex("Previous")].update(self.prs)
    if makePreviousDefault:
        SOMMangerInstance.makeDefault("Previous", "previousDefault")
    self.prs = SOMMangerInstance.states[SOMMangerInstance.resolveStateNameToIndex("stateName")]
    if not matchName("Current", SOMMangerInstance):
        SOMMangerInstance.addState(SOMMangerInstance.newState("Current", self.prs))
    else:
        SOMMangerInstance.states[SOMMangerInstance.resolveStateNameToIndex("Current")].update(self.prs)
    self.trd.somm = SOMMangerInstance


def saveCurrentSOMState(self):
    """save the current prs in the "Current" state """
    if matchName("Current", self.trd.somm):
        self.trd.somm.states[self.trd.somm.resolveStateNameToIndex("previous")].update(self.prs)
    else:
        self.trd.somm.addState(self.trd.somm.newState("Current", self.prs))


def revertSOMStateToDefault(self):
    """set the prs to the "Default" state"""
    self.prs = self.somm[self.somm.resolveStateNameToIndex("Default")]
    self.trd.somm.makeCurrent("Default")


def revertSOMStateToPrevious(self):
    """set the prs to the "Default" state"""
    self.prs = self.somm[self.somm.resolveStateNameToIndex("Previous")]
    self.trd.somm.makeCurrent("Previous")


def matchName(stateName, SOMMInstance):
    """return True if  stateName is in any state in SOMInstance
    return False otherwise
    """
    for tmpState in SOMMInstance.states:
        if tmpState.tag["stateName"] == stateName:
            return True
    return False
