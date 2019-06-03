"""Modules for attribs.Thread"""
import sys_objects
import prog.idGen
import attribs
import time
import socket

# restructure threadmodules to make data passing better
try:
    from sys_objects import data

    a = sys_objects.data()
    del a
except AttributeError:
    print("thread_modules cant see sys_objects.data")
    print(dir(sys_objects))


# Thread modules are small things added to a trd attribute at an object
# They all have the same structure except for a few special cases
#
# class TrdModuleData:
#     def __init__(self, urData, ...):
#         ...
#     ...
# class TrdModule:
#     def __init__(self, i, o, misc, misc1, ...):
#         ...
#     ...
# Data of type TrdModuleData is taken from TrdModule.o, combined with other data by CGE and put back into TrdModule.i
# if a module has no i or o its assumed it doesn't output/input
# Ill describe how CGE does combining

class Complex:
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
        """Pack data for Ram."""
        return sys_objects.data([self.problems, self.solutions], {"name": "Thread.Complex.package", "id": None,
                                                                  "dataType": "Thread.Complex.package"})


class AudioStereo:
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


class AudioMono:
    """Hold mono audio."""

    def __init__(self, sound=None):
        """
        :param sound: list
        """
        if sound is None:
            self.sound = []
        else:
            self.sound = sound

    def empty(self):
        self.sound = []


class Language:
    """Hold and manipulate audio."""

    def __init__(self, i=AudioStereo(), o=AudioMono()):
        """
        :param i: AudioStereo
        :param o: AudioMono
        """
        self.i = i
        self.o = o

    def listen(self, inputSource):
        """Get sound from input and append it to i."""
        self.i.left.append(inputSource.l)
        self.i.right.append(inputSource.r)

    def tune(self, minVolume, minPan, maxPan):
        """
        Check if audio is above a minimum volume or within a pan range and if its not cut it.

        Min volume is in Db.
        pan is a float range from -1.0 to 1.0.
        minPan is the smallest pan value.
        maxPan is the largest pan value.
        """

        for i in self.i.left:
            if abs(i) < minVolume:
                self.i.left[self.i.left.index(i)] = 0
            elif minPan > 0:
                self.i.left[self.i.left.index(i)] = 0
            elif abs(i) > minPan * -100:
                self.i.left[self.i.left.index(i)] = 0
            else:
                continue

        for i in self.i.right:
            if abs(i) < minVolume:
                self.i.right[self.i.right.index(i)] = 0
            elif maxPan < 0:
                self.i.right[self.i.right.index(i)] = 0
            elif abs(i) < maxPan * 100:
                self.i.right[self.i.right.index(i)] = 0
            else:
                continue

    def silence(self):
        """Clear spoken audio."""
        self.o = []

    def queueSpeak(self, sounds):
        """Add sounds to the speaking queue."""
        self.o = sounds

    def package(self):
        """Pack audio data into a data obj and return it."""
        return sys_objects.data([self.i, self.o], {"name": "Thread.Language.package", "id": None,
                                                   "dataType": "Thread.Language.package"})


class Move:
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

        o1 needs to be a Thread.Move not an sysObject.sysObject
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

        o1 needs to be a Thread.Move not an sysObject.sysObject
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
                                {"name": "Thread.Move.package", "id": None, "dataType": "Thread.Move.package"})


class OlfactorData:
    """"""

    def __init__(self, descriptor="None", strength=0):
        """
        :param descriptor: str
            Descriptor is a string.
        :param strength: int
            Strength is a float between and including 0 and 1.
        """
        self.descriptor = descriptor
        self.strength = strength


class Olfactor:
    """
    Hold olfactory input for thread.
    """

    def __init__(self, i=None, o=None):
        """
        :param i: list
            Inputted OlfactorData
        :param o: list
            Outputted OlfactorData
        """
        if i is None:
            self.i = None
        else:
            self.i = i
        if o is None:
            self.o = None
        else:
            self.o = o

    def package(self):
        """Pack Olfactor data into a data sysObject(it needs an id) and return it."""
        return sys_objects.data([self.i, self.o], {"name": "Thread.Olfactor.package", "id": None,
                                                   "dataType": "Thread.Olfactor.package"})


