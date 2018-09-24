import object
import threadModules.tasker



class trd:
    def __init__(self, ram=None, tsk=threadModules.tasker.tsk(), que=None, mov=None, lang=None, cpx=None, vis=None, transf=None,
                 sub=None):
        self.ram = ram
        self.tsk = tsk
        self.que = que
        self.mov = mov
        self.lang = lang
        self.cpx = cpx
        self.vis = vis
        self.transf = transf
        self.sub = sub

    # sores audio data to ram
    # Use: <obj> = Sysh.threadModules.language.store(<obj>)
    # Requires: obj
    def storeHeard(self):
        dta = object.data(self.lang.heard, {})
        self.ram.storage.append(dta)

    def makeChild(self, parent, offset):
        self.sub.parent = [parent, offset],
        self.sub.children = []
        self.mov = "sub"
