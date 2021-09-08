"""
Classes for actual things.

Classes
    :class:`StaticObject`, :class:`DynamicObject`, :class:`User`
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
    :param mod: The object's model, defaults to Model().
    :type mod: Model, optional
    :param mem: The object's memory, defaults to Memory().
    :type mem: Memory, optional
    :param tsk: The object's tasker, defaults to Tasker().
    :type tsk: Tasker, optional
    :param tags: The object's tags, defaults to {"id": <id>, "permissions": [[],[]]}.
    :type tags: dict, optional
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
        Append a reference to self at `requester`'s short term memory.

        The reference is a :class:`Data` object with an id of `None` and who's storage is (self's id, self).

        :param StaticObject requester: The object that requested the reference to self.
        """
        reference = Data(None, (self.tags["id"], self))
        reference.tags["dataType"] = "passReference"
        requester.memory.sts.append(reference)


class DynamicObject(StaticObject):
    """
    An object with long term memory and sensory input.

    Think something living.

    :param str id: The object's id.
    :param sns: The object's :class:`Sensory` module, one will be made if none is provided.
    :type sns: Sensory, optional
    :param mod: The object's :class:`Model` module, one will be made if none is provided.
    :type mod: Model, optional
    :param mem: The object's :class:`Memory` module, one will be made if none is provided.
    :type mem: Memory, optional
    :param tsk: The object's :class:`Tasker` module, one will be made if none is provided.
    :type tsk: Tasker, optional
    :param tags: The object's tags, will make new tags if none is provided, id tag will be set to `id`.
    :type tags: dict, optional
    """

    def __init__(self, id, sns=None, mod=None, mem=None, tsk=None, tags=None):
        """Constructor"""
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

    :param str id: The object's id.
    :param prs: The user's :class:`Personality` module, one will be made if none is provided.
    :type prs: Personality, optional
    :param sns: The object's :class:`Sensory` module, one will be made if none is provided.
    :type sns: Sensory, optional
    :param mod: The object's :class:`Model` module, one will be made if none is provided.
    :type mod: Model, optional
    :param mem: The object's :class:`Memory` module, one will be made if none is provided.
    :type mem: Memory, optional
    :param tsk: The object's :class:`Tasker` module, one will be made if none is provided.
    :type tsk: Tasker, optional
    :param tags: The object's tags, will make new tags if none is provided. Id tag will be set to `id`.
    :type tags: dict, optional
    """

    def __init__(self, id, prs=None, sns=None, mod=None, mem=None, tsk=None, tags=None):
        """Constructor"""
        if mem is None:
            mem = Memory.Memory([], Memory.SegmentedMemory(), True)
        super().__init__(id, sns, mod, mem, tsk, tags)
        if prs is None:
            self.personality = Personality()
        else:
            self.personality = prs
