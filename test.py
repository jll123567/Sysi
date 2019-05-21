"""don't mind me, just being dumb"""
import sys_objects
import CGE
class a(sys_objects.sysObject):
    def __init__(self, m=None, tr=None, tg=None):
        super().__init__(m, tr, tg)
    def c(self):
        print("block me", self.tag["id"])

b = a()
e = a()
f = a()
b.tag["id"] = "o/b"
e.tag["id"] = "o/e"
f.tag["id"] = "o/f"
b.tag["permissions"].update({"c": "default"})
e.tag["permissions"].update({"c": "default", "trd.tsk.debugPrint": "default"})
f.tag["permissions"].update({"c": "default", "trd.tsk.debugPrint": "default"})
b.trd.tsk.current = [["o/f", "c", [], "o/b"], ["o/e.trd.tsk", "debugPrint", ["block me uwu"], "o/b"]]
e.trd.tsk.current = [["o/b", "c", [], "o/e"]]
e.trd.tsk.current = [["o/e", "c", [], "o/f"]]
d = CGE.CGESession("d", [b, e, f], ['c', False], permissions={})
d.start()