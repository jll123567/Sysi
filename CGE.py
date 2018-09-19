import re
import object
import warnings

# task > CGE
# ["target(obj name)", "operation", [parameters]]


# CGE > sceneScript
# ["sender","target","operation",[parameters]]


objList = []
scene = object.scene()


# noinspection PyPep8Naming
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


# noinspection PyPep8Naming
def getMethods(obj):
    # noinspection PyPep8Naming
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


def getOperations():
    global objList
    operationList = []
    for obj in objList:
        try:
            for operation in obj.trd.tsk.current:
                operationList.append(operation)
        except AttributeError:
            warnings.warn("the object " + obj.tag["name"] + "does not have a thread and/or tasker \n please add one "
                                                            "if you want the object to do something",
                          objectDoesNotContainTsk)
    return operationList


def resolveNameToIndex(name):
    global objList
    if objList.__len__() == 1:
        return 0
    ndx = 0
    for obj in objList:
        # print(name == obj.tag["name"], name, obj.tag["name"])
        if name == obj.tag["name"]:
            break
        ndx += 1
    return ndx


def areOperationsPossible(operationList):
    global objList
    for operation in operationList:
        if '.' in operation[0]:
            name = ""
            ext = ""
            mode = 'n'
            for char in operation[0]:
                if char == '.' and mode == 'n':
                    mode = '.'
                if char == '.' and mode == '.':
                    mode = 'e'
                if mode == 'n':
                    name += char
                if mode == 'e':
                    ext += char
            ext = ext[1:]
            methods = getMethods(unpackSubObjFromExtension(objList[resolveNameToIndex(name)], ext))
            if operation[1] not in methods:
                raise operationNotPossible(str(operation[1]) + " not in " + str(name + '.' + ext) + " method list")

        else:
            if operation[1] not in getMethods(objList[resolveNameToIndex(operation[0])]):
                return False
    return True


#
def performSelectedOperation(objIndex, operation, subObjectReference=None, parameters=None):
    if  parameters is None:
        parameters = []
    global objList
    if subObjectReference is None:
        if parameters.__len__() == 0:
            try:
                getattr(objList[objIndex], operation)()
            except:
                raise operationNotPossible("getattr(objList[objIndex], operation)()")
        else:
            try:
                getattr(objList[objIndex], operation)(*parameters)
            except:
                raise operationNotPossible("getattr(objList[objIndex], operation)(*parameters)")
    else:
        # print(objIndex)
        subObj = unpackSubObjFromExtension(objList[objIndex], subObjectReference)
        if parameters.__len__() == 0:
            try:
                getattr(subObj, operation)()
            except:
                raise operationNotPossible("getattr(subObj, operation)()")
        else:
            try:
                getattr(subObj, operation)(*parameters)
            except:
                raise operationNotPossible("getattr(subObj, operation)(*parameters)")
        objList[objIndex] = repackSubToFull(objList[objIndex], subObj, subObjectReference)


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


def addObj(obj):
    global objList
    objList.append(obj)


def saveSceneInit(cont=None):
    global scene, objList
    if cont is not None:
        scene.loc = cont
    scene.obj = objList


def exportScene(tlInfo, name):
    global scene
    scene.scp[0] = tlInfo
    scene.tag["name"] = name
    return scene


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
        name = ""
        ext = ""
        mode = 'n'
        if '.' in op[0]:
            for char in op[0]:
                if char == '.' and mode == 'n':
                    mode = '.'
                if char == '.' and mode == '.':
                    mode = 'e'
                if mode == 'n':
                    name += char
                if mode == 'e':
                    ext += char
            if ext == "":
                ext = None
            else:
                ext = ext[1:]
            pass
        if ext == "":
            name = op[0]
            # print("pso: ", name)
            performSelectedOperation(resolveNameToIndex(name), op[1], None, op[2])
        else:
            performSelectedOperation(resolveNameToIndex(name), op[1], ext, op[2])
        if "evLog" in objList[resolveNameToIndex(name)].tag.keys():
            objList[resolveNameToIndex(name)].tag["evLog"].append(op[1])
        else:
            objList[resolveNameToIndex(name)].tag.update({"evLog": [op[1]]})

    moveThreadAlong()


def updateWithGoal(objName, subObjReference, comparator, goal, saveToScene=False):
    global objList
    if subObjReference is not None:
        test = unpackSubObjFromExtension(resolveNameToIndex(objName), subObjReference)
        del test
    if subObjReference is None:
        while goal != resolveNameToIndex(objName):
            update(saveToScene)
    elif comparator == '==':
        while goal != unpackSubObjFromExtension(resolveNameToIndex(objName), subObjReference):
            update(saveToScene)
    elif comparator == '!=':
        while goal == unpackSubObjFromExtension(resolveNameToIndex(objName), subObjReference):
            update(saveToScene)
    elif comparator == '>':
        while goal <= unpackSubObjFromExtension(resolveNameToIndex(objName), subObjReference):
            update(saveToScene)
    elif comparator == '<':
        while goal >= unpackSubObjFromExtension(resolveNameToIndex(objName), subObjReference):
            update(saveToScene)
    elif comparator == '>=':
        while goal < unpackSubObjFromExtension(resolveNameToIndex(objName), subObjReference):
            update(saveToScene)
    elif comparator == '<=':
        while goal != unpackSubObjFromExtension(resolveNameToIndex(objName), subObjReference):
            update(saveToScene)
    else:
        print("the comparator inputted is not valid")


class operationNotPossible(Exception):
    def __init__(self, expression, message="one or more operations are not available as writen"):
        self.expression = expression
        self.message = message


class objectDoesNotContainTsk(Warning):
    pass
