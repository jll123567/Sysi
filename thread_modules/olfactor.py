"""Define olf class."""
import object


class olf:
    """Hold olfactory input for thread.
    descriptor is a string
    strength is a float between and including 0 and 1"""
    def __init__(self, descriptor="None", strength=0):
        """Initialize attributes
        descriptor:"None"
        strength:0"""
        self.descriptor = descriptor
        self.strength = strength

    def package(self):
        """Pack olf data into a data sysObject(it needs an id) and return it."""
        return object.data([self.descriptor, self.strength], {"name": "tread.olf.package", "id": None,
                                                              "dataType": "thread.olf.package"})
