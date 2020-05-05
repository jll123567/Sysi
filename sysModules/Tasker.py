"""
File for Tasker and related classes.

Classes
    Tasker
    Shift
    Operation
"""


class Tasker:
    """
    Module that allows Taskable objects to preform actions in sessions.

    A tasker is a list of shifts where the first shift is the next set of operations to preform.
    It's also an iterator where next pops the next shift.

    Attributes
        shifts(list): A list of shifts.

    Methods
        insertShift(Shift shift, int idx=0): Insert <shift> at <idx>.
        popShift(int idx=0): Remove and return the shift at <idx>.
        getShift(int idx=0): Return the shift at <idx>.
        getShifts(): Return a list of all shifts.
        setShifts(list shifts): Set this tasker's shifts to <shifts>.
        appendShift(Shift shift): Append <shift> to this tasker's shifts.
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

    def insertShift(self, shift, idx=0):
        """Insert <shift> at <idx>."""
        self.shifts.insert(idx, shift)

    def popShift(self, idx=0):
        """Remove and return the shift at <idx>."""
        return self.shifts.pop(idx)

    def getShift(self, idx=0):
        """Return the shift at <idx>."""
        return self.shifts[idx]

    def getShifts(self):
        """Return a list of all shifts."""
        return self.shifts

    def setShifts(self, shifts):
        """Set this tasker's shifts to <shifts>."""
        self.shifts = shifts

    def appendShift(self, shift):
        """Append <shift> to this tasker's shifts."""
        self.shifts.append(shift)


class Shift:
    """
    A set of operations in no particular order that should occur at the same time.

    Similar to Tasker a shift is a list of operations.
    It's also an iterator where next pops the next operation.

    Attributes
        operations(list): A list of operations.

    Methods
        insertOperation(operation operation, int idx=0): Insert <operation> at <idx>.
        popOperation(int idx=0): Remove and return the operation at <idx>.
        getOperation(int idx=0): Return the operation at <idx>.
        getOperations(): Return a list of all operations.
        setOperations(list operations): Set this tasker's operations to <operations>.
        appendOperation(operation operation): Append <operation> to this tasker's operations.
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

    def insertOperation(self, operation, idx=0):
        """Insert <operation> at <idx>."""
        self.operations.insert(idx, operation)

    def popOperation(self, idx=0):
        """Remove and return the operation at <idx>."""
        return self.operations.pop(idx)

    def getOperation(self, idx=0):
        """Return the operation at <idx>."""
        return self.operations[idx]

    def getOperations(self):
        """Return a list of all operations."""
        return self.operations

    def setOperations(self, operations):
        """Set this tasker's operations to <operations>."""
        self.operations = operations

    def appendOperation(self, operation):
        """Append <operation> to this tasker's operations."""
        self.operations.append(operation)


class Operation:
    """
    Represents one action that is requested to the session.

    Attributes
        function(str): Identifier for the function to call.
        parameters(list): List of parameters to pass to function.
        target(str, Taskable): The Taskable object(or its id) to call the function of.
        source(str, Taskable): The Taskable object(or its id) that requested this.

    Methods
        getFunction(): Get this operation's function.
        getParameters(): Get this operation's parameters.
        getTarget(): Get this operation's target.
        getSource(): Get this operation's source.
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

    def getFunction(self):
        """Get this operation's function."""
        return self.function

    def getParameters(self):
        """Get this operation's parameters."""
        return self.parameters

    def getTarget(self):
        """Get this operation's target."""
        return self.target

    def getSource(self):
        """Get this operation's source."""
        return self.source
