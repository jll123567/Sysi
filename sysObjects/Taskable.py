"""
Module for the Taskable class.

Classes
    Taskable
"""
from copy import copy

from sysObjects.Tagable import Tagable
import sysModules.Tasker as Tasker
import types


class Taskable(Tagable):
    """
    Abstract class for sysObjects that have a tasker.

    All sysObjects in sysi that plan to use a tasker should inherit from this class.
    Inherits from Tagable.

    Attributes
        tasker Tasker: The tasker for this object.
        tags dict: The tags for this object.

    Tags:
        id str: object's id.
        permissions [whitelist, blacklist]: List of permissions.

    Methods
        makeFunctions(str code_string): Take a string with only function definitions and return a list of functions.
        attachFunction(function funct, str attr): Set <funct> to self.<attr>.
        bindFunction(str fuAttr): Make the function in self.<fuAttr> a bound method.
        installFunctionSuite(str code_string): Make, attach, and possibly bind a set of functions from <code_string>.
    """

    def __init__(self, tsk=None, tags=None):
        """
        Constructor

        Defaults
            tasker = Tasker()
            tags = {"id": None}

        Parameters
            tsk Tasker: The tasker this object will use.
            tags dict: The tags this object will use.
        """
        super().__init__(tags)
        if tsk is None:
            self.tasker = Tasker.Tasker()
        else:
            self.tasker = tsk
        self.tags["permissions"] = [[], []]

    @staticmethod
    def makeFunctions(code_string):
        """
        Take a string with only function definitions and return a list of functions.

        If only one function is made it is returned alone rather than in a list.

        Parameters
            code_string str: A string with a set of functions.

        Return
            [function]/function: The functions generated from <code_string>.
        """
        code = compile(code_string, "<Taskable>", "exec")  # Compile code string to get a code object.

        fCs = []
        fNs = []
        for i in code.co_consts:  # Get and separate the function's code objects and the function's names.
            if isinstance(i, str):
                fNs.append(i)
            else:
                fCs.append(i)
        fCs.pop(-1)  # Get rid of return constant(None).

        fUs = []
        for i in range(fCs.__len__()):  # Make the functions from the code objects.
            fUs.append(
                types.FunctionType(fCs[i], globals(), fNs[i]))  # Globals is needed to access global vars/ builtins.

        if fUs.__len__() == 1:  # Return
            return fUs[0]
        else:
            return fUs

    def attachFunction(self, funct: types.FunctionType, attr: str):
        """Set <funct> to self.<attr>."""
        setattr(self, attr, funct)

    def bindFunction(self, fuAttr: str):
        """Make the function in self.<fuAttr> a bound method."""
        mtd = types.MethodType(getattr(self, fuAttr), self)  # Make a bound method from the function at <fuAttr>.
        setattr(self, fuAttr, mtd)  # Reattach

    def installFunctionSuite(self, code_string):
        """
        Make, attach, and possibly bind a set of functions from <code_string>.

        All functions will be attached but some will be made into bound methods if their first argument is named 'self'.
        Functions/methods are attached with their name. Existing attributes with the same name will be OVERRIDDEN!!!
        <code_string> must follow all the same rules for makeFunctions.

        Parameters
            code_string str: A string with a set of functions.
        """
        code = compile(code_string, "<Taskable>", "exec")  # Same as in makeFunctions
        fCs = []
        fNs = []
        for i in code.co_consts:
            if isinstance(i, str):
                fNs.append(i)
            else:
                fCs.append(i)
        fCs.pop(-1)

        mthds = []
        functs = []  # Separate the functions from the methods.
        for i in range(fCs.__len__())[::-1]:  # Parse in reverse because popping.
            if fCs[i].co_varnames.__len__() == 0:  # Handle zero args/vars.
                functs.append([fCs.pop(i), fNs.pop(i)])
            elif fCs[i].co_varnames[0] == "self":  # Its a method if the first varname(ie argument) is "self".
                mthds.append([fCs.pop(i), fNs.pop(i)])
            else:  # Some args/vars but no self.
                functs.append([fCs.pop(i), fNs.pop(i)])

        for i in functs:  # For functions: attach to self with name.
            f = i[0]
            n = i[1]
            self.attachFunction(types.FunctionType(f, globals(), n), n)  # Globals to keep global vars/builtins.
        for i in mthds:  # For methods: attach to self with name and bind.
            f = i[0]
            n = i[1]
            self.attachFunction(types.FunctionType(f, globals(), n), n)
            self.bindFunction(n)

    @staticmethod
    def printFromObject(*args, **kwargs):
        """
        Call print with args and kwargs.

        :param list args: Arguments to feed into print.
        :param dict kwargs: Keyword arguments to feed into print.
        """
        print(*args, **kwargs)

    def loopOp(self, op, iterations):
        """
        Schedule an operation to be called in the next shift <iterations> number of times.

        :param Operation op: The operation to be called in the next shift.
        :param int iterations: The number of times to repeat this procedure.
            Effectively how many iterations of the "loop".
        """
        if iterations > 0:
            newOp = copy(op)  # The original operation is copied to avoid always using the same object in case it
            # gets modified somehow.
            iterations -= 1
            ownOp = Tasker.Operation("loopOp", [newOp, iterations], self, self)
            if not self.tasker.shifts:  # Handle different states of tasker.shifts
                sh = Tasker.Shift([newOp, ownOp])
                self.tasker.shifts.append(sh)
            elif isinstance(self.tasker.shifts[0], Tasker.Shift):
                self.tasker.shifts[0].append(newOp)
                self.tasker.shifts[0].append(ownOp)
            else:
                sh = Tasker.Shift([newOp, ownOp])
                self.tasker.shifts[0] = sh
        else:
            return

    def loopOpInf(self, op):
        """
        Schedule an operation to be called in the next shift for every shift onwards.

        :param Operation op: The operation to be called next shift.
        """
        newOp = copy(op)  # The original operation is copied to avoid always using the same object in case it
        # gets modified somehow.
        ownOp = Tasker.Operation("loopOpInf", [newOp], self, self)
        if not self.tasker.shifts:  # Handle different states of tasker.shifts
            sh = Tasker.Shift([newOp, ownOp])
            self.tasker.shifts.append(sh)
        elif isinstance(self.tasker.shifts[0], Tasker.Shift):
            self.tasker.shifts[0].append(newOp)
            self.tasker.shifts[0].append(ownOp)
        else:
            sh = Tasker.Shift([newOp, ownOp])
            self.tasker.shifts[0] = sh
