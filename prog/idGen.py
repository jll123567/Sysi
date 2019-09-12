# id generation for objects
# module type: prog
import sys_objects
import re
import warnings


# new universal id
def universalId(directory, sessionId, obj):
    objList = []
    for ses in directory.sessionList:  # Grab all objects from all sessions in directory
        for otherObj in ses.objList:
            objList.append(otherObj)

    if isinstance(obj, sys_objects.user):  # find if the id-less object is obj or usr
        objTypeLetter = 'u'
    else:
        objTypeLetter = 'o'
    maxCount = 0
    for extObj in objList:  # look through the object list for objects whos origin is the session and find the biggest id
        full = re.match(r"un/(.*)/[uo]/([0-9]*)[0-9]", extObj.tag["id"])
        uni = full.group(1)
        count = int(full.group(2))
        if sessionId[3:] == uni and count > maxCount:
            maxCount = count  # save that biggest id for later
    maxCount = maxCount + 1  # add one to make the id's unique
    maxCount = str(maxCount)
    finalId = "un/{}/{}/{}{}".format(sessionId[3:], objTypeLetter, maxCount,
                                     maxCount[-1])  # put together the componets of the new id
    return finalId


# generate an sysObject id with its uni as a base
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
    if isinstance(obj, sys_objects.sysObject):
        objTypeLetter = 'o'
    elif isinstance(obj, sys_objects.user):
        objTypeLetter = 'u'
    elif isinstance(obj, sys_objects.data):
        objTypeLetter = 'd'
    elif isinstance(obj, sys_objects.container):
        objTypeLetter = 'c'
    elif isinstance(obj, sys_objects.scene):
        objTypeLetter = 's'
    elif isinstance(obj, sys_objects.universe):
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
                "while assigning a generic ID, an sysObject in the list given was found without an ID\n does it have a "
                "tag?",
                listObjDoesNotHaveAnId))
        except KeyError:
            warnings.warn(print(
                "while assigning a generic ID, an sysObject in the list given was found without an ID\n does it have a "
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
    if isinstance(obj, sys_objects.sysObject):
        objTypeLetter = 'o'
    elif isinstance(obj, sys_objects.user):
        objTypeLetter = 'u'
    elif isinstance(obj, sys_objects.data):
        objTypeLetter = 'd'
    elif isinstance(obj, sys_objects.container):
        objTypeLetter = 'c'
    elif isinstance(obj, sys_objects.scene):
        objTypeLetter = 's'
    elif isinstance(obj, sys_objects.universe):
        objTypeLetter = 'un'
    else:
        objTypeLetter = 'o'
    genId = objTypeLetter + "/" + str(genIdPreChk) + str(chkSumRes)
    return genId


# get an id for cases(super generic)
# caseList([dta])*
# id(str)
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


# a warning in case an sysObject doesnt have an id
# No attributes
class listObjDoesNotHaveAnId(Warning):
    pass


# info at run
if __name__ == "__main__":
    print("id generation for objects\nmodule type: prog")
