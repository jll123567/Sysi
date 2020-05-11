"""
Classes for actual things.

Classes
    StaticObject
    DynamicObject
    User
"""
from sysObjects.Taskable import Taskable
import sysModules.Memory as Memory
from sysModules.Model import Model
from sysModules.Tasker import Tasker
from sysModules.Sensory import Sensory
from sysModules.Personality import Personality


class StaticObject(Taskable):
    """
    An object that has no long term memory.

    Think something that provides only basic utility, like a mug.

    Attributes
        model Model: Object's model.
        memory Memory: Object's memory.
        tasker Tasker: Object's tasker.
        tags dict: Object's tags.
    """

    def __init__(self, id, mod=Model(), mem=Memory.Memory(), tsk=Tasker(), tags=None):
        super().__init__(tsk, tags)
        self.tags["id"] = id
        self.model = mod
        self.memory = mem

    def __str__(self):
        return "{}:[\n{},\n{},\n{},\n{}\n]".format(self.tags['id'], self.model, self.memory, self.tasker, self.tags)


class DynamicObject(StaticObject):
    """
    An object with long term memory and sensory input.

    Think something living.

    Attributes
        sensory Sensory: Object's sensory module.
        model Model: Object's model.
        memory Memory: Object's memory.
        tasker Tasker: Object's tasker.
        tags dict: Object's tags.
    """

    def __init__(self, id, sns=Sensory(), mod=Model(), mem=Memory.Memory([], [], True), tsk=Tasker(), tags=None):
        super().__init__(id, mod, mem, tsk, tags)
        self.sensory = sns

    def __str__(self):
        return "{}:[\n{},\n{},\n{},\n{},\n{}\n]".format(self.tags['id'], self.model, self.memory, self.sensory,
                                                        self.tasker, self.tags)


class User(DynamicObject):
    def __init__(self, id, prs=Personality(), sns=Sensory(), mod=Model(),
                 mem=Memory.Memory([], Memory.SegmentedMemory(), True),
                 tsk=Tasker(), tags=None):
        super().__init__(id, sns, mod, mem, tsk, tags)
        self.personality = prs

    def __str__(self):
        return "{}:[\n{},\n{},\n{},\n{},\n{},\n{}\n]".format(self.tags['id'], self.model, self.memory, self.personality,
                                                             self.sensory, self.tasker, self.tags)
