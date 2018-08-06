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
        objList[1].trd.tsk.setCurrentProfile([["test/1.trd.mov", "accelerate", [3, 3, 3]], ["test/1.trd.mov", "move",
                                                                                            "()"]])
        print("set next instruction to continue moving")
        objList[1].trd.tsk.addProfile([["test/1.trd.mov", "move", "()"], ["test/1.trd.tsk", "loop",
                                                                          [["test/1.trd.mov", "move", "()"]]]])
