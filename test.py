"""don't mind me, just being dumb"""
import sys_objects
import CGE
import thread_modules.tasker as tk
import types
a = sys_objects.sysObject()
a.tag["id"] = "a"
a.trd.tsk.appendCurrent(tk.createSustainOperation("a"))
b = sys_objects.sysObject()
b.tag["id"] = "b"


def attack(self):
    self.trd.tsk.addShift([tk.createOperation("a", "receiveDamage", [{"hp": -10}], "b")])


b.attack = types.MethodType(attack, b)
b.trd.tsk.appendCurrent(tk.createOperation("b", "attack", [], "b"))
c = CGE.CGESession("", [a, b], ['c', False])
c.start()
d = True
while d:
    for i in c.objList:
        print(i.tag["stat"]["hp"], ":", i.tag["id"])
        # print(c.objList[1].trd.tsk.current)
        if i.tag["stat"]["hp"] != 100:
            d = False
