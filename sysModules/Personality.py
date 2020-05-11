"""
Classes for user pers.

Classes
    Personality
    Conditional
"""


class Personality:
    """
    Represents a user's decision making.

    The idea is to get all Conditional objects in goals to be true and false in limits.
    This allows a user to make decisions by mapping functions to changed output.

    Attributes
        goals [Conditional]: Conditionals to make true.
        limits [Conditional]: Conditionals to keep false.
        functions [str]: Functions usable by users.
    """

    def __init__(self, gl=None, lim=None, funct=None):
        """
        Constructor

        Goals, limits, and functions default to an empty list.

        Parameters
            gl=None [Conditional]: Conditionals to make true.
            lim=None [Conditional]: Conditionals to keep false.
            funct=None [str]: Functions usable by users.
        """
        if gl is None:
            self.goals = []
        else:
            self.goals = gl
        if lim is None:
            self.limits = []
        else:
            self.limits = lim
        if funct is None:
            self.functions = []
        else:
            self.functions = funct

    def __str__(self):
        return "g:{}, l:{} f:{}".format(self.goals, self.limits, self.functions)


class Conditional:
    """
    Put two objects in to have a constantly updating way to compare them.

    Attributes
        a any: Thing one.
        aAttribute str: The part of a to check.
        b any: Thing two.
        bAttribute str: The part of b to check.
        evalType str: How Conditional compares a and b.
    """

    def __init__(self, a, aatr, b, batr, evalType):
        self.a = a
        self.aAttribute = aatr
        self.b = b
        self.bAttribute = batr
        self.evalType = evalType

    def __bool__(self):
        """
        Returns true or false depending on a, b, and evalType. Defaults to false if bad evalType.
        """
        e = self.evalType
        if self.aAttribute is None:
            a = self.a
        else:
            a = self.a.__getattribute__(self.aAttribute)
        if self.bAttribute is None:
            b = self.b
        else:
            b = self.b.__getattribute__(self.bAttribute)

        if e == '=':
            return a == b
        elif e == '!':
            return a != b
        elif e == ">":
            return a > b
        elif e == "<":
            return a < b
        elif e == ">=":
            return a >= b
        elif e == "<=":
            return a <= b
        elif e == "is":
            return a is b
        else:
            return False

    def distance(self):
        """
        Calculate how far apart a and b are.

        For numerical values its the absolute value of the difference.
        For booleans this returns 0 for matching values.
        For lists, strings, and a being a tuple return how many matches there are between a and b.
        """
        if self.aAttribute is None:
            a = self.a
        else:
            a = self.a.__getattribute__(self.aAttribute)
        if self.bAttribute is None:
            b = self.b
        else:
            b = self.b.__getattribute__(self.bAttribute)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return abs(a - b)
        elif isinstance(a, bool) and isinstance(b, bool):
            if a == b:
                return 0
            else:
                return 1
        elif isinstance(a, (list, str, tuple)) and isinstance(b, (list, str)):
            matches = 0
            b = list(b)
            for i in a:
                for f in b:
                    if i == f:
                        matches += 1
                        b.remove(f)
                        break
            return abs(a.__len__() - matches)
        else:
            return None
