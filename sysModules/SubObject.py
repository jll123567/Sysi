"""
Module for objects the control other objects.

Classes:
    SubObject
"""
from sysModules.Model import Vector3


class SubObject:  # TODO: TEST ME!
    def __init__(self, owner, parent=None, children=None, offset=None):
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
        for ch in self.children:
            if ch.tags["id"] == chId:
                return ch

    def setChildParrents(self):
        for ch in self.children:
            if ch.subOjbect.parent != self.owner:
                ch.subOjbect.parent = self.owner

    def getNewPosition(self):
        parPos = self.parent.model.position
        newPos = parPos + self.offset
        return newPos

    def setNewPosition(self):
        self.owner.model.position = self.getNewPosition()

    def updateChildPositions(self):
        for ch in self.children:
            ch.subOjbect.setNewPosition()
