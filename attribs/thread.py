"""Definition for trd attributes in obj"""
import thread_modules.tasker
import thread_modules.ram


class trd:
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