class Queue:
    """Soft Tasker planning."""

    def __init__(self, tasks=None):
        """
        :param tasks: list
        """
        if tasks is None:
            self.tasks = []
        else:
            self.tasks = tasks

    def close(self):
        """Empty queue."""
        self.tasks = []

    def interrupt(self, task, index=0):
        """Insert <task> at <index> in self.tasks."""
        self.tasks.insert(index, task)

    def complete(self, index=None):
        """
        Remove the task at <index>.
        if <index> is None then remove self.tasks[0].
        """
        if index is None:
            self.tasks.pop(0)
        else:
            self.tasks.pop(index)

    def showTask(self):
        """Print all tasks in self."""

        def recurse(thatThingThatIsAListOfThings, indent):
            """Iterate through thatThingThatIsAListOfThings and recursively add indents."""
            if isinstance(thatThingThatIsAListOfThings, list):
                recurse(thatThingThatIsAListOfThings, indent + 1)
            else:
                if i[0] == "e":
                    print("  " * indent, "exact:", thatThingThatIsAListOfThings)
                elif i[0] == "i":
                    print("  " * indent, "inexact:", thatThingThatIsAListOfThings)
                else:
                    print("Not a valid task type")

        for i in self.tasks:
            recurse(i, 0)

    def makeValidTskProfile(self, queue):
        if isinstance(queue, Queue):
            tasks = queue.tasks
        else:
            tasks = queue
        # flatten "function" by rightfootin
        # snippet link: https://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
        #   modified to not include nested tuples as queues only support lists (or at least they're supposed to)
        mainTask = []
        for item in tasks:
            if isinstance(item, list):
                mainTask.extend(self.makeValidTskProfile(item))
            else:
                mainTask.append(item)
        return mainTask


class Ram:
    """
    Holds random data the thread needs to store temporarily.
    Storage elements hold any.
    """

    def __init__(self, storage=None):
        """
        :param storage: list
        """
        if storage is None:
            self.storage = []
        else:
            self.storage = storage

    def load(self, dta):
        """Put dta into self.storage ."""
        self.storage.append(dta)

    def loadTrdDta(self, dta):
        """Generate a generic id for dta and load() it."""
        dta.tag["id"] = prog.idGen.generateGenericId(self.storage, dta)
        self.load(dta)

    def read(self):
        """Print the contents of self.storage to the console."""
        for i in self.storage:
            print(i)

    def search(self, query):
        """
        Search self.storage for query
        Returns the index if the sysObject in storage and query are equal.
        Prints a message to the console if nothing was found.
        """
        matched = True
        idx = 0
        for i in self.storage:
            if i == query:
                return idx
            idx += 1
        if not matched:
            print("no results. try obj.trd.Ram.read()")

    def free(self, index):
        """
        Removes an sysObject from self.storage(with *style*).

        Index(int): Remove self.storage[index].
        Index(None): Remove self.storage[-1]
        Index("all"): Set self.storage = []
        Index(anything else): Print "invalid request".
        """
        if index is None:
            self.storage.pop(-1)
        elif index == "all":
            self.storage = []
        elif isinstance(index, int):
            self.storage.pop(index)
        else:
            print("invalid request")


class SOMState(sys_objects.data):
    """An individual SOMState, acts as a Personality with a name encoded as a data."""

    def __init__(self, stateName, prs, tag=None):
        """
        :param stateName: string
        :param prs: attribs.Personality
        :param tag: dictionary
        """
        super().__init__(prs, tag)
        if tag is None:
            self.tag = {"id": None, "name": None, "dataType": "SOMState", "stateName": stateName}
        else:
            self.tag = tag

    def rename(self, newName):
        """Change stateName of SOMState to newName."""
        self.tag["stateName"] = newName


