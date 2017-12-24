# import
import object

# setup
loadedScenes = []
paused = False


def loadScene(scn):
    global loadedScenes
    loadedScenes.append(scn)


def newScene(scp, obj, loc, tag):
    global loadedScenes
    loadedScenes.append(object.scene(scp, obj, loc, tag))


def closeScene(index, usr):
    global loadedScenes
    usr[0].mem.append(loadedScenes[index])
    loadedScenes.pop(index)
    return usr


def loadObj(index, obj):
    global loadedScenes
    loadedScenes[index].obj.append(obj)


def unloadObj(sceneIndex, objIndex):
    global loadedScenes
    loadedScenes[sceneIndex].obj.pop(objIndex)


def addScript(script, index):
    global loadedScenes
    loadedScenes[index].scp = script


def runScene(index):
    global loadedScenes, paused
    count = 0
    for i in loadedScenes[index].scp:
        if paused:
            print("paused")
        else:
            print(count, ":", i)
            count += 1


def switchCont(index, cont):
    global loadedScenes
    loadedScenes[index].loc = cont


def pause():
    global paused
    if not paused:
        paused = True
    else:
        paused = False


def free(index, usr):
    global loadedScenes
    isFree = True
    while isFree:
        loadedScenes[index].scp.append(input(">\\"))
        if loadedScenes[index].scp[-1] == "close()":
            isFree = False
    closeScene(index, usr)
    return usr


# runtime
if __name__ == "__main__":
    print(" scene handle v10.0")
