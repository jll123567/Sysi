# import
import object


# setup
# noinspection PyDefaultArgument
class sceneList(object.data):
    def __init__(self, storage=None, tag={"name": None}):
        super(sceneList, self).__init__()
        self.storage = storage
        self.tag = tag

    def loadScene(self, scn):
        self.storage.append(scn)

    def newScene(self, newScp=[], newObj=[],
                 newLoc=object.container([None, 0, 0, 0], ["h,0,0,0-0,0,0"], {"name": "defaultContainer"}),
                 newTag={"name": "emptyScene"}):
        self.storage.append(object.scene(newScp, newObj, newLoc, newTag))

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
    print(" scene handle v10.0")
