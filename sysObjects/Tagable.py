"""
The file for the tagable class.

Classes:
    tagable
"""


class Tagable:
    """
    Abstract class for sysObjects that can be tagged.

    All sysObjects in sysi should inherit from this class.

    Attributes
        tags(Dict): The tags for the object.
            Each tag is a key value pair and thus the dictionary.
            All sysObjects should have an 'id' tag.({'id': '...'} at minimum.)
    """

    def __init__(self, tags=None):
        """
        Constructor

        If no 'id' tag is provided in <tags> a blank one is added.

        Parameters
            tags(dict): Initial dictionary.

        Returns
            None
        """
        if tags is None:
            self.tags = {}
        else:
            self.tags = tags
        if "id" not in self.tags.keys():
            self.tags["id"] = None
