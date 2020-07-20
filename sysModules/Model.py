"""
Module for object's 3d representation.

Classes
    Vector3
    Model
"""
from copy import copy


class Vector3:
    """
    Represents a position in 3d space.

    Yep I could probably have imported this or used a list.

    Attributes
        x float: Pos on x axis.
        y float: Pos on y axis.
        z float: Pos on z axis.

    Methods
        S: add(Vector3 a, Vector3 b)
        S: sub(Vector3 a, Vector3 b)
        S: distance(Vector3 a, Vector3 b)
        distance(Vector3 other)
        S: areaBetween(Vector3 a, Vector3 b)
        areaBetween(Vector3 other)
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Constructor"""
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "[{}, {}, {}]".format(self.x, self.y, self.z)

    @staticmethod
    def add(a, b):
        """Add <a> and <b>."""
        x = float(a.x + b.x)
        y = float(a.y + b.y)
        z = float(a.z + b.z)
        return Vector3(x, y, z)

    def __add__(self, other):
        if not isinstance(other, Vector3):
            return NotImplemented
        return Vector3.add(self, other)

    @staticmethod
    def sub(a, b):
        """subtract <b> from <a>."""
        x = float(a.x - b.x)
        y = float(a.y - b.y)
        z = float(a.z - b.z)
        return Vector3(x, y, z)

    def __sub__(self, other):
        if not isinstance(other, Vector3):
            return NotImplemented
        return Vector3.sub(self, other)

    @staticmethod
    def distance(a, b):
        """Calculate the distance between <a> and <b>."""
        c = a - b
        return Vector3(abs(c.x), abs(c.y), abs(c.z))

    def distance(self, other):
        """Calculate the distance between self and <other>."""
        c = self - other
        return Vector3(abs(c.x), abs(c.y), abs(c.z))

    @staticmethod
    def areaBetween(a, b):
        """Calculate the area between <a> and <b>."""
        c = Vector3.distance(a, b)
        return c.x * c.y * c.z

    def areaBetween(self, other):
        """Calculate the area between self and <other>."""
        c = Vector3.distance(self, other)
        return c.x * c.y * c.z


class Model:
    """
    Represents object's appearance in 3d space.

    Attributes
        model any: Geometry and animations.
        material any: Ill implement something more substantial later.
        position Vector3: Position info
    """

    def __init__(self, mod=None, mat=None, pos=None):
        self.model = mod  # Implement better model.
        self.material = mat  # Implement better material.
        if pos is None:
            self.position = Vector3()
        else:
            self.position = pos  # https://twitter.com/PossumEveryHour
        self._modRestore = None

    def __str__(self):
        return "{}".format(self.position, self.model, self.material)

    def makeAssembly(self):
        """Store the model and material in a protected attribute and set them to None."""
        self._modRestore = (copy(self.model), copy(self.material))  # Save removed components.
        self.model = None
        self.material = None

    def restoreFromAssembly(self):
        """Restore the model and material from the _modRestore attribute."""
        self.model = self._modRestore[0]
        self.material = self._modRestore[1]
