"""
Don't mind me, just being testing thisngs here.
Ideally this file will be removed in any sort of "real release".
"""
import sys_objects
import thread_modules

a = sys_objects.sysObject()
a.tag["id"] = "un/tst/o/00"
a.trd.sub = thread_modules.SubObjManager()
a.trd.mov = thread_modules.Move()
a.trd.mov.warp(1, 2, 1)
b = sys_objects.sysObject()
b.tag["id"] = "un/tst/o/11"
b.trd.sub = thread_modules.SubObjManager()
b.trd.mov = thread_modules.Move()
b.trd.mov.warp(5, 5, 5)
a.trd.sub.addChild(b)
b.addParent(a)
print(b.getActualChildMov().debugMov())
