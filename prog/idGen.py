import object
import warnings


# TODO: make the ID generator dummy
def generateUniversalId(uni, obj):
    genIdPreChk = 0
    for uniObj in uni.obj:
        if uniObj.tag["id"] is None:
            pass
        else:
            idFromObj = str(uniObj.tag["id"])
            slashCnt = 0
            idFromObjProcessed = ""
            for character in idFromObj:
                if slashCnt == 2:
                    idFromObjProcessed += character
                if character == '/':
                    slashCnt += 1
            idFromObjProcessed = int(idFromObjProcessed[:-1])
            if idFromObjProcessed >= genIdPreChk:
                genIdPreChk = idFromObjProcessed + 1
    chkSumRes = genIdPreChk % 10
    if isinstance(obj, object.object):
        objTypeLetter = 'o'
    elif isinstance(obj, object.user):
        objTypeLetter = 'u'
    elif isinstance(obj, object.weapon):
        objTypeLetter = 'w'
    elif isinstance(obj, object.data):
        objTypeLetter = 'd'
    elif isinstance(obj, object.container):
        objTypeLetter = 'c'
    elif isinstance(obj, object.scene):
        objTypeLetter = 's'
    elif isinstance(obj, object.universe):
        objTypeLetter = 'un'
    else:
        objTypeLetter = 'o'
    genId = uni.tag["name"] + '/' + objTypeLetter + "/" + str(genIdPreChk) + str(chkSumRes)
    return genId


def generateGenericId(objList, obj):
    genIdPreChk = 0
    for listObj in objList:
        try:
            _ = listObj.tag["id"]
        except AttributeError:
            warnings.warn(print(
                "while assigning a generic ID, an object in the list given was found without an ID\n does it have a "
                "tag?",
                listObjDoesNotHaveAnId))
        except KeyError:
            warnings.warn(print(
                "while assigning a generic ID, an object in the list given was found without an ID\n does it have a "
                "tag?",
                listObjDoesNotHaveAnId))
        if listObj.tag["id"] is None:
            pass
        else:
            idFromObj = str(listObj.tag["id"])
            slashCnt = 0
            idFromObjProcessed = ""
            for character in idFromObj:
                if slashCnt == 1:
                    idFromObjProcessed += character
                if character == '/':
                    slashCnt += 1
            idFromObjProcessed = int(idFromObjProcessed[:-1])
            if idFromObjProcessed >= genIdPreChk:
                genIdPreChk = idFromObjProcessed + 1
    chkSumRes = genIdPreChk % 10
    if isinstance(obj, object.object):
        objTypeLetter = 'o'
    elif isinstance(obj, object.user):
        objTypeLetter = 'u'
    elif isinstance(obj, object.weapon):
        objTypeLetter = 'w'
    elif isinstance(obj, object.data):
        objTypeLetter = 'd'
    elif isinstance(obj, object.container):
        objTypeLetter = 'c'
    elif isinstance(obj, object.scene):
        objTypeLetter = 's'
    elif isinstance(obj, object.universe):
        objTypeLetter = 'un'
    else:
        objTypeLetter = 'o'
    genId = objTypeLetter + "/" + str(genIdPreChk) + str(chkSumRes)
    return genId


class listObjDoesNotHaveAnId(Warning):
    pass


if __name__ == "__main__":
    testUni = object.universe(None)
    testUni.obj = [object.object(), object.object(), object.object()]
    testUni.tag["name"] = "testUni"
    testUni.tag["id"] = generateUniversalId(testUni, testUni)
    for i in testUni.obj:
        i.tag.update({"id": generateUniversalId(testUni, i)})
