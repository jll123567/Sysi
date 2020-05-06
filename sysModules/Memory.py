"""
Module for object's storage related stuff.

Classes
    Memory
    SegmentedMemory(unimplemented)
"""


class Memory:
    """
    Stores arbitrary sysObjects for use later.

    Storage is done in short term and long term.

    Attributes
        sts None/list: Short term is intended disposable stuff.
        lts None/list/SegmentedMemory(unimplemented): Long term is intended for non-disposable stuff.
        ltsEnable bool: Enable for long term storage.

    Methods
        enableLts(list/SegmentedMemory/None memory=None): Enable long term storage and set it to <memory>.
        disableLts(): Disable long term storage.
    """

    def __init__(self, sts=None, lts=None, ltsEnable=False):
        """
        Constructor

        If ltsEnable is false then lts is set to None.
        Short term storage and long term storage are set to an empty list by default.

        Parameters
            sts None/list: Short term storage.
            lts None/list/SegmentedMemory(unimplemented): Long term storage.
            ltsEnable bool: Enable for long term storage.
        """
        if sts is None:
            self.sts = []
        else:
            self.sts = sts
        if not ltsEnable:
            self.ltsEnable = False
            self.lts = None
        elif lts is None:
            self.ltsEnable = True
            self.lts = []
        else:
            self.ltsEnable = True
            self.lts = lts

    def __str__(self):
        if not self.ltsEnable:
            lts = "Disabled"
        else:
            # TODO: Implement SegmentedMemory.
            # if isinstance(self.lts, SegmentedMemory):
            #     lts = "Segmented"
            # else:
            lts = "Unsegmented"
        if self.sts:
            sts = "In use"
        else:
            sts = "Empty"
        return "[{}, {}]".format(sts, lts)

    def enableLts(self, memory=None):
        """Enable long term storage and set it to <memory>."""
        self.ltsEnable = True
        if memory is None:
            self.lts = []
        else:
            self.lts = memory

    def disableLts(self):
        """Disable long term storage."""
        self.ltsEnable = False
        self.lts = None

    def sortSts(self):
        """Unimplemented."""
        pass

    def sortLts(self):
        """Unimplemented."""
        pass
