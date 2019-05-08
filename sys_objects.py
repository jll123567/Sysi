# coding=utf-8
"""Definitions for base sysh objects."""
import attribs
from math import sqrt
import prog.idGen
import time


# sysh.sysObject.sysObject(oof better name pls) model of sysObject(any), relevant self viewable data(attrib.Thread),
# tags and data for system/admin({tag:(str),...}) noinspection PyShadowingBuiltins
# noinspection PyShadowingBuiltins
class sysObject:
    def __init__(self, mod=None, trd=None, tag=None):
        if mod is None:
            self.mod = attribs.SysModel()
        else:
            self.mod = mod
        if trd is None:
            self.trd = attribs.Thread()
        else:
            self.trd = trd
        if tag is None:
            self.tag = {"id": None, "name": None, "stat": {"hp": 100}}
        else:
            self.tag = tag

    # make an sysObject's model dependant of sub objects
    # none
    # none
    def makeModelAssembly(self):
        oldModel = self.mod
        # noinspection PyTypeChecker
        self.tag.update({"oldModel": oldModel})
        self.mod = "assem"

    # asks some questions to check if obj is a usr
    # console input
    # console output/ obj/ usr
    def usershipQuery(self):
        print("can get info from and modify $HostUni")
        rww = input("y/n")
        print("can get and store objects in memory")
        rwi = input("y/n")
        print("attempts to add reason to previous current and future actions")
        rea = input("y/n")
        print("can add new functions to tasker")
        lrn = input("y/n")
        print("attempts to reserve or increase the integrity and freewill of objects or users")
        mor = input("y/n")
        print("does not == another obj")
        unq = input("y/n")
        total = [rww, rwi, rea, lrn, unq, mor]
        fail = False
        for i in total:
            if i != 'y' or i != 'n':
                fail = True
                print("form incorrectly filled")
                break
            if i == 'n':
                fail = True
                if isinstance(self, user):
                    oldUsrDta = [self.prs, self.mem]
                    objActual = sysObject(self.mod, self.trd, self.tag)
                    # noinspection PyTypeChecker
                    self.tag.update({"oldUsrDta": oldUsrDta})
                    print(self.tag["name"], "is Now Object")
                    return objActual
                else:
                    print(self.tag["name"], "is Object")
        if not fail:
            if isinstance(self, sysObject):
                usr = user(self.mod, self.trd, self.tag["notes"][0], self.tag["notes"][1], self.tag)
                print(self.tag["name"], "is Now User")
                return usr
            else:
                print(self.tag["name"], "is User")

    # remove a parent from a child obj
    # parent(obj)*
    # none
    def removeParent(self, parent):
        parentMov = [parent.trd.mov.x, parent.trd.mov.y, parent.trd.mov.z, parent.trd.mov.a, parent.trd.mov.b,
                     parent.trd.mov.c]
        offset = self.trd.sub.parent[1]
        self.trd.mov.x = parentMov[0] + offset[0]
        self.trd.mov.y = parentMov[1] + offset[1]
        self.trd.mov.z = parentMov[2] + offset[2]
        self.trd.mov.a = parentMov[3]
        self.trd.mov.b = parentMov[4]
        self.trd.mov.c = parentMov[5]
        self.trd.sub.parent = None

    def receiveDamage(self, damage):
        """Apply changes described in damage to stat tag"""
        for stat in self.tag["stat"].keys():
            for dmg in damage.keys():
                if stat == dmg:
                    self.tag["stat"][stat] += damage[dmg]


