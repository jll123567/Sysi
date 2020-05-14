"""
Module for Container

Classes
    Container
"""
from sysObjects.Tagable import Tagable
from sysModules.Model import Vector3


class Container(Tagable):
    """
    Specifies an area.

    Allows for nesting structure.
    Required for scenes and universes.

    Attributes
        parent Container/None: The parent container this container is within. None if its the base container.
        originOffset Vector3: The distance from the origin of the parent container. Set to 0 if parent is None.
        bounds list: The area enclosed by the container defined by two Vector3s from this container's origin.
            This container's origin is the total offset from base container.
            If bounds are [None, None] the container is "Unbounded"
                Only self.bounds[0] is checked here tho.
        tags dict: tags

    Methods
        getArea(): Get the area of the bounds.
        getTotalOriginOffset(): Get the total offset from this container to the base and return it as a Vector3.
    """

    def __init__(self, id, p=None, org=None, bnd=None, tags=None):
        """
        Constructor

        Parent defaults to None.
        OriginOffset defaults to 0 and is set to 0 if parent is None.
        Bounds defaults to None(Unbounded).

        Parameters
            id str: id
            p Container: parent
            org Vector3: originOffset
            bnd list: bounds
            tags dict: tags
        """
        super().__init__(tags)
        self.tags['id'] = id
        self.parent = p
        if org is None or self.parent is None:
            self.originOffset = Vector3()
        else:
            self.originOffset = org
        if bnd is None:
            self.bounds = [None, None]
        else:
            self.bounds = bnd

    def __str__(self):
        if self.parent is None:
            pId = None
        else:
            pId = self.parent.tags["id"]
        return "{}:\nparent:{}, origin:{}, bound area:{}\n{}".format(self.tags["id"], pId, self.originOffset,
                                                                     self.getArea(), self.tags)

    def getArea(self):
        """
        Get the area of the bounds.

        Returns "Unbounded" if bounds are [None, None].
        Returns
            float/str: area/unbounded message.
        """
        if self.bounds[0] is None:
            return "Unbounded"
        return self.bounds[0].areaBetween(self.bounds[1])

    def getTotalOriginOffset(self):
        """Get the total offset from this container to the base and return it as a Vector3."""
        if self.parent is None:
            return self.originOffset
        return self.originOffset + self.parent.getTotalOriginOffset()
