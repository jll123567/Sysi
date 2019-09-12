"""don't mind me, just being dumb"""
import sys_objects
import CGE
from prog.idGen import universalId

ses0 = CGE.CGESession("un/Zero", [], None)
ses1 = CGE.CGESession("un/One", [], None)
dirMain = CGE.sessionDirectory("dr/Main", [ses0, ses1])
a = sys_objects.sysObject()
dirMain.addObj(a, "un/Zero")
print(ses0.objList[0].tag)
# un/Zero/o/11
b = sys_objects.sysObject()
dirMain.addObj(b, "un/Zero")
print(ses0.objList[1].tag)
# un/Zero/o/22
dummy = sys_objects.sysObject()
dirMain.addObj(dummy, "un/Zero")
print(ses0.objList[2].tag)
# un/Zero/o/33
out = sys_objects.sysObject()
dirMain.addObj(out, "un/One")
print(ses1.objList[0].tag)
# un/One/o/11
unnamed = sys_objects.user()
dirMain.addObj(unnamed, "un/Zero")
print(ses0.objList[3].tag)
# un/Zero/u/44