class SOMManger:
    """Hold and modify states."""

    def __init__(self, states=None, default=None, current=None, previous=None):
        """
        :param states: list
        :param default: attribs.Personality
        :param current: attribs.Personality
        :param previous: attribs.Personality
        """
        if states is None:
            self.states = []
        else:
            self.states = states
        if default is None:
            self.states.append(SOMState("Default", attribs.Personality()))
        else:
            self.states.append(SOMState("Default", default))
        if current is None:
            self.states.append(SOMState("Current", attribs.Personality()))
        else:
            self.states.append(SOMState("Current", current))
        if previous is None:
            self.states.append(SOMState("Previous", attribs.Personality()))
        else:
            self.states.append(SOMState("Previous", previous))

    @staticmethod
    def newState(stateName, personality, tag=None):
        """Return a new instance of SOMState."""
        return SOMState(stateName, personality, tag)

    def addState(self, stateToAdd):
        """Add SOMState to self.states."""
        self.states.append(stateToAdd)

    def removeState(self, stateName):
        """Remove SOMState named stateName from self.states."""
        self.states.pop(self.resolveStateNameToIndex(stateName))

    def makeDefault(self, stateName, renameForCurrentDefault):
        """Rename the SOMState with the name "Default" to renameForCurrentDefault if possible.
            Rename SOMState with stateName to "Default".
        """
        if self.resolveStateNameToIndex("Default") is not None:
            self.states[self.resolveStateNameToIndex("Default")].rename(renameForCurrentDefault)
        self.states[self.resolveStateNameToIndex(stateName)].rename("Default")

    def makePrevious(self, stateName, renameForPrevious):
        """Rename the SOMState with the name "Previous" to renameForPrevious if possible.
            Rename SOMState with stateName to "Previous".
        """
        if self.resolveStateNameToIndex("Previous") is not None:
            self.states[self.resolveStateNameToIndex("Previous")].rename(renameForPrevious)
        self.states[self.resolveStateNameToIndex(stateName)].rename("Previous")

    def makeCurrent(self, stateName):
        """Rename the SOMState with the name "Current" to "Previous" and SOMState with stateName to "Current".
            Create Previous if it doesn't exist
            Don't change Previous is Current doesn't exist.
        """
        if self.resolveStateNameToIndex("Previous") is not None:
            if self.resolveStateNameToIndex("Current") is not None:
                self.states[self.resolveStateNameToIndex("Previous")]. \
                    update(self.states[self.resolveStateNameToIndex("Current")].storage)
        else:
            if self.resolveStateNameToIndex("Current") is not None:
                self.addState(SOMState("Previous", self.states[self.resolveStateNameToIndex("Current")].storage))
        self.states[self.resolveStateNameToIndex(stateName)].rename("Current")

    def resolveStateNameToIndex(self, stateName):
        """Find and return the index of the SOMState with the stateName stateName."""
        idx = 0
        for stateInstance in self.states:
            if stateInstance.tag["stateName"] == stateName:
                break
            idx += 1
        if idx == self.states.__len__():
            return None
        return idx


# this is an example class for SOM
# class SOMObject(sys_objects.user):
#
#     def __init__(self, mod=None, trd=None, prs=None, mem=None, tag=None):
#         super().__init__(mod, trd, prs, mem, tag)
#
#     def changeSOMState(self, stateName, makePreviousDefault=True):
#         SOMManagerInstance = self.trd.somm
#         if not self.matchName("Previous", SOMManagerInstance):
#             SOMManagerInstance.addState(SOMManagerInstance.newState("Previous", self.prs))
#         else:
#             SOMManagerInstance.states[SOMManagerInstance.resolveStateNameToIndex("Previous")].update(self.prs)
#         if makePreviousDefault:
#             SOMManagerInstance.makeDefault("Previous", "previousDefault")
#         self.prs = SOMManagerInstance.states[SOMManagerInstance.resolveStateNameToIndex(stateName)].storage
#         if not self.matchName("Current", SOMManagerInstance):
#             SOMManagerInstance.addState(SOMManagerInstance.newState("Current", self.prs))
#         else:
#             SOMManagerInstance.states[SOMManagerInstance.resolveStateNameToIndex("Current")].update(self.prs)
#         self.trd.somm = SOMManagerInstance
#
#     def saveCurrentSOMState(self):
#         if self.matchName("Current", self.trd.somm):
#             self.trd.somm.states[self.trd.somm.resolveStateNameToIndex("Current")].update(self.prs)
#         else:
#             self.trd.somm.addState(self.trd.somm.newState("Current", self.prs))
#
#     def revertSOMStateToDefault(self):
#         self.prs = self.trd.somm.states[self.trd.somm.resolveStateNameToIndex("Default")].storage
#         self.trd.somm.makeCurrent("Default")
#
#     def revertSOMStateToPrevious(self):
#         self.prs = self.trd.somm.states[self.trd.somm.resolveStateNameToIndex("Previous")].storage
#         self.trd.somm.makeCurrent("Previous")
#
#     @staticmethod
#     def matchName(stateName, SOMMInstance):
#         for tmpState in SOMMInstance.states:
#             if tmpState.tag["stateName"] == stateName:
#                 return True
#         return False


