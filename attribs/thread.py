# definition for trd attributes in obj
# module type: def
import object
import thread_modules.tasker


# def for thread obj ram(thread_modules.ram), tsk(thread_modules.tasker), que(thread_modules.queue),
# mov(thread_modules.move), lang(thread_modules.language), cpx(thread_modules.complex), vis(thread_modules.visual),
# transf(thread_modules.transfer), sub(thread_modules.subObject)
class trd:
    def __init__(self, ram=None, tsk=None, que=None, mov=None, lang=None, cpx=None, vis=None,
                 transf=None, sub=None):
        self.ram = ram
        if tsk is None:
            self.tsk = thread_modules.tasker.tsk()
        else:
            self.tsk = tsk
        self.que = que
        self.mov = mov
        self.lang = lang
        self.cpx = cpx
        self.vis = vis
        self.transf = transf
        self.sub = sub

    # stores audio data to ram
    # none
    # none
    def storeHeard(self):
        dta = object.data(self.lang.heard, {})
        self.ram.storage.append(dta)

    # makes an object a child object of parent
    # parent(object.object)*, offset([float, float, float])*
    # none
    def makeChild(self, parent, offset):
        self.sub.parent = [parent, offset],
        self.sub.children = []
        self.mov = "sub"


# info at run
if __name__ == "__main__":
    print("definition for trd attributes in obj\nmodule type: def")
