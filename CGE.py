# The Content Generation engine
# objects in objList are simulated and run based on the instructions in trd.tsk
# Module type: prog
# task > CGE
# ["target(obj name)", "operation", [parameters]]
# CGE > sceneScript
# ["sender","target","operation",[parameters]]
import re
import object
import warnings
import prog.idGen as idGen


# list of objects to iterate
objList = []
# scene to save changes to
scene = object.scene()


# get the attributes of obj as a list
# obj(obj)*
# attributes([str])
def getAtribs(obj):
    objDict = str(obj.__dict__.keys())
    stringList = str(re.search(r"'.*'", objDict).group())
    words = []
    word = ''
    for char in stringList:
        if char == '\'' or char == "\"" or char == ' ':
            continue
        if char == ',':
            words.append(word)
            word = ''
        else:
            word += char
    words.append(word)
    return words


# get the methods of an object
# obj(obj)*
# methodList([str])
def getMethods(obj):
    atribsList = getAtribs(obj)
    methodList = dir(obj)
    finalList = []
    for method in methodList:
        if method[0] == '_':
            continue
        if method in atribsList:
            continue
        finalList.append(method)
    return finalList


# get the operations that CGE needs to prform this shift
# No inputs
# operationList([operations])
def getOperations():
    global objList
    operationList = []
    for obj in objList:
        try:
            for operation in obj.trd.tsk.current:
                operationList.append(operation)
        except AttributeError:
            warnings.warn(
                "the object " + obj.tag["name"] + "does not have a threadModules and/or tasker \n please add one "
                                                  "if you want the object to do something",
                objectDoesNotContainTsk)
    return operationList


# resolve the object's id to its position in the objList
# objectId(str)*
# index(int)
def resolveIdToIndex(objId):
    global objList
    if objList.__len__() == 1:
        return 0
    ndx = 0
    for obj in objList:
        # print(name == obj.tag["name"], name, obj.tag["name"])
        if objId == obj.tag["id"]:
            break
        ndx += 1
    return ndx


# returns true if all methods in the operation list are usable on the target object
# operationList([operation])*
# operationsPossible(bool)
def areOperationsPossible(operationList):
    global objList
    for operation in operationList:
        if '.' in operation[0]:
            objId = ""
            ext = ""
            mode = 'n'
            for char in operation[0]:
                if char == '.' and mode == 'n':
                    mode = '.'
                if char == '.' and mode == '.':
                    mode = 'e'
                if mode == 'n':
                    objId += char
                if mode == 'e':
                    ext += char
            ext = ext[1:]
            methods = getMethods(unpackSubObjFromExtension(objList[resolveIdToIndex(objId)], ext))
            if operation[1] not in methods:
                raise operationNotPossible(str(operation[1]) + " not in " + str(objId + '.' + ext) + " method list")

        else:
            if operation[1] not in getMethods(objList[resolveIdToIndex(operation[0])]):
                return False
    return True


# apply the operation to the target object
# object index(int)*, method to apply(str)*, refrencees to sub objects(str), paramaters for the method([any])
# No output
def performSelectedOperation(objIndex, method, subObjectReference=None, parameters=None):
    if parameters is None:
        parameters = []
    global objList
    if subObjectReference is None:
        if parameters.__len__() == 0:
            try:
                getattr(objList[objIndex], method)()
            except:
                raise operationNotPossible("getattr(objList[objIndex], operation)()")
        else:
            try:
                getattr(objList[objIndex], method)(*parameters)
            except:
                raise operationNotPossible("getattr(objList[objIndex], operation)(*parameters)")
    else:
        # print(objIndex)
        subObj = unpackSubObjFromExtension(objList[objIndex], subObjectReference)
        if parameters.__len__() == 0:
            try:
                getattr(subObj, method)()
            except:
                raise operationNotPossible("getattr(subObj, operation)()")
        else:
            try:
                getattr(subObj, method)(*parameters)
            except:
                raise operationNotPossible("getattr(subObj, operation)(*parameters)")
        objList[objIndex] = repackSubToFull(objList[objIndex], subObj, subObjectReference)


# get a subobject from its extension
# obj(obj)*, subObjRefrence(str)*
# subObj(obj)
def unpackSubObjFromExtension(obj, subObjReference):
    subs = []
    sub = ""
    for char in subObjReference:
        if char == '.':
            subs.append(sub)
            sub = ""
        else:
            sub += char
    subs.append(sub)
    extractedObj = obj
    for subObj in subs:
        extractedObj = getattr(extractedObj, subObj)
    return extractedObj


