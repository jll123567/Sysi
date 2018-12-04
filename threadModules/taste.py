#
#
import object


#
#
class taste:
    def __init__(self, bit=0.0, swt=0.0, slt=0.0, sor=0.0, pln=0.0):
        self.bit = bit
        self.swt = swt
        self.slt = slt
        self.sor = sor
        self.pln = pln

    #
    #
    #
    def package(self):
        return object.data([self.bit, self.swt, self.slt, self.pln], {"name": "tread.olf.package",
                                                                      "id": None, "dataType": "thread.olf.package"})
