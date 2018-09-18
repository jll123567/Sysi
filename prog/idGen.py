import object


# TODO: make the ID generator dummy
def generateUniversalId(uni, obj):
    genIdPreChk = 0
    for uniObj in uni.obj:
        idFromObj = str(uniObj.tag["id"])
        slashCnt = 0
        idFromObjProcessed = ""
        for charater in idFromObj:
            if slashCnt == 2:
                idFromObjProcessed += charater
            if charater == '/':
                slashCnt += 1
        idFromObjProcessed = int(idFromObjProcessed[:-1])
        if idFromObjProcessed >= genIdPreChk:
            genIdPreChk = idFromObjProcessed + 1
    chkSumRes = genIdPreChk % 9
    if isinstance(obj, object.object):
        objTypeLett = 'o'
    elif isinstance(obj, object.user):
        objTypeLett = 'u'
    elif isinstance(obj, object.weapon):
        objTypeLett = 'w'
    elif isinstance(obj, object.data):
        objTypeLett = 'd'
    elif isinstance(obj, object.container):
        objTypeLett = 'c'
    elif isinstance(obj, object.scene):
        objTypeLett = 's'
    elif isinstance(obj, object.universe):
        objTypeLett = 'un'
    else:
        objTypeLett = 'o'
    genId = uni.tag["name"] + '/' + objTypeLett + "/" + str(genIdPreChk) + str(chkSumRes)
    return genId
