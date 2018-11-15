import time
import object
import CGE
a = object.object()
a.tag["id"] = "o/00"
a.trd.tsk.current = [[a.tag["id"]+".trd.tsk", "debugPrint", ["hey hey 1 2 3"]]]
session = CGE.CGESession("session0", [a])
session.run(2)