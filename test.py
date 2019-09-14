"""
Don't mind me, just being testing thisngs here.
Ideally this file will be removed in any sort of "real release".
"""
import sys_objects
import CGE
from prog import idGen

u = sys_objects.universe()
u.tag["id"] = "un/idTst"

dummy = sys_objects.sysObject()
dummy.tag["id"] = "un/idTst/o/11"
dummy.tag["name"] = "dummy"
u.obj.append(dummy)

a = sys_objects.sysObject()
a.tag["name"] = 'a'
b = sys_objects.user()
b.tag["name"] = 'b'
c = sys_objects.data()
c.tag["name"] = 'c'
d = sys_objects.container()
d.tag["name"] = 'd'
e = sys_objects.scene()
e.tag["name"] = 'e'
f = sys_objects.universe()
f.tag["name"] = 'f'


class gg(sys_objects.sysObject):
    def __init__(self):
        super().__init__()


g = gg()
g.tag["name"] = 'g'

u.obj = [dummy, a, b, c, d, e, f]
u.generateIdsForObjects()
u.addObj(g)
for o in u.obj:
    print(o.tag)
