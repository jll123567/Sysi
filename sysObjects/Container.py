"""
Container object.

Describes a set of boundries that other objects could reside within. Containers are the parents of other containers and
are offset by their parent.

Classes
    :class:`Container`
"""
from sysObjects.Tagable import Tagable
from sysModules.Model import Vector3


class Container(Tagable):
    """
    Specifies an area that objects can be contained within.

    Allows for nesting structure.
    Encouraged for scenes and universes.
    The parent holds the parent container and can be `None`. The origin offset is a :class:`Vector3` with the offset from
    the parent and should be zero when the parent is `None`. Bounds are a list containing two :class:`Vector3` s or None.
    When the list is [None, None] the container is "Unbounded" and every object is inside of it. Useful for the base
    container of a :class:`Universe`.


    :param str id: The id of this container.
    :param p: The parent container this container is within and offset by.
    :type p: Container or None
    :param org: The distance from the origin of the parent container. Make sure it's 0 if parent is None.
    :type org: Vector3, optional
    :param bnd: The area enclosed by the container defined by a list two :class:`Vector3`s from this container's origin.
        If bounds are [None, None] the container is "Unbounded" but only self.bounds[0] is checked in this file.
        Defaults to unbounded.
        The container's origin is the total offset from base container.
    :type bnd: list, optional
    :param tags: Tags. The `id` tag will be set to `id`.
    :type tags: dict, optional
    """

    def __init__(self, id, p=None, org=None, bnd=None, tags=None):
        """
        Constructor
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

        :return: Returns either a float, a string with the area, or "Unbounded" if bounds are [None, None].
        :rtype: float or str
        """
        if self.bounds[0] is None:
            return "Unbounded"
        return self.bounds[0].areaBetween(self.bounds[1])

    def getTotalOriginOffset(self):
        """Gets the total offset from this container to the base and returns it as a Vector3."""
        if self.parent is None:
            return self.originOffset
        return self.originOffset + self.parent.getTotalOriginOffset()
