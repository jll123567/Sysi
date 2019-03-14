"""don't mind me, just being dumb"""
import CGE
import sys_objects
import thread_modules.ram
a = sys_objects.sysObject()
a.tag["id"] = "a"
a.trd.tsk.current = [["CSH", "crossWarp", ["S1"], a.tag["id"]]]
e = sys_objects.sysObject()
e.tag["id"] = "e"
e.trd.ram = thread_modules.ram.ram()
e.trd.tsk.current = [["e.trd.tsk", "loopInf", [["e.trd.tsk", "wait", [0.01], e.tag["id"]]], e.tag["id"]]]
c = CGE.CGESession("S0", [a], ["c", ""])
d = CGE.CGESession("S1", [e], ["c", ""])
b = CGE.CrossSessionHandler("CSH", [c, d])
b.start()
f = None
noReprint = True
while True:
    try:
        if noReprint:
            print(b.sessionList[1].objList[1])
            noReprint = False

    except IndexError:
        pass
