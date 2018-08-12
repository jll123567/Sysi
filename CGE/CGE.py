import re


class operationNotPossible(Exception):
    def __init__(self, expression, message="one or more operations are not available as writen"):
        self.expression = expression
        self.message = message


# task > CGE
# ["target(obj name)", "operation", [parameters]]

# CGE > sceneScript
# ["sender","target","operation",[parameters]]

objList = []


# TODO: make a way to export a Live run and all change done through CGE to a valid scene
# also TODO: make a way to have CGE run update until a goal is reached

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
        for operation in obj.trd.tsk.current:
            operationList.append(operation)
    return operationList


def resolveNameToIndex(name):
    global objList
    ndx = 0
    for obj in objList:
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
                return False

        else:
            if operation[1] not in getMethods(objList[resolveNameToIndex(operation[0])]):
                return False
    return True


# noinspection PyDefaultArgument,PyBroadException
def performSelectedOperation(objIndex, operation, subObjectReference=None, parameters=[]):
    global objList
    if subObjectReference is None:
        if parameters.__len__() == 0:
            try:
                getattr(objList[objIndex], operation)()
            except:
                print("selected operation not possible with selected parameters")
        else:
            try:
                getattr(objList[objIndex], operation)(*parameters)
            except:
                print("selected operation not possible with selected parameters")
    else:
        subObj = unpackSubObjFromExtension(objList[objIndex], subObjectReference)
        if parameters.__len__() == 0:
            try:
                getattr(subObj, operation)()
            except:
                print("selected operation not possible with selected parameters")
        else:
            try:
                getattr(subObj, operation)(*parameters)
            except:
                print("selected operation not possible with selected parameters")
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

    # noinspection PySimplifyBooleanCheck
    while subs != []:
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
    for obj in objList:
        obj.trd.tsk.nextCurrent()
    print("shift completed")


def addObj(obj):
    global objList
    objList.append(obj)


def update():
    global objList
    operationList = getOperations()
    if not areOperationsPossible(operationList):
        raise operationNotPossible
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
        performSelectedOperation(resolveNameToIndex(name), op[1], ext, op[2])
    moveThreadAlong()
