"""
Module for the Taskable class.

Classes
    Taskable
"""
from objects.Tagable import Tagable
from sysModules.Tasker import Tasker


class Taskable(Tagable):
    """
    Abstract class for objects that have a tasker.

    All objects in sysi that plan to use a tasker should inherit from this class.
    Inherits from Tagable.

    Attributes
        tasker(Tasker): The tasker for this object.
        tags(dict): The tags for this object.

    Methods
        getTasker(): Return the tasker.
    """

    def __init__(self, tsk=None, tags=None):
        """
        Constructor

        tasker defaults to a new Tasker.
        Check Tagable for how to format tags.

        Parameters
            tsk Tasker: The tasker this object will use.
            tags dict: The tags this object will use.
        """
        super().__init__(tags)
        if tsk is None:
            self.tasker = Tasker()
            pass
        else:
            self.tasker = tsk

    def getTasker(self):
        """Return the tasker."""
        return self.tasker