class user(sysObject):
    """A person in sysh."""
    def __init__(self, mod=None, trd=None, prs=None, mem=None, tag=None):
        """
        :type trd: attribs.Thread
        :type prs: attribs.Personality
        :type mem: attribs.UsrMemory
        :type tag: dict
        :param mod: Model.
        :param trd: Thread.
        :param prs: Personality.
        :param mem: Memory.
        :param tag: System tracking.
        """
        super().__init__(mod, trd, tag)
        if mod is None:
            self.mod = attribs.SysModel()
        else:
            self.mod = mod
        if trd is None:
            self.trd = attribs.Thread()
        else:
            self.trd = trd
        if prs is None:
            self.prs = attribs.Personality()
        else:
            self.prs = prs
        if mem is None:
            self.mem = attribs.UsrMemory()
        else:
            self.mem = mem
        if tag is None:
            self.tag = {"id": None, "name": None, "alias": [], "stat": {"hp": 100}}
        else:
            self.tag = tag

    def storeToMemory(self, storedRamName, storedRamImportance):
        """
        Save a copy of self.trd.ram to memory.

        :type storedRamName: str
        :type storedRamImportance: int
        :param storedRamName: A string to identify the object by.
        :param storedRamImportance:  A value for relevancy importance.
        """
        dta = data([self.trd.ram.storage],
                   {"id": None, "name": storedRamName, "relevancy": [0, 0, storedRamImportance]})
        dta.tag["id"] = prog.idGen.generateGenericId(self.mem.external, dta)
        self.mem.addMemory(1, dta)

    def loadToRam(self, block, idx):
        """
        Load an obj from self.mem to self.trd.ram .

        :type block: int
        :type idx: int
        :param block: Memory block to load from.
        :param idx: Index from block to load from
        """
        if block == 0:
            self.trd.ram.load(self.mem.internal[idx])
        else:
            self.trd.ram.load(self.mem.external[idx])

    @staticmethod
    def checkIteg(objPast, objCurrent):
        """
        Check the integrity of a sysObject.

        :type objPast: sysObject
        :type objCurrent: sysObject
        :param objPast: Old version of object.
        :param objCurrent: New version of object.
        :return: Reduced or maintained.
        """
        if objPast.tag["health"] > objCurrent.tag["health"]:
            return "reduced"
        else:
            return "maintained"

    @staticmethod
    def checkWill(objPast, objCurrent):
        """
        Check the will of a sysObject.

        :type objPast: sysObject
        :type objCurrent: sysObject
        :param objPast: Old version of object.
        :param objCurrent: New version of object.
        :return: Reduced or maintained.
        """
        if objPast.tag["functlist"].__len__() > objCurrent.tag["functlist"].__len__():
            return "reduced"
        else:
            return "maintained"

    @staticmethod
    def calculate_relevancy(obj):
        """
        Calculate the relevancy of an object.

        :type obj: sysObject
        :param obj: Object to calculate relevancy of.
        :return: Relevancy
        """
        if obj.tag["relevancy"][1] == 0:
            return 100 + (sqrt(obj.tag["relevancy"][1]) * 10) + 25 + (obj.tag["relevancy"][2])
        else:
            return (100 * ((1 / 3) ** obj.tag["relevancy"][0])) + (sqrt(obj.tag["relevancy"][1]) * 10) + (
                obj.tag["relevancy"][2])

    def loadQueue(self, idx):
        """
        Load a queue from self.mem.external .

        :type idx: int
        :param idx: Index of self.mem.external .
        """
        self.trd.que = self.mem.external[idx].storage

    def saveQueue(self, tags):
        """
        Save a queue to self.mem.external .

        :type tags: dict
        :param tags: Tags for the queue's enclosing data object.
        """
        lastQueue = data(self.trd.que, tags)  # todo: make a package for queue and use it here.
        self.mem.addMemory(1, lastQueue)


class data:
    """Arbitrary data with tags."""
    def __init__(self, storage=None, tag=None):
        """
        :type storage: any
        :type tag: dict
        :param storage: Arbitrary data.
        :param tag: System tracking.
        """
        if tag is None:
            self.tag = {"id": None, "name": None}
        else:
            self.tag = tag
        self.storage = storage

    def update(self, storage):
        self.storage = storage


# spaces
# origin in relation to supercont([supercont,x,y,z]), bounds[["h/s,x,y,z-x,y,z"], ...], tag({"id":(str), ...})
class container:
    def __init__(self, org=None, bnd=None, tag=None):
        if org is None:
            self.org = [None, 0, 0, 0]
        else:
            self.org = org
        if bnd is None:
            self.bnd = [["h,0,0,0-0,0,0"]]
        else:
            self.bnd = bnd
        # [“(h/s,)x,y,z-x,y,z”,...]
        # [None] means no bounds
        if tag is None:
            self.tag = {"id": None, "name": None}
        else:
            self.tag = tag