# take an updated subObj and put it into the original obj
# fullObj(obj)*, subObj(obj)*, subObjRefrence(str)*
# fullObj(obj)
def repackSubToFull(fullObj, subObj, subObjReference):
    subs = []
    sub = ""
    for char in subObjReference:
        if char == '.':
            subs.append(sub)
            sub = ""
        else:
            sub += char
    subs.append(sub)
    currentSub = subs[-1]
    subs.pop(-1)

    while subs:
        extractedObj = fullObj
        for subObjs in subs:
            extractedObj = getattr(extractedObj, subObjs)
        setattr(extractedObj, currentSub, subObj)
        subObj = extractedObj
        currentSub = subs[-1]
        subs.pop(-1)
    setattr(fullObj, currentSub, subObj)
    return fullObj


# preps the objList for the next shift
# No input
# No output
def moveThreadAlong():
    global objList
    objsEmpty = 0
    for obj in objList:
        if obj.trd.tsk.profiles.__len__() == 0:
            objsEmpty = 0
        try:
            obj.trd.tsk.nextCurrent()
        except AttributeError:
            pass
    print("shift completed")
    if objsEmpty == objList.__len__():
        print("all object's threads empty \ndumping objects from list")
        objList = []


# adds obj to the objList
# obj(obj)*
# No output
def addObj(obj):
    global objList
    objList.append(obj)


# save the state of the objList as the inital state of a scene, with optional container setting
# cont(container)
# No output
def saveSceneInit(cont=None):
    global scene, objList
    if cont is not None:
        scene.loc = cont
    scene.obj = objList


# get the finished scene recording
# timeLine information([str])*, scene name(str)*, universe to gen id(uni)*
# scene(scene)
def exportScene(tlInfo, name, universe):
    global scene
    scene.scp[0] = tlInfo
    scene.tag["name"] = name
    scene.tag["id"] = idGen.generateUniversalId(universe, scene)
    return scene


# todo finish doc
def update(saveToScene=False):
    global objList
    if not objList:
        return "No objects to process"
    objIdx = 0
    for _ in objList:
        if not objList[objIdx].trd.tsk.current:
            continue
        if not isinstance(objList[objIdx].trd.tsk.current[0], list):
            objList[objIdx].trd.tsk.current[0] = [objList[objIdx].trd.tsk.current[0]]
        objIdx += 1
    operationList = getOperations()
    # if not
    areOperationsPossible(operationList)
    # raise operationNotPossible(operationList)
    if saveToScene:
        scene.scp.append(operationList)
    for op in operationList:
        objId = ""
        ext = ""
        mode = 'n'
        if '.' in op[0]:
            for char in op[0]:
                if char == '.' and mode == 'n':
                    mode = '.'
                if char == '.' and mode == '.':
                    mode = 'e'
                if mode == 'n':
                    objId += char
                if mode == 'e':
                    ext += char
            if ext == "":
                ext = None
            else:
                ext = ext[1:]
            pass
        if ext == "":
            objId = op[0]
            # print("pso: ", name)
            performSelectedOperation(resolveIdToIndex(objId), op[1], None, op[2])
        else:
            performSelectedOperation(resolveIdToIndex(objId), op[1], ext, op[2])
        if "evLog" in objList[resolveIdToIndex(objId)].tag.keys():
            objList[resolveIdToIndex(objId)].tag["evLog"].append(op[1])
        else:
            objList[resolveIdToIndex(objId)].tag.update({"evLog": [op[1]]})

    moveThreadAlong()


def updateWithGoal(objId, subObjReference, comparator, goal, saveToScene=False):
    global objList
    if subObjReference is not None:
        test = unpackSubObjFromExtension(resolveIdToIndex(objId), subObjReference)
        del test
    if subObjReference is None:
        while goal != resolveIdToIndex(objId):
            update(saveToScene)
    elif comparator == '==':
        while goal != unpackSubObjFromExtension(resolveIdToIndex(objId), subObjReference):
            update(saveToScene)
    elif comparator == '!=':
        while goal == unpackSubObjFromExtension(resolveIdToIndex(objId), subObjReference):
            update(saveToScene)
    elif comparator == '>':
        while goal <= unpackSubObjFromExtension(resolveIdToIndex(objId), subObjReference):
            update(saveToScene)
    elif comparator == '<':
        while goal >= unpackSubObjFromExtension(resolveIdToIndex(objId), subObjReference):
            update(saveToScene)
    elif comparator == '>=':
        while goal < unpackSubObjFromExtension(resolveIdToIndex(objId), subObjReference):
            update(saveToScene)
    elif comparator == '<=':
        while goal != unpackSubObjFromExtension(resolveIdToIndex(objId), subObjReference):
            update(saveToScene)
    else:
        print("the comparator inputted is not valid")


class operationNotPossible(Exception):
    def __init__(self, expression, message="one or more operations are not available as writen"):
        self.expression = expression
        self.message = message


class objectDoesNotContainTsk(Warning):
    pass


if __name__ == "__main__":
    print("ContentGenerationEngine11.0")
