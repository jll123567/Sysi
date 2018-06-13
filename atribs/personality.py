# noinspection PyDefaultArgument
class prs:
    # noinspection SpellCheckingInspection
    def __init__(self, goals=[], limits=[], functions=[]):
        self.goals = goals
        self.limits = limits
        self.functions = functions

        # setup
        # [limits,goals,functions,dict]
        # "functname()"
        # goals are bool checks that a atribs attempts to mke true and are in urgency order
        # limits are similar but are meant to not be made true and are still in urgency order
        # tasker profile(auto-get)
        # {"word": referenceCount(int), "...": ...}

    def setPrs(self, limit, goal, funct):
        self.limits = limit
        self.goals = goal
        self.functions = funct

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
    print("pers def and functions v10.0")
