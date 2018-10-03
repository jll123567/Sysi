# definition for scenePlayback(but its not working)
# Module type: broke
# todo: fix and doc me
import object
import prog.idGen


class sceneList(object.data):
    def __init__(self, storage=None, tag=None):
        if storage is None:
            storage = []
        if tag is None:
            tag = {"name": None, "id": None}
        super().__init__(storage, tag)

    def loadScene(self, scn):
        self.storage.append(scn)

    def newScene(self, newScp=None, newObj=None,
                 newLoc=object.container([None, 0, 0, 0], ["h,0,0,0-0,0,0"], {"name": "defaultContainer", "id": None}),
                 newTag=None):
        if newScp is None:
            newScp = []
        if newObj is None:
            newObj = []
        if newTag is None:
            newTag = {"name": "emptyScene", "id": None}
        scn = object.scene(newScp, newObj, newLoc, newTag)
        scn.tag.update({"id": prog.idGen.generateGenericId(self.storage, scn)})
        self.storage.append(scn)

    def loadObj(self, index, obj):
        self.storage[index].obj.append(obj)

    def unloadObj(self, sceneIndex, objIndex):
        self.storage[sceneIndex].obj.pop(objIndex)

    def switchScript(self, script, index):
        self.storage[index].scp = script

    def runScene(self, index):
        count = 0
        s = self.storage[index]
        for i in s.scp:
            if s.tag["paused"]:
                print("paused")
            else:
                print(count, ":", i)
                count += 1

    def switchCont(self, index, cont):
        self.storage[index].loc = cont

    # noinspection PyTypeChecker
    def pause(self):
        if not self.tag["paused"]:
            self.tag["paused"] = True
        else:
            self.tag["paused"] = False


# runtime
if __name__ == "__main__":
    print(" scene handle v11.0")
    f = sceneList()
    f.newScene()
