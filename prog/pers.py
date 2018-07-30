# setup
# [limits,goals,functions,dict]
# "functname()"
# goals are bool checks that a atribs attempts to mke true and are in urgency order
# limits are similar but are meant to not be made true and are still in urgency order
# tasker profile(auto-get)
# {"word": refrenceCount(int), "...": ...}

##this is a tool to debug Usr.prs, dont use this regularly##

def setPrs(usr, limit, goal, funct, usrDict):
    usr.prs = [limit, goal, funct, usrDict]
    return usr


def updateDict(usr, usrDict):
    usr.prs[3] = usrDict
    return usr


def newGoal(usr, goal, index):
    usr.prs[1].insert(index, goal)
    return usr


def newLimit(usr, limit, index):
    usr.prs[2].insert(index, limit)
    return usr


def newFunction(usr, funct):
    usr.prs[0].append(funct)
    return usr


def removeGoal(usr, index):
    usr.prs[1].pop(index)
    return usr


def removeLimit(usr, index):
    usr.prs[2].pop(index)
    return usr


def removeFunction(usr, index):
    usr.prs[0].pop(index)
    return usr


def clearPrs(usr):
    usr.prs = [0, 0, 0]
    return usr


"""Terms:
    aimless:atribs has no goals
    unsatisfied:atribs has one or more unsolvable goals
    satisfied:atribs has met all goals
    unlimited:atribs has no limiters
    limited:atribs has limiters
    simulated:object has  a unofficial pers
    404<term>:cannot get <term>
    Conflicted:atribs cannot complete a goal w/o satisfying a limiter
    observe:has std observer functions
    admin:has all possible functions(within a certain context)
    jailed:does not have some or any standard atribs functions
   Note:
       pers only helps predict atribs behavior and may be slightly inaccurate due to system run location(you can only guess what you know.)"""

# runtime
if __name__ == "__main__":
    print("pers def and functionsv10.0")
