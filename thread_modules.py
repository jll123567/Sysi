""""""
import sys_objects
import prog.idGen
from attribs import Personality
import time


class cpx:
    """Arbitrary resolution."""

    def __init__(self, problems=None, solutions=None):
        """
        :param problems: list
        :param solutions: list
        """
        if problems is None:
            self.problems = []
        else:
            self.problems = problems
        if solutions is None:
            self.solutions = []
        else:
            self.solutions = solutions

    def newProblem(self, problem):
        """Create a new unsolved problem."""
        self.problems.append(problem)
        self.solutions.append(None)

    def postSolution(self, solution, problemIndex=0):
        """Add a solution to a problem."""
        self.solutions.insert(problemIndex, solution)

    def package(self):
        """Pack data for ram."""
        return sys_objects.data([self.problems, self.solutions], {"name": "Thread.cpx.package", "id": None,
                                                                  "dataType": "Thread.cpx.package"})


class audioStereo:
    """Hold stereo audio."""

    def __init__(self, left=None, right=None):
        """
        :param left: list
        :param right: list
        """
        if left is None:
            self.left = []
        else:
            self.left = left
        if right is None:
            self.right = []
        else:
            self.right = right


class audioMono:
    """Hold mono audio."""

    def __init__(self, sound=None):
        """
        :param sound: list
        """
        if sound is None:
            self.sound = []
        else:
            self.sound = sound


class lang:
    """Hold and manipulate audio."""

    def __init__(self, heard=audioStereo(), speakQue=audioMono()):
        """
        :param heard: AudioStereo
        :param speakQue: AudioMono
        """
        self.heard = heard
        self.speakQue = speakQue

    def listen(self, inputSource):
        """Get sound from input and append it to heard."""
        self.heard.left.append(inputSource.l)
        self.heard.right.append(inputSource.r)

    def tune(self, minVolume, minPan, maxPan):
        """
        Check if audio is above a minimum volume or within a pan range and if its not cut it.

        Min volume is in Db.
        pan is a float range from -1.0 to 1.0.
        minPan is the smallest pan value.
        maxPan is the largest pan value.
        """

        for i in self.heard.left:
            if abs(i) < minVolume:
                self.heard.left[self.heard.left.index(i)] = 0
            elif minPan > 0:
                self.heard.left[self.heard.left.index(i)] = 0
            elif abs(i) > minPan * -100:
                self.heard.left[self.heard.left.index(i)] = 0
            else:
                continue

        for i in self.heard.right:
            if abs(i) < minVolume:
                self.heard.right[self.heard.right.index(i)] = 0
            elif maxPan < 0:
                self.heard.right[self.heard.right.index(i)] = 0
            elif abs(i) < maxPan * 100:
                self.heard.right[self.heard.right.index(i)] = 0
            else:
                continue

    def silence(self):
        """Clear spoken audio."""
        self.speakQue = []

    def queueSpeak(self, sounds):
        """Add sounds to the speaking queue."""
        self.speakQue = sounds

    def package(self):
        """Pack audio data into a data obj and return it."""
        return sys_objects.data([self.heard, self.speakQue], {"name": "Thread.lang.package", "id": None,
                                                              "dataType": "Thread.lang.package"})


class mov:
    """holds sysObject position, acceleration and rotation"""

    def __init__(self, x=0, y=0, z=0, vx=0, vy=0, vz=0, rx=0, ry=0, rz=0, rvx=0, rvy=0, rvz=0):
        """
        initialize attributes

        x: x position
        y: y position
        z: z position
        vx: x velocity
        vy: y velocity
        vz: z velocity
        rx: pitch
        ry: yaw
        rz: roll
        rvx: pitch velocity
        rvy: yaw velocity
        rvz: roll velocity
        """
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.rvx = rvx
        self.rvy = rvy
        self.rvz = rvz

    def warp(self, x, y, z):
        """set position"""
        self.x = x
        self.y = y
        self.z = z

    def setRotation(self, rx, ry, rz):
        """set rotation(degrees)"""
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def accelerate(self, vx, vy, vz):
        """set acceleration"""
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def accelerateRotation(self, rvx, rvy, rvz):
        """set rotation acceleration"""
        self.rvx = rvx
        self.rvy = rvy
        self.rvz = rvz

    def move(self):
        """change position and rotation based on acceleration"""
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.rx += self.rvx
        self.ry += self.rvy
        self.rz += self.rvz

    def attract(self, o1, force):
        """changes position based on another sysObject's position and a force

        o1 needs to be a Thread.mov not an sysObject.sysObject
        attract pusses together"""
        if self.x > o1.x:
            self.vx = (force * -1)
        elif self.x < o1.x:
            self.vx = force
        else:
            self.vx = 0
        if self.y > o1.y:
            self.vy = (force * -1)
        elif self.y < o1.y:
            self.vy = force
        else:
            self.vy = 0
        if self.z > o1.z:
            self.vz = (force * -1)
        elif self.z < o1.z:
            self.vz = force
        else:
            self.vz = 0
        self.move()

    def repel(self, o1, force):
        """changes position based on another sysObject's position and a force

        o1 needs to be a Thread.mov not an sysObject.sysObject
        repel pushes away"""
        if self.x > o1.x:
            self.vx = force
        elif self.x < o1.x:
            self.vx = force * -1
        else:
            self.vx = 0
        if self.y > o1.y:
            self.vy = force
        elif self.y < o1.y:
            self.vy = force * -1
        else:
            self.vy = 0
        if self.z > o1.z:
            self.vz = force
        elif self.z < o1.z:
            self.vz = force * -1
        else:
            self.vz = 0
        self.move()

    def package(self):
        """pack attributes into a data sysObject and return it"""
        return sys_objects.data([self.x, self.y, self.z, self.vx, self.vy, self.vz, self.rx,
                                 self.ry, self.rz, self.rvx, self.rvy, self.rvz],
                                {"name": "Thread.mov.package", "id": None, "dataType": "Thread.mov.package"})


