"""
Module for object's 3d representation.

Classes
    Vector3
    Model
"""


class Vector3:
    """
    Represents a position in 3d space.

    Yep I could probably have imported this or used a list.

    Attributes
        x float: Pos on x axis.
        y float: Pos on y axis.
        z float: Pos on z axis.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Constructor"""
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "[{}, {}, {}]".format(self.x, self.y, self.z)


class Model:
    """
    Represents object's appearance in 3d space.

    Attributes
        model any: Geometry and animations.
        material any: Ill implement something more substantial later.
        position Vector3: Position info
    """

    def __init__(self, mod=None, mat=None, pos=Vector3()):
        self.model = mod  # Implement better model.
        self.material = mat  # Implement better material.
        self.position = pos  # https://twitter.com/PossumEveryHour

    def __str__(self):
        return "{}".format(self.position, self.model, self.material)
