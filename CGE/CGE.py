import re


# import object
# import atribs.thread
# import thread.tasker

# task > CGE
# ["target(obj name)", "operation", [parameters]]

# CGE > sceneScript
# ["sender","target","operation",[parameters]]

# g = object.object(None, atribs.thread.trd(None, thread.tasker.tsk([["test3"]], []), None, None, None, None, None,
# None, None), {"name": "test/g"})

# f = object.object(None, atribs.thread.trd(None, thread.tasker.tsk([["test1"], ["test2"]]), None, None, None, None,
#  None, None, None), {"name": "test/f"})

# testObjList = [g, f]


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
