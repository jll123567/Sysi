"""don't mind me, just being dumb"""
import sys_objects
import CGE
class a(sys_objects.sysObject):
    def __init__(self, m=None, tr=None, tg=None):
        super().__init__(m, tr, tg)
    def c(self):
        print("block me", self.tag["id"])

b = a()
b.tag["id"] = "o/b"
b.tag["permissions"].update({"c":"default"})
b.trd.tsk.current = [["o/b", "c", [], "o/b"]]
d = CGE.CGESession("d", [b], ['c', False])
d.start()