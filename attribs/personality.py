"""Definition of the usr.prs attribute"""


class prs:
    """Define loosely the behavior of users
        pers only helps loosely define user behavior but does not code for behavior. Use trd.tsk for this.
        goals and limits are boolean expressions ranked most important to least important(goal[0] is most)
        goals are encouraged, limits are not
    """

    def __init__(self, goals=None, limits=None, functions=None):
        """Goals: list
            Limits: list
            Functions: list
        """
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

    def setPrs(self, limit, goal, funct):
        """Set self.limit, goal and functions to <limit>, <goal>, <funct>."""
        self.limits = limit
        self.goals = goal
        self.functions = funct

    def newGoal(self, goal, index):
        """Insert <goal> to self.goals[<index>]."""
        self.goals.insert(index, goal)

    def newLimit(self, limit, index):
        """Insert <limit> to self.limits[<index>]."""
        self.limits.insert(index, limit)

    def newFunction(self, funct):
        """Insert <funct> to self.functions[<index>]."""
        self.functions.append(funct)

    def removeGoal(self, index):
        """Remove goal at <index>."""
        self.goals.pop(index)

    def removeLimit(self, index):
        """Remove limit at <index>."""
        self.limits.pop(index)

    def removeFunction(self, index):
        """Remove function at <index>."""
        self.functions.pop(index)

    def clearPrs(self):
        """Set all prs attributes to None."""
        self.limits = None
        self.goals = None
        self.functions = None
