# Description of the usr.prs attribute
# Module type:def


# user personality(general behavior guide) Goals([] of boolean expressions that define goals)*, limits([] of boolean
# expressions that define limits(goals to avoid))*, functions([] of available functions)*
# note that order of goals/ limits determines importance(goal[0] is more important that goal[1])
# Terms:
#     aimless:has no goals
#     unsatisfiable:has one or more unsolvable goals
#     satisfied:has met all goals
#     unlimited:has no limiters
#     limited:has limiters
#     simulated:sysObject pers does not belong to a free user
#    Note:
#        pers only helps predict attrib's behavior but does not code for behavior. Use trd.tsk for this.
class prs:
    def __init__(self, goals=None, limits=None, functions=None):
        if goals is None:
            self.goals = []
        else:
            self.goals = goals
        if limits is None:
            self.limits = []
        else:
            self.limits = limits
        if functions is None:
            self.functions = []
        else:
            self.functions = functions

    # sets the values of limit, goal and funct
    # limit([] of limits)*, goal([] of goals)*, funct([] of functions available)
    def setPrs(self, limit, goal, funct):
        self.limits = limit
        self.goals = goal
        self.functions = funct

    # adds a new goal at goals[index]
    # goal(goal)*, index(int)*
    # none
    def newGoal(self, goal, index):
        self.goals.insert(index, goal)

    # adds a new limit at limits[index]
    # limit(limit)*, index(int)*
    # none
    def newLimit(self, limit, index):
        self.limits.insert(index, limit)

    # adds a new available function to functions
    # funct(available function)*
    # none
    def newFunction(self, funct):
        self.functions.append(funct)

    # removes a goal at index
    # index(int)*
    # none
    def removeGoal(self, index):
        self.goals.pop(index)

    # removes a limit at index
    # index(int)*
    # none
    def removeLimit(self, index):
        self.limits.pop(index)

    # removes a available function at index
    # index(int)*
    # none
    def removeFunction(self, index):
        self.functions.pop(index)

    # sets all prs attributes to None
    # none
    # none
    def clearPrs(self):
        self.limits = None
        self.goals = None
        self.functions = None


# info at run
if __name__ == "__main__":
    print("Description of the usr.prs attribute\nModule type:def")