class olf:
    """Hold olfactory input for thread.
    descriptor is a string
    strength is a float between and including 0 and 1"""

    def __init__(self, descriptor="None", strength=0):
        """Initialize attributes
        descriptor:"None"
        strength:0"""
        self.descriptor = descriptor
        self.strength = strength

    def package(self):
        """Pack olf data into a data sysObject(it needs an id) and return it."""
        return sys_objects.data([self.descriptor, self.strength], {"name": "Thread.olf.package", "id": None,
                                                                   "dataType": "Thread.olf.package"})


# thread module queue
# tasks([])
class que:
    def __init__(self, tasks=None):
        if tasks is None:
            self.tasks = []
        else:
            self.tasks = tasks

    # empty queue
    # none
    # none
    def close(self):
        self.tasks = []

    # insert a task at an index
    # task(task(str)*, index(int)
    # none
    def interrupt(self, task, index=0):
        self.tasks.insert(index, task)

    # complete a ask
    # index(int)
    # none
    def complete(self, index=None):
        if index is None:
            self.tasks.pop(0)
        else:
            self.tasks.pop(index)

    # show that tasks in the queue
    # none
    # console output(str)
    def showTask(self):
        # iterates through that thatThingThat'sAListOfThings and recursively adds indents
        # thatThingThat'sAListOfThings([])*, indent(int)*
        # console output(str)
        # noinspection SpellCheckingInspection
        def recurse(thatThingThatsAListOfThings, indent):
            if isinstance(thatThingThatsAListOfThings, list):
                recurse(thatThingThatsAListOfThings, indent + 1)
            else:
                if i[0] == "e":
                    print("  " * indent, "exact:", thatThingThatsAListOfThings)
                elif i[0] == "i":
                    print("  " * indent, "inexact:", thatThingThatsAListOfThings)
                else:
                    print("Not a valid task type")

        for i in self.tasks:
            recurse(i, 0)


# make exact exact tasks into a valid tsk profile(broken at the moment)
# queue(Thread.queue)*
# tsk profile(Thread.tsk)
def makeValidTskProfile(queue):
    if isinstance(queue, que):
        tasks = queue.tasks
    else:
        tasks = queue
    # flatten function by rightfootin
    # snippet link: https://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
    #   modified to not include nested tuples as queues only support lists (or at least they're supposed to)
    mainTask = []
    for item in tasks:
        if isinstance(item, list):
            mainTask.extend(makeValidTskProfile(item))
        else:
            mainTask.append(item)
    return mainTask


class ram:
    """holds random data the thread needs to store temporarily
    storage is a list that holds any"""

    def __init__(self, storage=None):
        """Initialize attributes
        Storage:[]"""
        if storage is None:
            self.storage = []
        else:
            self.storage = storage

    def load(self, dta):
        """put dta into self.storage"""
        self.storage.append(dta)

    def loadTrdDta(self, dta):
        """generate a generic id for dta and load() it"""
        dta.tag["id"] = prog.idGen.generateGenericId(self.storage, dta)
        self.load(dta)

    def read(self):
        """print the contents of self.storage to the console"""
        for i in self.storage:
            print(i)

    def search(self, query):
        """searched self.storage for query
        returns the index if the sysObject in storage and query are equal
        prints a message to the console if nothing was found"""
        matched = True
        idx = 0
        for i in self.storage:
            if i == query:
                return idx
            idx += 1
        if not matched:
            print("no results. try obj.trd.ram.read()")

    def free(self, index):
        """removes an sysObject from self.storage(with *style*)

        index(int) is the int-th item in self.storage
        index(None) removes the last (or -1st) item in ram
        index("all") sets ram to []
        index(else) print error to console"""
        if index is None:
            self.storage.pop(-1)
        elif index == "all":
            self.storage = []
        elif isinstance(index, int):
            self.storage.pop(index)
        else:
            print("invalid request")


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
                self.states[self.resolveStateNameToIndex("Previous")]. \
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


# objects can be like groups without being groups
# parent and child objects have a "sub" section in their thread_modules

# "sub": {"parent": [reference, offset], "children": [reference, ...]}

# reference:objId
# offset: is the distance of the  parent's position to the sysObject's position in the format [x,y,z]
# if an sysObject has one child put it in a list by its self
# if a sysObject has no children but a prent leave "children" set to an empty list ([])
# if a sysObject has no parent set "parent" to None
# if an sysObject has neither children or a parent remove the "sub" entry or set it to None
# children's move becomes child.mov = "sub"

# ex parent: "sub": {"parent": None, "children": [child0]}
# ex child: "sub": {"parent": [parent0, [1,1,1]], "children":[child1]}


# Sub sysObject
# parent([objId(str), [x,y,z]]/None), children([obj]/[])
class sub:
    def __init__(self, parent=None, children=None):
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = children

    # sets parent
    # parent(obId(str)), offset([x,y,z])
    # none
    def setParent(self, parent, offset):
        self.parent = [parent, offset]

    # set children
    # children([child(objId(str))])
    # none
    def setChildren(self, children):
        self.children = children

    # add a child to a parent
    # child(objId(str))
    # none
    def addChild(self, child):
        self.children.append(child)

    # remove child rom parent
    # index(int)
    # none
    def removeChild(self, index):
        self.children.pop(index)

    # pack data for ram
    # none
    # dta(sub attribs, tags)
    def package(self):
        return sys_objects.data([self.parent, self.children], {"name": "tread.sub.package", "id": None,
                                                               "dataType": "thread.sub.package"})

