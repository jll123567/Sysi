import object


class trd:
    def __init__(self, ram=None, tsk=None, mov=None, lang=None, cpx=None, vis=None, transf=None):
        self.ram = ram
        self.tsk = tsk
        self.mov = mov
        self.lang = lang
        self.cpx = cpx
        self.vis = vis
        self.transf = transf

    # sores audio data to ram
    # Use: <obj> = Sysh.thread.language.store(<obj>)
    # Requires: obj
    def storeHeard(self):
        dta = object.data(self.lang.heard, {})
        self.ram.storage.append(dta)
