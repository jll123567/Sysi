"""
File for Tasker and related classes.

Classes
    Tasker
    Shift
    Operation
"""


class Operation:
    """
    Represents one action that is requested to the session.

    Attributes
        function str: Identifier for the function to call.
        parameters list: List of parameters to pass to function.
        target str/Taskable: The Taskable object(or its id) to call the function of.
        source str/Taskable: The Taskable object(or its id) that requested this.
    """

    def __init__(self, funct, param, trg, src):  # Consider Enable/Disable for ops.
        """
        Constructor

        Parameters
            funct str: Identifier for the function to call.
            param list: List of parameters to pass to function.
            target str or Taskable: The Taskable object(or its id) to call the function of.
            source str or Taskable: The Taskable object(or its id) that requested this.
        """
        self.function = funct
        self.parameters = param
        self.target = trg
        self.source = src

    def __str__(self):
        """
        Convert to a string.

        Format is "<function>, <parameters>, <target>, <source>".

        Returns
            str: This operation as a string.
        """
        return "{0.function}, {0.parameters}, {0.target}, {0.source}".format(self)


class Shift:
    """
    A set of operations in no particular order that should occur at the same time.

    Similar to Tasker a shift is a list of operations.
    It's also an iterator where next pops the next operation.

    Attributes
        operations(list): A list of operations.
    """

    def __init__(self, ops=None):
        """
        Constructor

        Operations is set to [] if None is provided.

        Parameters
            ops list: a list of operations.
        """
        if ops is None:
            self.operations = []
        else:
            self.operations = ops

    def __iter__(self):
        """Return self as an iterator"""
        return self

    def __next__(self):
        """Pop and return the next shift."""
        if not self.operations:
            raise StopIteration
        return self.operations.pop(0)

    def __str__(self):
        """
        Convert to a string.

        Format is [<operation0>, <operation1>, ..., <operation-n>]

        Returns
            str: This shift as a string.
        """
        s = []
        for o in self.operations:
            s.append(o.getFunction())
        return "[" + str.join(", ", s) + "]"


class Tasker:
    """
    Module that allows Taskable sysObjects to preform actions in sessions.

    A tasker is a list of shifts where the first shift is the next set of operations to preform.
    It's also an iterator where next pops the next shift.

    Attributes
        shifts(list): A list of shifts.
    """

    def __init__(self, shifts=None):
        """
        Constructor

        Shifts is set to [] if None is provided.

        Parameters
            shifts list: a list of shifts.
        """
        if shifts is None:
            self.shifts = []
        else:
            self.shifts = shifts

    def __iter__(self):
        """Return self as an iterator"""
        return self

    def __next__(self):
        """Pop and return the next shift."""
        if not self.shifts:
            raise StopIteration
        return self.shifts.pop(0)

    def __str__(self):
        """
        Convert to a string.

        Format is [<shift0>, <shift1>, ..., <shiftn>]

        Returns
            str: This Tasker as a string.
        """
        shiftsStr = []
        for shift in self.shifts:
            shiftsStr.append(str(shift))
        s = str.join(', ', shiftsStr)
        return "[" + str.join("", s.split("\"")) + "]"