class scene:
    """Describes objects calling methods in an container for a time."""

    def __init__(self, tl=None, scp=None, obj=None, cont=None, tag=None):
        """
        :param tl: List with lineName and startTime in that order. None for both if un-plotted.
        :param scp: List of shifts to run.
        :param obj: List of objects in scene.
        :param cont: Container that encapsulates the scene.
        :param tag: Dict for system tracking.
        """
        if tl is None:
            self.tl = [None, None]
        else:
            self.tl = tl
        if scp is None:
            self.scp = [["master", None, 30]]
        else:
            self.scp = scp
        if obj is None:
            self.obj = []
        else:
            self.obj = obj
        if cont is None:
            self.cont = container([None, 0, 0, 0], ["h,0,0,0-0,0,0"], {"id": None, "name": "defaultContainer"})
        else:
            self.cont = cont
        if tag is None:
            self.tag = {"id": None, "name": None}
        else:
            self.tag = tag

    def tlUnplot(self):
        """Unplot the scene from a time line."""
        self.tl = [None, None]

    def tlPlot(self, line, startOffset):
        """Plot the scene to a time line."""
        self.tl = [line, startOffset]

    def raiseSyshError(self, objListIdx, errType, sev, mes, res, sel):
        """Add an error to the scene."""
        e = sysErr(errType, sev, mes, res, sel, self.obj[objListIdx], self.cont, {"id": ""})
        e.tag["id"] = prog.idGen.generateGenericId(self.obj, e)
        self.obj.append(e)

    def raiseRequest(self, request, objListIdx):
        """Add a request to the scene."""
        d = data([request, self.cont, self.obj[objListIdx]], {"id": "", "dataType": "request"})
        d.tag["id"] = prog.idGen.generateGenericId(self.obj, d)
        self.obj.append(d)


class universe:
    """Describes a collection of scenes and relevant information."""

    def __init__(self, scn=None, obj=None, cont=None, funct=None, rule=None, tag=None):
        """
        :param scn: List of scenes.
        :param obj: List of objects.
        :param cont: List of containers.
        :param funct: List of functions.
        :param rule: List of operations to be run each shift in applicable scenes.
        :param tag: Dict for system tracking.
        """
        if scn is None:
            self.scn = []
        else:
            self.scn = scn
        if obj is None:
            self.obj = []
        else:
            self.obj = obj
        if cont is None:
            self.cont = []
        else:
            self.cont = cont
        if funct is None:
            self.funct = []
        else:
            self.funct = funct
        if rule is None:
            self.rule = []
        else:
            self.rule = rule
        if tag is None:
            self.tag = {"id": None, "name": None}
        else:
            self.tag = tag

    def tlGetEndOfLine(self, line):
        """Find the time in shifts that a lines and return it."""
        tempScnList = []
        for scnLn in self.scn:
            if scnLn.tl[0] == line:
                tempScnList.append(scnLn)
        scnIdx = 0
        currentScnIdx = 0
        largestStartTime = 0
        for scnChk in tempScnList:
            if scnChk.tl[1] > largestStartTime:
                scnIdx = currentScnIdx
                largestStartTime = scnChk.tl[1]
            currentScnIdx += 1
        return tempScnList[scnIdx].__len__() - 1


class sysErr:
    """Deprecated"""

    def __init__(self, errType=None, severity=None, message=None, resolutions=None, selected=None, obj=None, cont=None,
                 tag=None):
        """
        :param errType: int:
            0 resolved
            1 warn
            2 error
        :param severity: int:
            0 resolved
            1 low
            2 medium
            3 high
            4 critical
            5 fatal
        :param message: str
        :param resolutions: list
            [str, ...]
        :param selected: None/int
        :param obj: str
            obj Id
        :param cont: str
            cont Id
        :param tag: dict
            system tracking
        """
        if resolutions is None:
            self.resolutions = []
        else:
            self.resolutions = resolutions
        if selected is None:
            self.selected = []
        else:
            self.selected = selected
        if tag is None:
            self.tag = {"name": None, "id": None}
        else:
            self.tag = tag
        self.errType = errType
        self.severity = severity
        self.message = message
        self.obj = obj
        self.cont = cont
        self.timeRaised = time.clock()

    def setError(self, errType, severity, message, resolutions, selected, obj, cont):
        """Set error attributes."""
        self.errType = errType
        self.severity = severity
        self.message = message
        self.obj = obj
        self.cont = cont
        self.resolutions = resolutions
        self.selected = selected

    # clear the error
    # none
    # none
    def clearError(self):
        """Clear error attributes."""
        self.resolutions = None
        self.selected = None
        self.errType = None
        self.severity = None
        self.message = None
        self.obj = None
        self.cont = None

    def resolveError(self):
        """Console thing to do resolution."""
        resolving = True
        print(self.errType + ',' + self.severity + ':' + self.message)
        count = 0
        for resolution in self.resolutions:
            print(str(count) + ":" + resolution)
            count += 1
        while resolving:
            try:
                selected = input("resolution?:")
                self.selected = int(selected)
            except ValueError:
                print("int only")
            else:
                resolving = False


# info at run
if __name__ == "__main__":
    print("sysObject type definitions\nmodule type: def")
