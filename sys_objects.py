# coding=utf-8
# sysObject type definitions
# module type: def
import attribs
from math import sqrt
import error
import prog.idGen


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


# sysh.sysObject.user
# model(any), thread(Thread), Personality(Personality), memory(UsrMemory) tag({"id":(str), ...})
class user(sysObject):
    def __init__(self, mod=None, trd=None, prs=None, mem=None, tag=None):
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

    # saves a copy of ram ro memory
    # storedRamName(str)*, storedRamImportance(int[0-100])*
    # none
    def storeToMemory(self, storedRamName, storedRamImportance):
        dta = data([self.trd.ram.storage],
                   {"id": None, "name": storedRamName, "relevancy": [0, 0, storedRamImportance]})
        dta.tag["id"] = prog.idGen.generateGenericId(self.mem.real, dta)
        self.mem.addMemory(1, dta)

    # load a UsrMemory obj to ram
    # block(int[0-2])*, index(int)
    # none
    def loadToRam(self, block, index):
        if block == 0:
            print("no internal access")
        elif block == 1:
            self.trd.ram.load(self.mem.real[index])
        else:
            self.trd.ram.load(self.mem.external[index])

    # check the integrity of an sysObject
    # past of obj(obj)*, obj now(obj)*
    # status(str)
    @staticmethod
    def checkIteg(objPast, objCurrent):
        if objPast.tag["health"] > objCurrent.tag["health"]:
            return "reduced"
        else:
            return "maintained"

    # check freedom of will(functions available)
    # past of obj(obj)*, obj now(obj)*
    # status(str)
    @staticmethod
    def checkWill(objPast, objCurrent):
        if objPast.tag["functlist"].__len__() > objCurrent.tag["functlist"].__len__():
            return "reduced"
        else:
            return "maintained"

    # get the relevancy of an sysObject
    # obj(obj)*
    # relevancy(int)
    @staticmethod
    def calculate_relevancy(obj):
        if obj.tag["relevancy"][1] == 0:
            return 100 + (sqrt(obj.tag["relevancy"][1]) * 10) + 25 + (obj.tag["relevancy"][2])
        else:
            return (100 * ((1 / 3) ** obj.tag["relevancy"][0])) + (sqrt(obj.tag["relevancy"][1]) * 10) + (
                obj.tag["relevancy"][2])

    # load a queue from UsrMemory.real
    # real index(int)*
    # none
    def loadQueue(self, realIndex):
        self.trd.que = self.mem.real[realIndex].storage

    # save a queue to UsrMemory.real
    # tags(tag)*
    # none
    def saveQueue(self, tags):
        lastQueue = data(self.trd.que, tags)
        self.mem.addMemory(1, lastQueue)
        print("queue saved to: ", lastQueue, "@", self.tag["id"], ".UsrMemory.real")


# packaged data
# storage(any), tag({"id":(str), ...})
class data:
    def __init__(self, storage=None, tag=None):
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
        e = error.err(errType, sev, mes, res, sel, self.obj[objListIdx], self.cont, {"id": ""})
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


# info at run
if __name__ == "__main__":
    print("sysObject type definitions\nmodule type: def")
