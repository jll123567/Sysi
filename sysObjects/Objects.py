"""
Classes for actual things.

Classes
    StaticObject
"""
from sysObjects.Taskable import Taskable
from sysModules.Memory import Memory
from sysModules.Model import Model
from sysModules.Tasker import Tasker


class StaticObject(Taskable):
    """
    An object that has no long term storage.

    Attributes
        model Model: Object's model.
        memory Memory: Object's memory
        tasker Tasker: Object's tasker
        tags dict: Object's tags
    """

    def __init__(self, mod=Model(), mem=Memory(), tsk=Tasker(), tags=None):
        super().__init__(tsk, tags)
        self.model = mod
        self.memory = mem

    def __str__(self):
        return "{}:[\n{},\n{},\n{},\n{}\n]".format(self.tags['id'], self.model, self.memory, self.tasker, self.tags)

    # TODO: Implement Dynamic function stuff.
