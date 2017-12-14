#import

#setup
#useable functions,goals,limits
    #"functname()"
    # goals are bool cheks that a user attempts to mke true and are in urgency order
    #limits are similar but are meant to not be made true and are still in urgency order
    #tasker profile(aauto-get)

def set(usr,goal,limit,funct):
    usr.prs=[funct,goal,limit,usr.trd["tsk"]]

def newGoal(usr,goal,index):
    usr.prs[1].insert(index,goal)

def newLimit(usr,limit,index):
    usr.prs[2].insert(index,limit)
    
def newFunction(usr,funct):
    usr.prs[0].append(funct)
    
def removeGoal(usr,index):
    usr.prs[1].pop(index)

def removeLimit(usr,index):
    usr.prs[2].pop(index)
    
def removeFunction(usr,index):
    usr.prs[0].pop(index)

def updateProfile(usr):
    usr.prs[3]=usr.trd["tsk"]
    
def clear(usr):
    usr.prs=[0,0,0]
"""Terms:
    aimless:user has no goals
    unsatisfied:user has one or more unsolveable goals
    satisfied:user has met all goals
    unlimited:user has no limiters
    limited:user has limiters
    simulated:object has  a unoffical pers
    404<term>:cannot get <term>
    Conflicted:user cannot complete a goal w/o satisfying a limiter
    observe:has std ovbserer functions
    admin:has all posible functions(within a certain context)
    jailed:does not have some or any standard user functions
   Note:
       pers olny helps predict user behavio and may be slightly inacurate due to system run location(you can only guess what you know.)"""

#runtime
if __name__ == "__main__":
    print("pers def and functionsv10.0")