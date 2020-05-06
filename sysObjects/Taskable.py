"""
Module for the Taskable class.

Classes
    Taskable
"""
from sysObjects.Tagable import Tagable
from sysModules.Tasker import Tasker


class Taskable(Tagable):
    """
    Abstract class for sysObjects that have a tasker.

    All sysObjects in sysi that plan to use a tasker should inherit from this class.
    Inherits from Tagable.

    Attributes
        tasker(Tasker): The tasker for this object.
        tags(dict): The tags for this object.
    """

    def __init__(self, tsk=Tasker(), tags=None):
        """
        Constructor

        tasker defaults to a new Tasker.
        Check Tagable for how to format tags.

        Parameters
            tsk Tasker: The tasker this object will use.
            tags dict: The tags this object will use.
        """
        super().__init__(tags)
        self.tasker = tsk
