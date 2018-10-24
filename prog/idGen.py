# id generation for objects
# module type: prog
import object
import warnings


# generate an object id with its uni as a base
# uni(uni)*, obj(obj)*
# objId(str)
def generateUniversalId(uni, obj):
    genIdPreChk = 0
    objList = []
    for subList in [uni.obj, uni.scn, uni.cont]:
        for objS in subList:
            objList.append(objS)
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
        objTypeLetter = 'ol'
    genId = uni.tag["name"] + '/' + objTypeLetter + "/" + str(genIdPreChk) + str(chkSumRes)
    return genId


# generates am id for obj using ovjList as a base
# objList([obj])*, obj(obj)*
# objId(str)
def generateGenericId(objList, obj):
    genIdPreChk = 0
    if objList is None:
        objList = []
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


#
#
#
def generateCaseId(caseList):
    genIdPreChk = 0
    if caseList is None:
        caseList = []
    for listObj in caseList:
        try:
            _ = listObj.tag["caseInfo"]["id"]
        except AttributeError:
            warnings.warn(print(
                "while assigning an ID, a case in the list given was found without an ID\n does it have a "
                "tag?",
                listObjDoesNotHaveAnId))
        except KeyError:
            warnings.warn(print(
                "while assigning an ID, a case in the list given was found without an ID\n does it have a "
                "tag?",
                listObjDoesNotHaveAnId))
        if listObj.tag["caseInfo"]["id"] is None:
            pass
        else:
            idFromObj = str(listObj.tag["caseInfo"]["id"])
            idFromObj = int(idFromObj[:-1])
            if idFromObj >= genIdPreChk:
                genIdPreChk = idFromObj + 1
    chkSumRes = genIdPreChk % 10
    genId = str(genIdPreChk) + str(chkSumRes)
    return genId


# a warning in case an object doesnt have an id
# No attributes
class listObjDoesNotHaveAnId(Warning):
    pass


# info at run
if __name__ == "__main__":
    print("id generation for objects\nmodule type: prog")
