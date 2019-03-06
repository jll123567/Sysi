"""don't mind me, just being dumb"""
import CGE
import object
import thread_modules.ram
a = object.object()
a.tag["id"] = "a"
a.trd.tsk.current = [["CSH", "crossWarp", ["S1"], a.tag["id"]]]
e = object.object()
e.tag["id"] = "e"
e.trd.ram = thread_modules.ram.ram()
e.trd.tsk.current = [["e.trd.tsk", "loopInf", [["e.trd.tsk", "wait", [0.01], e.tag["id"]]], e.tag["id"]]]
c = CGE.CGESession("S0", [a], ["t", ""])
d = CGE.CGESession("S1", [e], ["t", ""])
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
