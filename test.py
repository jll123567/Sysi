"""don't mind me, just being dumb"""
import sys_objects
import CGE
import thread_modules
class a(sys_objects.sysObject):
    def __init__(self, m=None, tr=None, tg=None):
        super().__init__(m, tr, tg)
    def c(self):
        print("block me", self.tag["id"])

b = a()
d = a()
e = a()
b.tag["id"] = "o/b"
d.tag["id"] = "o/d"
e.tag["id"] = "o/e"
aOlf = ["b", "d", "e"]
num = 0
for i in [b, d, e]:
    i.trd.olf = thread_modules.Olfactor()
    i.trd.olf.o = thread_modules.OlfactorData(aOlf[num], 0.2)
    i.trd.tsk.appendCurrent([i.tag["id"] + ".trd.tsk", "loopInf", [[
        i.tag["id"] + ".trd.tsk", "doNothing", [], i.tag["id"]
    ]], i.tag["id"]])
    # i.tag["permissions"].update({"trd.tsk.loopInf": "Default"})
    num += 1
del i
del aOlf
del num
b.tag["id"]
f = CGE.CGESession("f", [b, d, e], ["c", False])
f.start()
