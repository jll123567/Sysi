# a small bug tracker like thing
# module type: prog
import error
import object
import prog.idGen

# error queue(fill with err)
errQueue = []
inProgress = {}
cases = []


# queues and resolves a list of errors
# errs([err])*
# Console output(str)
def errorResolve(userId=None):
    global inProgress, errQueue
    idx = 0
    if userId is None:
        for errs in errQueue:
            errs.resolveError()
            errQueue = []
        print("queue completed closing")
    else:
        for errs in inProgress[userId]:
            errs.resolveError()
            inProgress[userId].pop(idx)
            idx += 1
        print("queue completed, closing")


# populate the queue
# uni(uni)*
# none
def populateQueue(uni):
    global errQueue
    for scn in uni.scn:
        for obj in scn:
            if isinstance(obj, error.err):
                errQueue.append(obj)


#
#
#
def assignErrors(userId, idxList):
    global inProgress, errQueue
    errList = []
    for idx in idxList:
        errList.append(errQueue[idx])
        errQueue.pop(idx)
    inProgress.update({userId: errList})


#
#
#
def caseFileCompiler(userId, userName, desc, packages=None):
    global cases
    if packages is None:
        packages = []
    tags = {"dataType": "caseFile", "caseInfo": {"id": prog.idGen.generateCaseId(cases),
                                                 "userInfo": [userId, userName], "description": desc}}
    dta = object.data()
    dta.storage = packages
    dta.tag.update(tags)
    return dta


# info at run
if __name__ == "__main__":
    print("a small bug tracker like thing\nmodule type: prog")
