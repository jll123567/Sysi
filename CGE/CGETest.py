import object
import thread.tasker
import thread.move
import atribs.model
import atribs.thread
import CGE

objList = [
    object.object(atribs.model.sysModel(), atribs.thread.trd(None, thread.tasker.tsk(), None, thread.move.mov(), None,
                                                             None), {"name": "test/0"}),
    object.object(atribs.model.sysModel(),
                  atribs.thread.trd(None, thread.tasker.tsk(), None, thread.move.mov(1, 1, 1, 0, 0, 0), None,
                                    None), {"name": "test/1"})
]

for obj in objList:
    if obj.tag["name"] == "test/0":
        print("object 0")
        print("setting current profile([[test/0.trd.mov, warp, [2, 2, 2]]])")
        objList[0].trd.tsk.setCurrentProfile([["test/0.trd.mov", "warp", [2, 2, 2]]])

    if obj.tag["name"] == "test/1":
        print("object 1")
        print("setting current profile([[test/1.trd.mov, accelerate, [3, 3, 3]], [test/1.trd.mov, move, ()]])")
        objList[1].trd.tsk.setCurrentProfile([["test/1.trd.mov", "accelerate", [1, 1, 1]], ["test/1.trd.mov", "move",
                                                                                            []]])
        print("set next instruction to continue moving")
        objList[1].trd.tsk.profiles = [[["test/1.trd.mov", "move", []], ["test/1.trd.tsk", "loop",
                                                                         [["test/1.trd.mov", "move", []]]]]]
CGE.objList = [objList[1]]
while CGE.objList[0].trd.mov.x < 100:
    CGE.update()
    print(CGE.objList[0].trd.mov.x)


class weirdObjWithCustomFunct(object.object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def printTheText():
        print("theText")


CGE.objList = []
g = weirdObjWithCustomFunct()
g.tag["name"] = "test/2"
g.trd.tsk.setCurrentProfile([[g.tag["name"], "printTheText", []]])
CGE.addObj(g)
CGE.addObj(object.scene([[0, None, 30]], [], None, {"name": "test/embeddedScene"}))
CGE.saveSceneInit()
# breakpoint()
for i in range(0, 3):
    CGE.update(True)
coolScene = CGE.exportScene([0, None, 30], "test/coolScene")
print("a")
