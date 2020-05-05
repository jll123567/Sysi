"""

"""


# TODO: DOC ME
class Tasker:
    """

    """

    def __init__(self, shifts=None):
        """

        """
        if shifts is None:
            self.shifts = []
        else:
            self.shifts = shifts

    def __iter__(self):
        """"""
        return self

    def __next__(self):
        """"""
        if not self.shifts:
            raise StopIteration
        return self.shifts.pop(0)

    def __str__(self):
        shiftsStr = []
        for shift in self.shifts:
            shiftsStr.append(str(shift))
        s = str.join(', ', shiftsStr)
        return "[" + str.join("", s.split("\"")) + "]"

    def insertShift(self, shift, idx=0):
        """"""
        self.shifts.insert(idx, shift)

    def popShift(self, idx=0):
        """"""
        return self.shifts.pop(idx)

    def getShift(self, idx=0):
        """"""
        return self.shifts[idx]

    def getShifts(self):
        """"""
        # TODO: Input validation.
        return self.shifts

    def setShifts(self, shifts):
        """"""
        self.shifts = shifts

    def appendShift(self, shift):
        """"""
        self.shifts.append(shift)


class Shift:
    """

    """

    def __init__(self, ops=None):
        """

        """
        if ops is None:
            self.operations = []
        else:
            self.operations = ops

    def __iter__(self):
        """"""
        return self

    def __next__(self):
        """"""
        if not self.operations:
            raise StopIteration
        return self.operations.pop(0)

    def __str__(self):
        s = []
        for o in self.operations:
            s.append(o.getFunction())
        return "[" + str.join(", ", s) + "]"

    def insertOperation(self, operation, idx=0):
        """"""
        self.operations.insert(idx, operation)

    def popOperation(self, idx=0):
        """"""
        return self.operations.pop(idx)

    def getOperation(self, idx=0):
        """"""
        return self.operations[idx]

    def getOperations(self):
        """"""
        return self.operations

    def setOperations(self, operations):
        """"""
        # TODO: Input validation.
        self.operations = operations

    def appendOperation(self, operation):
        """"""
        self.operations.append(operation)


class Operation:
    """

    """

    def __init__(self, funct, param, trg, src):  # Consider Enable/Disable for ops.
        """"""
        self.function = funct
        self.parameters = param
        self.target = trg
        self.source = src

    def __str__(self):
        return "{0.function}, {0.parameters}, {0.target}, {0.source}".format(self)

    def getFunction(self):
        """"""
        return self.function

    def getParameters(self):
        """"""
        return self.parameters

    def getTarget(self):
        """"""
        return self.target

    def getSource(self):
        """"""
        return self.source
