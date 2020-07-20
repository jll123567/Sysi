"""
Module for objects the control other objects.

Classes:
    SubObject
"""
from sysModules.Model import Vector3


class SubObject:
    """
    A module for having objects take direct control and ownership of other objects.
    Put this module at <your_object>.subObject.

    :param Taskable owner: The object that owns this instance of the SubObject sysModule.
    :param Taskable/None parent: The object acting as the parent of owner.
    :param list children: The objects that the owner is a parent to.
    :param Vector3 offset: The distance the owner is away from the parent.
    """

    def __init__(self, owner, parent=None, children=None, offset=None):
        """Constructor"""
        self.owner = owner
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = children
        if offset is None:
            self.offset = Vector3()
        else:
            self.offset = offset

    def __str__(self):
        return "Owner {}:Parent {}:Offset {}:Children {}".format(self.owner, self.parent, self.offset,
                                                                 self.children.__len__())

    def getChildById(self, chId):
        """
        Return the child object in self.children that has an id that matches <chId>.
        If no valid match is found None is returned.

        :param str chId: The id of the child to find.
        :return: The child with the matching id.
        :rtype: Taskable/None
        """
        for ch in self.children:  # Iterate though all children.
            if ch.tags["id"] == chId:
                return ch

    def setChildParrents(self):
        """
        Set the parent of all objects in self.children to self.owner.

        This assumes all children have a subObject module at the standard location.
        """
        for ch in self.children:
            if ch.subObject.parent != self.owner:
                ch.subObject.parent = self.owner

    def getNewPosition(self):
        """
        Return a Vector3 representing the parent's position plus self.offset.

        :return: The new position.
        :rtype: Vector3
        """
        parPos = self.parent.model.position
        newPos = parPos + self.offset
        return newPos

    def setNewPosition(self):
        """Set the owner's position to that from self.getNewPosition()."""
        self.owner.model.position = self.getNewPosition()

    def updateChildPositions(self):
        """
        Call setNewPosition on all children.

        Assumes all children have a SubObject module at the standard location.
        """
        for ch in self.children:
            ch.subObject.setNewPosition()

    def makeModelAssembly(self):
        """Call makeAssembly() at the owner's model."""
        self.owner.model.makeAssembly()

    def restoreModelFromAssembly(self):
        """Call restoreFromAssembly() at the owner's model."""
        self.owner.model.restoreFromAssembly()
