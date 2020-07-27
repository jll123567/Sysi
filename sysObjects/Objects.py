"""
Classes for actual things.

Classes
    StaticObject
    DynamicObject
    User
"""
from sysObjects.Data import Data
from sysObjects.Taskable import Taskable
import sysModules.Memory as Memory
from sysModules.Model import Model
from sysModules.Sensory import Sensory
from sysModules.Personality import Personality


class StaticObject(Taskable):
    """
    An object that has no long term memory.

    Think something that provides only basic utility, like a mug.

    :param str id: The object's id.
    :param Model mod: The object's model, defaults to Model().
    :param Memory mem: The object's memory, defaults to Memory().
    :param Tasker tsk: The object's tasker, defaults to Tasker().
    :param dict tags: The object's tags, defaults to {"id": <id>, "permissions": [[],[]]}.
    """

    def __init__(self, id, mod=None, mem=None, tsk=None, tags=None):
        """Constructor"""
        super().__init__(tsk, tags)
        self.tags["id"] = id
        self.tags["health"] = 100
        if mod is None:
            self.model = Model()
        else:
            self.model = mod
        if mem is None:
            self.memory = Memory.Memory()
        else:
            self.memory = mem

    def __str__(self):
        return self.tags['id']

    def passReference(self, requester):
        """
        Append a reference to self at <requester>'s short term memory.

        The reference is a data object with an id of None and who's storage is (self's id, self).

        :param StaticObject requester: The object that requested the reference to self.
        """
        reference = Data(None, (self.tags["id"], self))
        reference.tags["dataType"] = "passReference"
        requester.memory.sts.append(reference)


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

    def __init__(self, id, sns=None, mod=None, mem=None, tsk=None, tags=None):
        """
        Constructor

        Defaults
            sensory = Sensory()
            model = Model()
            memory = Memory([], [], True)
            tasker = Tasker()
            tags = {"id": <id>}

        Parameters
            id str: Id
            sns Sensory: sensory
            mod Model: model
            mem Memory: memory
            tsk Tasker: tasker
            tags dict: tags
        """
        if mem is None:
            mem = Memory.Memory([], [], True)
        super().__init__(id, mod, mem, tsk, tags)
        if sns is None:
            self.sensory = Sensory()
        else:
            self.sensory = sns


class User(DynamicObject):
    """
    An object with arbitrary tasker construction and segmented long term memory.

    ???

    Attributes
        personality Personality: User's personality.
        sensory Sensory: User's sensory module.
        model Model: User's model.
        memory Memory: User's memory.
        tasker Tasker: User's tasker.
        tags dict: User's tags.
    """

    def __init__(self, id, prs=None, sns=None, mod=None, mem=None, tsk=None, tags=None):
        """
        Constructor

        Defaults
            personality = Personality()
            sensory = Sensory()
            model = Model()
            memory = Memory([], Memory.SegmentedMemory(), True)
            tasker = Tasker()
            tags = {"id": <id>}

        Parameters
            id str: Id
            sns Sensory: sensory
            mod Model: model
            mem Memory: memory
            tsk Tasker: tasker
            tags dict: tags
        """
        if mem is None:
            mem = Memory.Memory([], Memory.SegmentedMemory(), True)
        super().__init__(id, sns, mod, mem, tsk, tags)
        if prs is None:
            self.personality = Personality()
        else:
            self.personality = prs
