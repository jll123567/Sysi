"""Definition for user memory."""
import re
import hashlib
import sys_objects


class mem:
    """Hold arbitrary copies of objects.
        Functions requesting a block want an int between 0 and 2.
            0 is for internal, 1 is for real, 2 is for external
    """

    def __init__(self, internal=None, real=None, external=None):
        """Internal: list
            Real: list
            External: list
        """
        if internal is None:
            self.internal = []
        else:
            self.internal = internal
        if real is None:
            self.real = []
        else:
            self.real = real
        if external is None:
            self.external = []
        else:
            self.external = external

    def removeMemory(self, block, index):
        """Remove the memory at block[index]."""
        if block == 0:
            self.internal.pop(index)
        elif block == 1:
            self.real.pop(index)
        else:
            self.external.pop(index)

    def addMemory(self, block, obj):
        """Add obj to mem at block."""
        if block == 0:
            self.internal.append(obj)
        elif block == 1:
            self.real.append(obj)
        else:
            self.external.append(obj)

    # finds something that matched the query and prints it, if nothing is found, None is printed
    # query(str)
    # console output(str)
    def find(self, query=""):
        """Print objects in mem that match query.
            If nothing is found None is printed.
        """
        for d in self.__dict__:
            for i in d:
                if re.match(str(i), r"*(.)" + query + r"*(.)"):
                    print(i)
                else:
                    print(None)

    def modify(self, block, index, value):
        """Set the value at index in block in mem."""
        if block == 0:
            self.internal[index] = value
        elif block == 1:
            self.real[index] = value
        else:
            self.external[index] = value


def hashObj(obj):
    """Return the MD5 hash of obj"""
    info = obj
    dta = sys_objects.data((hashlib.md5(info.encode('utf-8')).hexdigest()), obj.tag)
    return dta
# The reason I do this here is [None]
