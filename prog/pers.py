# usable functions,goals,limits
# "functname()"
# goals are bool checks that a user attempts to mke true and are in urgency order
# limits are similar but are meant to not be made true and are still in urgency order
# tasker profile(auto-get)


def set(usr, goal, limit, funct):
    usr.prs = [funct, goal, limit, usr.trd["tsk"]]


def newGoal(usr, goal, index):
    usr.prs[1].insert(index, goal)


def newLimit(usr, limit, index):
    usr.prs[2].insert(index, limit)


def newFunction(usr, funct):
    usr.prs[0].append(funct)


def removeGoal(usr, index):
    usr.prs[1].pop(index)


def removeLimit(usr, index):
    usr.prs[2].pop(index)


def removeFunction(usr, index):
    usr.prs[0].pop(index)


def updateProfile(usr):
    usr.prs[3] = usr.trd["tsk"]


def clear(usr):
    usr.prs = [0, 0, 0]


"""Terms:
    aimless:user has no goals
    unsatisfied:user has one or more unsolvable goals
    satisfied:user has met all goals
    unlimited:user has no limiters
    limited:user has limiters
    simulated:object has  a unofficial pers
    404<term>:cannot get <term>
    Conflicted:user cannot complete a goal w/o satisfying a limiter
    observe:has std observer functions
    admin:has all possible functions(within a certain context)
    jailed:does not have some or any standard user functions
   Note:
       pers only helps predict user behavior and may be slightly inaccurate due to system run location(you can only guess what you know.)"""


if __name__ == "__main__":
    print("pers def and functions v10.0")


# by jacob ledbetter
