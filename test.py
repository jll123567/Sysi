"""don't mind me, just being dumb"""
import sys_objects
import CGE
from prog.idGen import universalId

ses0 = CGE.CGESession("un/Zero", [], None)
ses1 = CGE.CGESession("un/One", [], None)
dirMain = CGE.sessionDirectory("dr/Main", [ses0, ses1])
a = sys_objects.sysObject()
a.tag["id"] = universalId(dirMain, ses0.sessionId, a)
print(a.tag)
ses0.objList.append(a)
# un/Zero/o/11
b = sys_objects.sysObject()
b.tag["id"] = universalId(dirMain, ses0.sessionId, b)
print(b.tag)
ses1.objList.append(b)
# un/Zero/o/22
dummy = sys_objects.sysObject()
dummy.tag["id"] = universalId(dirMain, ses0.sessionId, dummy)
print(dummy.tag)
ses0.objList.append(dummy)
# un/Zero/o/33
out = sys_objects.sysObject()
out.tag["id"] = universalId(dirMain, ses1.sessionId, out)
print(out.tag)
ses0.objList.append(out)
# un/One/o/11
unnamed = sys_objects.user()
unnamed.tag["id"] = universalId(dirMain, ses0.sessionId, unnamed)
print(unnamed.tag)
ses0.objList.append(unnamed)
# un/Zero/u/44
