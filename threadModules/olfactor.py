# Defines thread olfactory input(hey, why not)
# module type: def
import object


# olfactory input for thread
# descriptor(str), strength(float between 0 and 1)
class olf:
    def __init__(self, descriptor="None", strength=0):
        self.descriptor = descriptor
        self.strength = strength

    # packs olf data into a data object(it needs an id)
    # none
    # olf data(object.dta([desc, str],tags))
    def package(self):
        return object.data([self.descriptor, self.strength], {"name": "tread.olf.package", "id": None,
                                                              "dataType": "thread.olf.package"})
