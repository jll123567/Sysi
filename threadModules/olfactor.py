"""Define olf class."""
import object


class olf:
    """Hold olfactory input for thread."""
    def __init__(self, descriptor="None", strength=0):
        """descriptor holds string
        strength holds float between 0 and 1"""
        self.descriptor = descriptor
        self.strength = strength

    def package(self):
        """Pack olf data into a data object(it needs an id) and return it."""
        return object.data([self.descriptor, self.strength], {"name": "tread.olf.package", "id": None,
                                                              "dataType": "thread.olf.package"})