class SubObjManager:
    """
    Data for SysObjects that are/have subObjects.

    Objects can be like groups without being groups.
    Parent and child objects have a "SubObjManager" section in their Thread.
    """

    def __init__(self, parent=None, children=None):
        """
        :param parent: list
            [reference, offset]
        :param children: list
            [reference, ...]

        reference = object's id

        offset = [x,y,z]

        If a sysObject has no children but a parent leave "children" set to an empty list ([])

        If a sysObject has no parent set "parent" to None

        If an sysObject has neither children or a parent remove the "SubObjManager" entry or set parent and children to None.

        If has a parent, move becomes child.trd.mov = "sub"
        """
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = children

    def setParent(self, parent, offset):
        """Set the parent and offset."""
        self.parent = [parent, offset]

    def setChildren(self, children):
        """Set children."""
        self.children = children

    def addChild(self, child):
        """Append self.children with <child>."""
        self.children.append(child)

    def removeChild(self, index):
        """Remove the child at <index>."""
        self.children.pop(index)

    def package(self):
        """Package for Ram."""
        return sys_objects.data([self.parent, self.children], {"name": "Thread.SubObjManager.package", "id": None,
                                                               "dataType": "Thread.SubObjManager.package"})


class Tasker:
    """
    Handle function requests for CGE
    Essential for threads.
    """

    def __init__(self, current=None, profile=None):
        """
        :param current: shift
        :param profile: list
            [shift, ...]

        shift = [operation, ...]

        operation = [target, method, [parameters, ...], source(this SysObject's id)]
        """
        if current is None:
            self.current = []
        else:
            self.current = current
        if profile is None:
            self.profile = []
        else:
            self.profile = profile

    def nextCurrent(self):
        """Move shift in self.profile[0] to self.current."""
        if self.profile:
            if isinstance(self.profile[0], list):
                self.current = self.profile[0]
            else:
                self.current = [self.profile[0]]
            self.profile.pop(0)
        else:
            self.current = []

    def debugCurrentOp(self):
        """
        Print self.current[0] or the shift in current.
        This can be used for debugging but also can be used to leak data from the thread in unexpected ways.
        """
        print(self.current[0])

    def setCurrent(self, shift):
        """Set self.current to <shift>."""
        self.current = shift

    def appendCurrent(self, operation):
        """Append <operation> to self.current ."""
        self.current.append(operation)

    def addShift(self, shift):
        """Append <shift> to self.profile ."""
        self.profile.append(shift)

    def removeShift(self, index):
        """Remove self.profile[<index>]."""
        self.profile.pop(index)

    @staticmethod
    def wait(t):
        """Time.sleep() for <t> seconds."""
        time.sleep(t)

    @staticmethod
    def doNothing():
        """Do LITERALLY NOTHING."""
        pass

    def loopInf(self, operation):  # todo extend the functionality of this a tad?
        """Add a shift that runs <operation> and this method(<operation>)."""
        objId = ""
        for char in operation[0]:
            if char == '.':
                break
            else:
                objId += char
        objId += ".Thread.Tasker"
        self.addShift([operation, [objId, "loopInf", [operation], operation[3]]])

    def ifStatement(self, comparator, object0, object1, then, els=None):
        """
        Determine the next shift based on the state of <object0> and <object1>.

        :param comparator: ("==","!=",">","<","<=",">=")
        :param object0: any
        :param object1: any
        :param then: shift
        :param els: shift or None
        """
        if not isinstance(then[0], list):
            then = [then]
        if comparator == '==':
            if object0 == object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '!=':
            if object0 != object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '>':
            if object0 > object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '<':
            if object0 < object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '>=':
            if object0 >= object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        elif comparator == '<=':
            if object0 <= object1:
                self.profile.insert(0, then)
            else:
                if els is not None:
                    self.profile.insert(0, els)
        else:
            print("the comparator inputted is not valid")

    @staticmethod
    def debugPrint(msg):
        """Print <msg>."""
        print(msg)

    @staticmethod
    def createOperation(targetId, function, parameters, sourceId):
        """Create an operation and return it."""
        return [targetId, function, parameters, sourceId]

    def createSustainOperation(self, objId):
        return self.createOperation(objId + ".Thread.Tasker", "loopInf",
                                    [self.createOperation(objId + ".Thread.Tasker", "doNothing", [], objId)], objId)

    def package(self):
        """Package data for Ram."""
        return sys_objects.data([self.current, self.profile], {"name": "Thread.Tasker.package", "id": None,
                                                               "dataType": "Thread.Tasker.package"})


class TasteData:
    """Handle an instance of a taste."""

    def __init__(self, bit=0.0, swt=0.0, slt=0.0, sor=0.0, pln=0.0):
        """
        All attributes are floats from 0 to 1.

        :param bit: float
        :param swt: float
        :param slt: float
        :param sor: float
        :param pln: float
        """
        self.bit = bit
        self.swt = swt
        self.slt = slt
        self.sor = sor
        self.pln = pln


