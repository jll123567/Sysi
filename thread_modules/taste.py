"""taste input for thread"""
import sys_objects


class taste:
    """hold taste

    bit:float between and including 0 and 1
    the rest: the same as bit"""
    def __init__(self, bit=0.0, swt=0.0, slt=0.0, sor=0.0, pln=0.0):
        """initializes class attributes(to 0 by default)"""
        self.bit = bit
        self.swt = swt
        self.slt = slt
        self.sor = sor
        self.pln = pln

    def package(self):
        """pack taste into a data and return it"""
        return sys_objects.data([self.bit, self.swt, self.slt, self.pln], {"name": "tread.olf.package",
                                                                      "id": None, "dataType": "thread.olf.package"})
