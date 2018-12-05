# taste input for thread
# module type: def
import object


# handles state input as average of five basic flavors(if anyone has a better model of taste hit me up)
# bitter(float(0,1)), sweet((float(0,1)), salty(float(0,1)), sour(float(0,1)), plain(float(0,1))
class taste:
    def __init__(self, bit=0.0, swt=0.0, slt=0.0, sor=0.0, pln=0.0):
        self.bit = bit
        self.swt = swt
        self.slt = slt
        self.sor = sor
        self.pln = pln

    # packs taste into a data object for ram to use
    # none
    # dta([basically a taste], tags)
    def package(self):
        return object.data([self.bit, self.swt, self.slt, self.pln], {"name": "tread.olf.package",
                                                                      "id": None, "dataType": "thread.olf.package"})
