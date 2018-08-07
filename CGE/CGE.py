import re


# task > CGE
# ["target(obj name)", "operation", [paramaters]]

# CGE > sceneScript
# ["sender","traget","oepration",[paramaters]]

objList = []

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


def getOperations(objList):
    operationList = []
    for obj in objList:
        for operation in obj.trd.tsk.current:
            operationList.append(operation)
    return operationList

def performSelectedOperation(objIndex, subOjectRefrence, operation, paramaters=[]):
    global objList
    if subOjectRefrence == None:
        if paramaters.__len__() == 0:
            getattr(objList[objIndex], operation)()
        else:
            getattr(objList[objIndex], operation)(*paramaters)
    else:
        subObj = unpackSubObjFromExtension(objList[objIndex], subOjectRefrence)
        if paramaters.__len__() == 0:
            getattr(subObj, operation)()
        else:
            getattr(subObj, operation)(*paramaters)
        objList[objIndex] = repackSubToFull(objList[objIndex], subObj, subOjectRefrence)


def unpackSubObjFromExtension(obj, subObjRefrence):
    subs = []
    sub = ""
    for char in subObjRefrence:
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

def repackSubToFull(fullObj, subObj, subObjRefrence):
    subs = []
    sub = ""
    for char in subObjRefrence:
        if char == '.':
            subs.append(sub)
            sub = ""
        else:
            sub += char
    subs.append(sub)
    currentSub = subs[-1]
    subs.pop(-1)

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