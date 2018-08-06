import re


# task > CGE
# ["target(obj name)", "operation", [paramaters]]

# CGE > sceneScript
# ["sender","traget","oepration",[paramaters]]

objList = []

# noinspection PyPep8Naming
def getAttribs(obj):
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
def getMethods(obj, atribsList):
    # noinspection PyPep8Naming
    methodList = dir(obj)
    finalList = []
    for method in methodList:
        if method[0] == '_':
            continue
        if method in atribsList:
            continue
        finalList.append(method)
    return finalList

def performSelectedOperation(objIndex, subOjectRefrence, operation, paramaters=[]):
    global objList
    if subOjectRefrence == "trd.mov":
        if paramaters.__len__() == 0:
            getattr(objList[objIndex].trd.mov, operation)()
        else:
            getattr(objList[objIndex].trd.mov, operation)(*paramaters)
    elif subOjectRefrence == "trd.tsk":
        if paramaters.__len__() == 0:
            getattr(objList[objIndex].trd.tsk, operation)()
        else:
            getattr(objList[objIndex].trd.tsk, operation)(*paramaters)
    else:
        if paramaters.__len__() == 0:
            getattr(objList[objIndex], operation)()
        else:
            getattr(objList[objIndex], operation)(*paramaters)