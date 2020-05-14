"""
Module for tagged data storage.

Classes
    Data
"""
from sysObjects.Tagable import Tagable


class Data(Tagable):
    """
    Class for storing some arbitrary data with tags.

    Inherit from this if you plan to make a more robust object to store your particular type of data.

    Attributes
        storage any: The data you plan to store.
        tags dict: Tags.

    Methods
        setDataType(str dataType): Set the dataType of this Data to <dataType>.
    """

    def __init__(self, id, s=None, tags=None):
        super().__init__(tags)
        self.tags['id'] = id
        self.tags["dataType"] = "None"
        self.storage = s

    def __str__(self):
        return "{}:{}[\n{},\n{}\n]".format(self.tags["id"], self.tags["dataType"], self.storage, self.tags)

    def setDataType(self, dataType: str):
        """Set the dataType of this Data to <dataType>."""
        self.tags["dataType"] = dataType
