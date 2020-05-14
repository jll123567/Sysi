"""
Module for the Taskable class.

Classes
    Taskable
"""
from sysObjects.Tagable import Tagable
from sysModules.Tasker import Tasker
import types


class Taskable(Tagable):
    """
    Abstract class for sysObjects that have a tasker.

    All sysObjects in sysi that plan to use a tasker should inherit from this class.
    Inherits from Tagable.

    Attributes
        tasker Tasker: The tasker for this object.
        tags dict: The tags for this object.

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
            self.tasker = Tasker()
        else:
            self.tasker = tsk

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
