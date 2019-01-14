import CGE
import object
a = object.object()
a.tag["id"] = "a"
a.trd.tsk.current = [["CSH", "crossWarp", ["S1"], a.tag["id"]]]
print(a.trd.tsk.current)
e = object.object()
e.tag["id"] = "e"
e.trd.tsk.current = [["e.trd.tsk", "loopInf", [["e.trd.tsk", "wait", [0.01], e.tag["id"]]], e.tag["id"]]]
print(a.trd.tsk.current)
c = CGE.CGESession("S0", [a], ["t", ""])
d = CGE.CGESession("S1", [e], ["t", ""])
print(a.trd.tsk.current)
print(e.trd.tsk.current)
breakpoint()
b = CGE.CrossSessionHandler("CSH", [c, d])
b.run()
while True:
    try:
        print(b.sessionList[1].objList[1])
    except IndexError:
        pass
