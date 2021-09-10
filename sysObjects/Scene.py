"""
The module for Scenes

**Variables** :
    `defaultContainer` (:py:class:`sysObjects.Container.Container`): A default container with no id, parent, or bounds.


"""
from sysObjects.Tagable import Tagable
from sysObjects.Container import Container

defaultContainer = Container(None)


class Scene(Tagable):
    """
    Represents the run of a Session.

    :param str id: The scene's id.
    :param Container cont: A :py:class:`sysObjects.Container.Container` that contains all objects in the scene.
        Requires a container though None could(but shouldn't be provided).
    :param tl: The timeline id and what shift the scene starts at (in that order).
        Timeline can be None to indicate the events in this scene as invalid.
    :type tl: tuple or None
    :param scp: List of :py:class:`sysModules.Tasker.Shift`'s in chronological order.
        :py:class:`sysModules.Tasker.Tasker`. When `None` :py:attr:`script` is set to an empty ``list``.
    :type scp: list or None
    :param obj: List of :py:class:`sysObjects.Tagable.Tagable` objects at their inital state.
        When ``None`` :py:attr:`objectList` is set to an empty ``list``.
    :type obj: list or None
    :param tags: Tags. When ``None`` then ``tags`` is set to ``{"id": id}``. "id" will be set to ``id``.
    :type tags: dict or None
    """

    def __init__(self, id, cont, tl=None, scp=None, obj=None, tags=None):
        """Constructor"""
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
