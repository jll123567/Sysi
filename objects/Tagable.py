"""
The file for the tagable class.

Classes:
    tagable
"""


class Tagable:
    """
    Abstract class for objects that can be tagged.

    All objects in sysi should inherit from this class.

    Attributes
        tags(Dict): The tags for the object.
            Each tag is a key value pair and thus the dictionary.
            All objects should have an 'id' tag.({'id': '...'} at minimum.)

    Methods
        getTags(): Return all tags.
        getTag(any tag): Return the value of the tag specified by <tag>.
        setTags(dict tags): Set tags to <tags>.
        setTag(any tag, any value): Set the value of <tag> to <value>.
        addTag(dict tag): Add <tag> to tags.
        removeTag(any tag): Remove <tag> from tags.
        popTag(any tag): Remove and return <tag> from tags.
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

    def getTags(self):
        """Return all tags."""
        return self.tags

    def getTag(self, tag):
        """Return the value of the tag specified by <tag>."""
        return self.tags[tag]

    def setTags(self, tags):
        """Set tags to <tags>."""
        # TODO: input validation
        self.tags = tags

    def setTag(self, tag, value):
        """Set the value of <tag> to <value>."""
        self.tags[tag] = value

    def addTag(self, tag):
        """Add <tag> to tags."""
        self.tags.update(tag)

    def removeTag(self, tag):
        """Remove <tag> from tags."""
        del self.tags[tag]

    def popTag(self, tag):
        """Remove and return <tag> from tags."""
        return self.tags.pop(tag)
