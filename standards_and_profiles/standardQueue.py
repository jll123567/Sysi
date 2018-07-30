# import

##ADMIN TOOL##
# setup
# separates queue into 6 smaller queues that follow each other
def addStdQueue(usr):
    std = {"status": [], "preservation": [], "limit": [], "command": [], "personal": [], "aimless": []}
    usr = thread.FmemMgnt.store(usr, 1, std)
    return usr


def makeValidQueue(stdQue):
    mainQueue = []
    for i in stdQue:
        mainQueue.append(i)
    return mainQueue


def makeValidTskProfile(stdQue):
    # flatten function by rightfootin
    # snippet link: https://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
        # modified to not include nested tuples as queues only support lists (or at least they're supposed to)
    mainTask = []
    for item in stdQue:
        if isinstance(item, list):
            mainTask.extend(makeValidTskProfile(item))
        else:
            mainTask.append(item)
    return mainTask


# runtime
if __name__ == "__main__":
    print("standard queue creator and converter v10.0")
