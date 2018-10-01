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
#     simulated:object pers does not belong to a free user
#    Note:
#        pers only helps predict atribs behavior but does not code for behavior. Use trd.tsk for this.
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
    # No output
    def newGoal(self, goal, index):
        self.goals.insert(index, goal)

    # adds a new limit at limits[index]
    # limit(limit)*, index(int)*
    # No output
    def newLimit(self, limit, index):
        self.limits.insert(index, limit)

    # adds a new available function to functions
    # funct(available function)*
    # No output
    def newFunction(self, funct):
        self.functions.append(funct)

    # removes a goal at index
    # index(int)*
    # No output
    def removeGoal(self, index):
        self.goals.pop(index)

    # removes a limit at index
    # index(int)*
    # No output
    def removeLimit(self, index):
        self.limits.pop(index)

    # removes a available function at index
    # index(int)*
    # No output
    def removeFunction(self, index):
        self.functions.pop(index)

    # sets all prs attributes to None
    # No input
    # No output
    def clearPrs(self):
        self.limits = None
        self.goals = None
        self.functions = None


# info at run
if __name__ == "__main__":
    print("Description of the usr.prs attribute\nModule type:def")
