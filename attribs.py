"""Common attributes for sysObjects."""
import re
import hashlib
import sys_objects
import thread_modules.tasker
import thread_modules.ram


class UsrMemory:
    """
    Hold arbitrary copies of objects.
        Functions requesting a block want an int between 0 and 2.
            0 is for internal, 1 is for real, 2 is for external
    """

    def __init__(self, internal=None, real=None, external=None):
        """
        :param internal: list
        :param real: list
        :param external: list
        """
        if internal is None:
            self.internal = []
        else:
            self.internal = internal
        if real is None:
            self.real = []
        else:
            self.real = real
        if external is None:
            self.external = []
        else:
            self.external = external

    def removeMemory(self, block, index):
        """Remove the memory at block[index]."""
        if block == 0:
            self.internal.pop(index)
        elif block == 1:
            self.real.pop(index)
        else:
            self.external.pop(index)

    def addMemory(self, block, obj):
        """Add obj to UsrMemory at block."""
        if block == 0:
            self.internal.append(obj)
        elif block == 1:
            self.real.append(obj)
        else:
            self.external.append(obj)

    def find(self, query=""):
        """
        Print objects in UsrMemory that match query.
        If nothing is found None is printed.
        """
        for d in self.__dict__:
            for i in d:
                if re.match(str(i), r"*(.)" + query + r"*(.)"):
                    print(i)
                else:
                    print(None)

    def modify(self, block, index, value):
        """Set the value at index in block in UsrMemory."""
        if block == 0:
            self.internal[index] = value
        elif block == 1:
            self.real[index] = value
        else:
            self.external[index] = value


class SysModel:
    """sysh's own 3d model format(why not?)"""

    def __init__(self, geom=None, skel=None, ani=None):
        """
        :param geom: {"scale": int, "points": ["x,y,z-x,y,z","more points"]}
        :param skel: {"scale": int, "points": [skeleton point"x,y,z",["points bound to it(by offset)"x,y,z","..."], [...]}
        :param ani: {animationName: {"scale": int, [[original skpos"x,y,z", new pos(1ms later)"x,y,z", "..."], [...]]},nextAnimation: [...]}
        Note that parents have a model of "assem".
        """
        if geom is None:
            self.geom = {"scale": 1, "lines": ["0,0,0-0,0,0"]}
        else:
            self.geom = geom
        if skel is None:
            self.skel = {"scale": 1, "points": ["0,0,0", ["0,0,0"]]}
        else:
            self.skel = skel
        if ani is None:
            self.ani = {"default": {"scale": 1, "animation": [["0,0,0", "0,0,0", ]]}}
        else:
            self.ani = ani

    def addAnimation(self, animation):
        """Add a new animation to the model."""
        self.ani.update(animation)


class FileModel:
    """Model based on a file."""

    def __init__(self, file):
        """:param file: any"""
        self.file = file


class Personality:
    """
    Define loosely the behavior of users.
    Pers only helps loosely define user behavior but does not code for behavior. Use Thread.tsk for this.
    Goals and limits are boolean expressions ranked most important to least important(goal[0] is most).
    Goals are encouraged, limits are not.
    """

    def __init__(self, goals=None, limits=None, functions=None):
        """
        :param goals: list
        :param limits: list
        :param functions: list
        """
        if goals is None:
            self.goals = []
        else:
            self.goals = goals
        if limits is None:
            self.limits = []
        else:
            self.limits = limits
        if functions is None:
            self.functions = []
        else:
            self.functions = functions

    def setPrs(self, limit, goal, funct):
        """Set self.limit, goal and functions to <limit>, <goal>, <funct>."""
        self.limits = limit
        self.goals = goal
        self.functions = funct

    def newGoal(self, goal, index):
        """Insert <goal> to self.goals[<index>]."""
        self.goals.insert(index, goal)

    def newLimit(self, limit, index):
        """Insert <limit> to self.limits[<index>]."""
        self.limits.insert(index, limit)

    def newFunction(self, funct):
        """Insert <funct> to self.functions[<index>]."""
        self.functions.append(funct)

    def removeGoal(self, index):
        """Remove goal at <index>."""
        self.goals.pop(index)

    def removeLimit(self, index):
        """Remove limit at <index>."""
        self.limits.pop(index)

    def removeFunction(self, index):
        """Remove function at <index>."""
        self.functions.pop(index)

    def clearPrs(self):
        """Set all Personality attributes to None."""
        self.limits = None
        self.goals = None
        self.functions = None


class Thread:
    """Holds self and public accessible data for computation."""

    def __init__(self, ram=None, tsk=None, que=None, somm=None, mov=None, lang=None, cpx=None, vis=None,
                 transf=None, sub=None):
        """Check each thread_modules class of the same name."""
        if ram is None:
            self.ram = thread_modules.ram.ram()
        else:
            self.ram = ram
        if tsk is None:
            self.tsk = thread_modules.tasker.tsk()
        else:
            self.tsk = tsk
        self.que = que
        self.somm = somm
        self.mov = mov
        self.lang = lang
        self.cpx = cpx
        self.vis = vis
        self.transf = transf
        self.sub = sub

    def storeHeard(self):
        """Store audio data to ram."""
        dta = self.lang.package()
        self.ram.storage.append(dta)

    def makeChild(self, parent, offset):
        """Make a sysObject a child of <parent>"""
        self.sub.parent = [parent, offset],
        self.sub.children = []
        self.mov = "sub"


def hashObj(obj):
    """Return the MD5 hash of obj"""
    info = obj
    dta = sys_objects.data((hashlib.md5(info.encode('utf-8')).hexdigest()), obj.tag)
    return dta
