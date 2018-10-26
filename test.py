import object
import CGE
import prog.idGen as idGen

a = object.object()
b = object.object()
sc = object.scene()
sc.obj = [a, b]
for idx in range(0, 1):
    sc.obj[idx].tag["id"] = idGen.generateGenericId(sc.obj, sc.obj[idx])
sc.scp = [None, [[sc.obj[0].tag["id"]+".trd.tsk", "debugPrint", ["sh0 op0"]], [sc.obj[0].tag["id"]+".trd.tsk", "debugPrint", ["sh0 op1"]]], [[sc.obj[0].tag["id"]+".trd.tsk", "debugPrint", ["sh1 op0"]], [sc.obj[0].tag["id"]+".trd.tsk", "debugPrint", ["sh1 op1"]]]]
CGE.replayScene(sc)
