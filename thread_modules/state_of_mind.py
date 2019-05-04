"""Classes for the stateOfMind system."""
import sys_objects
from attribs import Personality


class state(sys_objects.data):
    """An individual state, acts as a Personality with a name encoded as a data."""
    def __init__(self, stateName, prs, tag=None):
        """
        stateName: string
        Personality: attribs.Personality
        tag: dictionary
        """
        super().__init__(prs, tag)
        if tag is None:
            self.tag = {"id": None, "name": None, "dataType": "SOMState", "stateName": stateName}
        else:
            self.tag = tag

    def rename(self, newName):
        """Change stateName of state to newName."""
        self.tag["stateName"] = newName


class SOMManger:
    """Hold and modify states."""

    def __init__(self, states=None, default=None, current=None, previous=None):
        """
        states: list
        default: attribs.Personality
        current: attribs.Personality
        previous: attribs.Personality
        """
        if states is None:
            self.states = []
        else:
            self.states = states
        if default is None:
            self.states.append(state("Default", Personality()))
        else:
            self.states.append(state("Default", default))
        if current is None:
            self.states.append(state("Current", Personality()))
        else:
            self.states.append(state("Current", current))
        if previous is None:
            self.states.append(state("Previous", Personality()))
        else:
            self.states.append(state("Previous", previous))

    @staticmethod
    def newState(stateName, personality, tag=None):
        """Return a new instance of state."""
        return state(stateName, personality, tag)

    def addState(self, stateToAdd):
        """Add state to self.states."""
        self.states.append(stateToAdd)

    def removeState(self, stateName):
        """Remove state named stateName from self.states."""
        self.states.pop(self.resolveStateNameToIndex(stateName))

    def makeDefault(self, stateName, renameForCurrentDefault):
        """Rename the state with the name "Default" to renameForCurrentDefault if possible.
            Rename state with stateName to "Default".
        """
        if self.resolveStateNameToIndex("Default") is not None:
            self.states[self.resolveStateNameToIndex("Default")].rename(renameForCurrentDefault)
        self.states[self.resolveStateNameToIndex(stateName)].rename("Default")

    def makePrevious(self, stateName, renameForPrevious):
        """Rename the state with the name "Previous" to renameForPrevious if possible.
            Rename state with stateName to "Previous".
        """
        if self.resolveStateNameToIndex("Previous") is not None:
            self.states[self.resolveStateNameToIndex("Previous")].rename(renameForPrevious)
        self.states[self.resolveStateNameToIndex(stateName)].rename("Previous")

    def makeCurrent(self, stateName):
        """Rename the state with the name "Current" to "Previous" and state with stateName to "Current".
            Create Previous if it doesn't exist
            Don't change Previous is Current doesn't exist.
        """
        if self.resolveStateNameToIndex("Previous") is not None:
            if self.resolveStateNameToIndex("Current") is not None:
                self.states[self.resolveStateNameToIndex("Previous")].\
                    update(self.states[self.resolveStateNameToIndex("Current")].storage)
        else:
            if self.resolveStateNameToIndex("Current") is not None:
                self.addState(state("Previous", self.states[self.resolveStateNameToIndex("Current")].storage))
        self.states[self.resolveStateNameToIndex(stateName)].rename("Current")

    def resolveStateNameToIndex(self, stateName):
        """Find and return the index of the state with the stateName stateName."""
        idx = 0
        for stateInstance in self.states:
            if stateInstance.tag["stateName"] == stateName:
                break
            idx += 1
        if idx == self.states.__len__():
            return None
        return idx


class SOMObject(sys_objects.user):

    def __init__(self, mod=None, trd=None, prs=None, mem=None, tag=None):
        """
        mod: attribs.SysObject or attribs.FileObject
        trd: attribs.Thread
        prs: attribs.Personality
        mem: attribs.UsrMemory
        tag: dictionary
        """
        super().__init__(mod, trd, prs, mem, tag)

    def changeSOMState(self, stateName, makePreviousDefault=True):
        """Change the current state of the StateOfMindManager and update the Personality."""
        SOMManagerInstance = self.trd.somm
        if not self.matchName("Previous", SOMManagerInstance):
            SOMManagerInstance.addState(SOMManagerInstance.newState("Previous", self.prs))
        else:
            SOMManagerInstance.states[SOMManagerInstance.resolveStateNameToIndex("Previous")].update(self.prs)
        if makePreviousDefault:
            SOMManagerInstance.makeDefault("Previous", "previousDefault")
        self.prs = SOMManagerInstance.states[SOMManagerInstance.resolveStateNameToIndex(stateName)].storage
        if not self.matchName("Current", SOMManagerInstance):
            SOMManagerInstance.addState(SOMManagerInstance.newState("Current", self.prs))
        else:
            SOMManagerInstance.states[SOMManagerInstance.resolveStateNameToIndex("Current")].update(self.prs)
        self.trd.somm = SOMManagerInstance

    def saveCurrentSOMState(self):
        """Save the current Personality in the "Current" state or add it as "Current" if "Current" doesn't exist."""
        if self.matchName("Current", self.trd.somm):
            self.trd.somm.states[self.trd.somm.resolveStateNameToIndex("Current")].update(self.prs)
        else:
            self.trd.somm.addState(self.trd.somm.newState("Current", self.prs))

    def revertSOMStateToDefault(self):
        """Set the Personality to the "Default" state."""
        self.prs = self.trd.somm.states[self.trd.somm.resolveStateNameToIndex("Default")].storage
        self.trd.somm.makeCurrent("Default")

    def revertSOMStateToPrevious(self):
        """Set the Personality to the "Default" state."""
        self.prs = self.trd.somm.states[self.trd.somm.resolveStateNameToIndex("Previous")].storage
        self.trd.somm.makeCurrent("Previous")

    @staticmethod
    def matchName(stateName, SOMMInstance):
        """
        See if stateName is in any state in SOMInstance.
        Return True if there is a match.
        Return False otherwise.
        """
        for tmpState in SOMMInstance.states:
            if tmpState.tag["stateName"] == stateName:
                return True
        return False
