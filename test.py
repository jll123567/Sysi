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
for i in [b, e, f]:
    i.tag.update({"lolYep": i.tag["id"]})
print(b.tag)
print(e.tag)
print(f.tag)
