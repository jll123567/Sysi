import CGE
import object
import threadModules.ram
a = object.object()
a.tag["id"] = "a"
a.trd.tsk.current = [["CSH", "crossWarp", ["S1"], a.tag["id"]]]
e = object.object()
e.tag["id"] = "e"
e.trd.ram = threadModules.ram.ram()
e.trd.tsk.current = [["e.trd.tsk", "loopInf", [["e.trd.tsk", "wait", [0.01], e.tag["id"]]], e.tag["id"]]]
c = CGE.CGESession("S0", [a], ["t", ""])
d = CGE.CGESession("S1", [e], ["t", ""])
# breakpoint()
# b = CGE.CrossSessionHandler("CSH", [c, d])
# b.start()
# while True:
#     try:
#         print(b.sessionList[1].objList[1])
#     except IndexError:
#         pass
