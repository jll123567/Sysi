# id generation for objects
# module type: prog
from old import sys_objects
import re
import warnings


# new universal id
def dynamicUniversalId(directory, sessionId, obj):
    """
    Generate an id for <obj> based on <directory> and <sessionId>.
    Use when giving an id for objects currently running in sessions.
    """
    objList = []
    for ses in directory.sessionList:  # Grab all objects from all sessions in directory
        for otherObj in ses.objList:
            objList.append(otherObj)
    if isinstance(obj, sys_objects.user):  # find if the id-less object is obj or usr
        objTypeLetter = 'u'
    else:
        objTypeLetter = 'o'
    maxCount = 0
    for extObj in objList:  # look through the object list for objects who's origin is the session and find the biggest id
        full = re.match(r"un/(.*)/[uo]/([0-9]*)[0-9]", extObj.tag["id"])
        uni = full.group(1)
        count = int(full.group(2))
        if sessionId[3:] == uni and count > maxCount:
            maxCount = count  # save that biggest id for later
    maxCount += 1  # add one to make the id's unique
    maxCount = str(maxCount)
    finalId = "un/{}/{}/{}{}".format(sessionId[3:], objTypeLetter, maxCount,
                                     maxCount[-1])  # put together the components of the new id
    return finalId


def staticUniversalId(uni, obj=None):
    """
    Use <uni> to generate an id for <obj>.
    Used to generate id's for stored objects.
    For objects currently running in sessions please use dynamicUniversalId().
    This also assumes all objects created by a particular uni are in the uni at time of id generation.
    """
    if obj is None:
        for o in uni.obj:
            if o.tag["id"] is None:
                o.tag["id"] = staticUniversalId(uni, o)
        return None
    maxCount = 0  # init shit
    for uniObj in uni.obj:  # get the number from the object
        if uniObj.tag["id"] is None:
            pass
        else:
            try:
                full = re.match(r"un/(.*)/[uodcs][n]*/([0-9]*)[0-9]", uniObj.tag["id"])
                count = int(full.group(2))
                if count > maxCount:
                    maxCount = count  # save that biggest id for later
            except AttributeError:
                raise badId
    maxCount += 1  # add one to make the id's unique
    if isinstance(obj, sys_objects.user):  # get the type letter
        objTypeLetter = 'u'
    elif isinstance(obj, sys_objects.sysObject):
        objTypeLetter = 'o'
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
    genId = "{}/{}/{}{}".format(uni.tag["id"], objTypeLetter, str(maxCount), str(maxCount)[-1])  # Put together id.
    return genId


def generateGenericId(objList, obj):
    """Generate an id with an objList and an object."""
    if objList is None:  # Make sure objList is initialized.
        objList = []
    count = 0  # Initialize count.
    for listObj in objList:  # Iterate though objList.
        try:
            _ = listObj.tag["id"]  # Make sure there is an id tag.
        except AttributeError:
            pass
        except KeyError:
            pass
        if isinstance(listObj.tag["id"], str):
            pass
        else:
            full = re.match(r"[uodcs][n]*/([0-9]*)[0-9]", listObj.tag["id"])  # Get the count.
            if count < full.group(1):
                count = full.group(1)
    count += 1  # Increment and prep count.
    count = str(count)
    if isinstance(obj, sys_objects.user):  # Get the object letter
        objTypeLetter = 'u'
    elif isinstance(obj, sys_objects.sysObject):
        objTypeLetter = 'o'
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
    genId = "{}/{}{}".format(objTypeLetter, count, count[-1])
    return genId


def generateCaseId(caseList):
    """Generate a case id."""
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


class listObjDoesNotHaveAnId(Warning):
    """A warning in case an sysObject doesnt have an id."""
    pass


class badId(Exception):
    pass
