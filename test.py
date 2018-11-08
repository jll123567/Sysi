import CGE
import object

f = object.object()
g = object.universe()
g.rule.append([".trd.tsk", "debugPrint", ["fff"]])
f.tag["id"] = "o/00"
g.tag["id"] = "un/untitled"
CGE.objList = [f]
CGE.addUniRules(g)
CGE.update()
