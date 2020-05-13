"""
The module for Scenes

Classes
    Scene
"""
from sysObjects.Tagable import Tagable


# defaultContainer = Container()


class Scene(Tagable):
    """
    Represents the run of a Session.

    Attributes
        container Container: The container where the session took place.
        timeline tuple: The timeline id and what shift the scene starts at (in that order).
        script [Shifts]: The shifts in order of occurrence.
        objectList [object]: The objects in the scene at their inital state.
        tags dict: Tags.
    """

    def __init__(self, id, cont, tl=None, scp=None, obj=None, tags=None):
        """
        Constructor

        Requires a container though None could(but shouldn't be provided).
        Timeline can be None to indicate the events in this scene as invalid.
        script and objectList default to an empty list.

        Parameters
            id str: id
            cont Container: container
            tl list/None: timeline
            scp [Shift]: script
            obj [object]: objectList
            tags dict: tags
        """
        super().__init__(tags)
        self.tags["id"] = id
        self.container = cont
        self.timeline = tl
        if scp is None:
            self.script = []
        else:
            self.script = scp
        if obj is None:
            self.objectList = []
        else:
            self.objectList = obj

    def __str__(self):
        if self.container is None:
            contId = None
        else:
            contId = self.container.tags["id"]
        return "{}:taking place in {}at{}\nobjects:{}, shifts:{}\n{}".format(self.tags["id"], contId, self.timeline,
                                                                             self.objectList.__len__(),
                                                                             self.script.__len__(),
                                                                             self.tags)
