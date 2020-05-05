""""""
# TODO: DOC ME
from objects.Tagable import Tagable
from sysModules.Tasker import Tasker


class Taskable(Tagable):
    """"""

    def __init__(self, tsk=None, tags=None):
        """"""
        super().__init__(tags)
        if tsk is None:
            self.tasker = Tasker()
            pass
        else:
            self.tasker = tsk

    def getTasker(self):
        """Return the tasker."""
        return self.tasker
