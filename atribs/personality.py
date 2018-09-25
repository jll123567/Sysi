# Description of the usr.prs atribute
# Module type:def


# user peronality(general behavior guide) Goals([] of boolean expressions that define goals)*, limits([] of boolean
# expressions that define limits(goals to avoid))*, functions([] of available functions)*
# note that order of goals/ limits determines importance(goal[0] is more important that goal[1])
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
    # limit([] of limits)*, goal([] of goals)*, funct([] of functions availiable)
    def setPrs(self, limit, goal, funct):
        self.limits = limit
        self.goals = goal
        self.functions = funct

    # adds a new goal at goals[index]
    # k
    def newGoal(self, goal, index):
        self.goals.insert(index, goal)

    def newLimit(self, limit, index):
        self.limits.insert(index, limit)

    def newFunction(self, funct):
        self.functions.append(funct)

    def removeGoal(self, index):
        self.goals.pop(index)

    def removeLimit(self, index):
        self.limits.pop(index)

    def removeFunction(self, index):
        self.functions.pop(index)

    def clearPrs(self):
        self.limits = None
        self.goals = None
        self.functions = None


# runtime
if __name__ == "__main__":
    print("pers def and functions v11.0")