class Taste:
    """Handle taste."""

    def __init__(self, i, o):
        """
        :param i: list
            Inputted TasteData.
        :param o: list
            Outputted TasteData.
        """
        if i is None:
            self.i = []
        else:
            self.i = i
        if o is None:
            self.o = []
        else:
            self.o = o

    def package(self):
        """Pack taste into a data and return it."""
        return sys_objects.data([self.i, self.o], {"name": "Thread.Taste.package",
                                                   "id": None,
                                                   "dataType": "Thread.Taste.package"})


class TactileData:
    """Individual points for Tactile."""

    def __init__(self, position=None, pressure=0.0, relTemp=0.0):
        """
        :param position: list
        :param pressure: float
        :param relTemp: float
        """
        if position is None:
            self.position = [0.0, 0.0, 0.0]
        else:
            self.position = position
        self.pressure = pressure
        self.relTemp = relTemp

    def package(self):
        """Package for Ram."""
        return sys_objects.data(self.flatten(), {"name": "Thread.Tactile.TactileSensoryNode.package", "id": None,
                                                 "dataType": "Thread.Tactile.TactileSensoryNode.package"})

    def flatten(self):
        """Return a list of self.position, self.pressure, and self.relTemp respectively."""
        return [self.position, self.pressure, self.relTemp]


class Tactile:
    """Handle tactile sensory data."""

    def __init__(self, i, o):
        """
        :param i: list
            Inputted TasteData.
        :param o: list
            Outputted TasteData.
        """
        if i is None:
            self.i = []
        else:
            self.i = i
        if o is None:
            self.o = []
        else:
            self.o = o

    def package(self):
        """Package for Ram."""
        nodeListI = []
        for node in self.i:
            nodeListI.append(node.flatten())
        nodeListO = []
        for node in self.o:
            nodeListO.append(node.flatten())
        return sys_objects.data([nodeListI, nodeListO],
                                {"name": "Thread.Tactile.package", "id": None, "dataType": "Thread.Tactile.package"})


class Transfer:
    """General SysData I/O with socket support."""

    def __init__(self, interface=None):
        """
        :param interface: any
        """
        self.interface = interface

    def send(self, sender, dta):
        """Package data for sending."""
        pkg = dta
        pkg.tag.update({"sender": sender})
        self.interface = pkg

    def receive(self, sender):
        """Grab data using a copy of the sending object."""
        # Is there a better way to do this? Probably.
        try:
            self.interface = sender.trd.transf.interface
        except AttributeError:
            print("listed sender:" + str(sender.tag["name"]) + "'s Transfer interface was not found\ndoes it have a "
                                                               "Thread.Transfer")

    def clearInterface(self):
        """Set self.interface to None."""
        self.interface = None

    def makeSocketInterface(self):
        """Create a new socket at self.interface ."""
        self.interface = socket.socket()

    def connectSocket(self, host, port):
        """Connect the socket using its provided method."""
        self.interface.connect((host, port))

    def sendSocket(self, msg):
        """
        Send ascii text.
        Raise a RuntimeError if the connection breaks.
        """
        msg = msg.encode("ascii")
        totalSent = 0
        while totalSent < len(msg):
            sent = self.interface.send(msg[totalSent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalSent = totalSent + sent

    def receiveSocket(self):
        """
        Grab 254 bytes from the socket.
        Raise a RuntimeError if the connection breaks.
        """
        chunks = []
        bytes_recd = 0
        while bytes_recd < 254:
            chunk = self.interface.recv(min(254 - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def disconnectSocket(self):
        """Close the socket."""
        self.interface.close()


class Visual:
    """Hold and process visual data."""

    def __init__(self, i=None, pitch=0, yaw=0, roll=0):
        """
        :param i: list
        :param pitch: float
        :param yaw: float
        :param roll: float
        """
        if i is None:
            self.i = []
        else:
            self.i = i
        self.rx = pitch
        self.ry = yaw
        self.rz = roll

    def rotate(self, rx, ry, rz):
        """Set the rotation attributes of the visual thread."""
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def clearImg(self):
        """Set the i attribute to an empty list."""
        self.i = []

    def resetPos(self):
        """Set rotation attributes to 0."""
        self.rx = 0
        self.ry = 0
        self.rz = 0

    def package(self):
        """Package for Ram"""
        return sys_objects.data([self.i, self.rx, self.ry, self.rz], {"name": "Thread.Visual.package", "id": None,
                                                                      "dataType": "Thread.Visual.package"})
