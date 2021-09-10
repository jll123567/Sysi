"""
Module for tagged data storage.


"""
from sysObjects.Tagable import Tagable


class Data(Tagable):
    """
    Class for storing some arbitrary data with tags.

    Inherit from this if you plan to make a more robust object to store your particular type of data.

    :param str id: The id of this object.
    :param any storage: The data you plan to store.
    :param dict tags: Tags. Defaults to
        ``{"id": id, "dataType": None, "relevancy": [0], "interest": [0], "content": []}``

    """

    def __init__(self, id, storage=None, tags=None):
        """Constructor"""
        super().__init__(tags)
        self.tags['id'] = id
        self.tags["dataType"] = "None"
        self.tags["relevancy"] = [0]  # Make a formal format for this later.
        self.tags["interest"] = [0]
        self.tags["content"] = []  # A list of strings that describe the content of the data. Not just the type.
        self.storage = storage

    def __str__(self):
        return "{}:{}".format(self.tags["dataType"], self.storage)

    def setDataType(self, dataType: str):
        """Set the dataType of this Data to ``dataType``."""
        self.tags["dataType"] = dataType
