# definition for trd attributes in obj
# module type: def
import object
import threadModules.tasker


# def for thread obj ram(threadModules.ram), tsk(threadModules.tasker), que(threadModules.queue),
# mov(threadModules.move), lang(threadModules.language), cpx(threadModules.complex), vis(threadModules.visual),
# transf(threadModules.transfer), sub(threadModules.subObject)
class trd:
    def __init__(self, ram=None, tsk=threadModules.tasker.tsk(), que=None, mov=None, lang=None, cpx=None, vis=None,
                 transf=None, sub=None):
        self.ram = ram
        self.tsk = tsk
        self.que = que
        self.mov = mov
        self.lang = lang
        self.cpx = cpx
        self.vis = vis
        self.transf = transf
        self.sub = sub

    # stores audio data to ram
    # No input
    # No output
    def storeHeard(self):
        dta = object.data(self.lang.heard, {})
        self.ram.storage.append(dta)

    # makes an object a child object of parent
    # parent(object.object)*, offset([float, float, float])*
    # No output
    def makeChild(self, parent, offset):
        self.sub.parent = [parent, offset],
        self.sub.children = []
        self.mov = "sub"


# info at run
if __name__ == "__main__":
    print("definition for trd attributes in obj\nmodule type: def")
