import re
class operationNotPossible(Exception):
    def __init__(self, expression, message = "one or more operations are not available as listed"):
        self.expression = expression
        self.message = message

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

def areOperationsPosible(operationList):
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
                elif mode == 'e':
                    ext += char
            methods = getMethods(unpackSubObjFromExtension(objList[resolveNameToIndex(name)], ext))
            if operation[1] not in methods:
                return False

        else:
            if operation[1] not in getMethods(objList[resolveNameToIndex(operation[0])]):
                return False
    return True



def performSelectedOperation(objIndex, subOjectRefrence, operation, paramaters=[]):
    global objList
    if subOjectRefrence == None:
        if paramaters.__len__() == 0:
            try:
                getattr(objList[objIndex], operation)()
            except:
                print("selected operation not posible with selected paramaters")
        else:
            try:
                getattr(objList[objIndex], operation)(*paramaters)
            except:
                print("selected operation not posible with selected paramaters")
    else:
        subObj = unpackSubObjFromExtension(objList[objIndex], subOjectRefrence)
        if paramaters.__len__() == 0:
            try:
                getattr(subObj, operation)()
            except:
                print("selected operation not posible with selected paramaters")
        else:
            try:
                getattr(subObj, operation)(*paramaters)
            except:
                print("selected operation not posible with selected paramaters")
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

def update():
    global objList
    operationList = getOperations()
    if not areOperationsPosible(operationList):
        raise operationNotPossible
    #run ops
