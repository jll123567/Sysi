# a small bug tracker like thing
# module type: prog
import error

# error queue(fill with err)
queue = []
inProgress = {}
cases = []


# queues and resolves a list of errors
# errs([err])*
# Console output(str)
def errorResolve(userId):
    global inProgress
    idx = 0
    for errs in inProgress[userId]:
        errs.resolveError()
        inProgress[userId].pop(idx)
        idx += 1
    print("queue completed, closing")


# populate the queue
# uni(uni)*
# none
def populateQueue(uni):
    global queue
    for scn in uni.scn:
        for obj in scn:
            if isinstance(obj, error.err):
                queue.append(obj)


#
#
#
def assignErrors(userId, idxList):
    global inProgress, queue
    errList = []
    for idx in idxList:
        errList.append(queue[idx])
        queue.pop(idx)
    inProgress.update({userId: errList})


# info at run
if __name__ == "__main__":
    print("a small bug tracker like thing\nmodule type: prog")
