"""
Module for object's storage related stuff.

Classes
    Memory
    SegmentedMemory
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
        getLts(): Get and return lts or lts.mem if lts is a SegmentedMemory object.
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
            if isinstance(self.lts, SegmentedMemory):
                lts = "Segmented"
            else:
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

    def getLts(self):
        """Get and return lts or lts.mem if lts is a SegmentedMemory object."""
        if isinstance(self.lts, SegmentedMemory):
            return self.lts.mem
        else:
            return self.lts

    def sortSts(self):
        """Unimplemented."""
        pass

    def sortLts(self):
        """Unimplemented."""
        pass

    def search(self, content, shortOrLong=False):
        """
        Find data in memory that has any matching content tags to that of <content>.
        :param list content: A list of strings to find in data objects.
            Elements in content are implicitly or'd.
        :param bool shortOrLong: Weather or not to look in sts or lts, defaults to false for sts.
        :return: Data objects with matching content tags.
        :rtype: list
        """
        resultsIdx = set()
        for c in content:
            if not shortOrLong:
                for d in self.sts:
                    if "content" in d.tags.keys() and c in d.tags["content"]:
                        resultsIdx.update([self.sts.index(d)])
            else:
                for d in self.lts:
                    if "content" in d.tags.keys() and c in d.tags["content"]:
                        resultsIdx.update([self.sts.index(d)])
        results = []
        if not shortOrLong:
            for idx in resultsIdx:
                results.append(self.sts[idx])
        else:
            for idx in resultsIdx:
                results.append(self.sts[idx])
        return results


class SegmentedMemory:
    """
    Segmented memory option.

    Effectively a dict where you can iterate through all values. Therefore its an iterator.
    Dict must be set up as the following.
        {<segments>}
        <segment> = <segment name>:[<elements>]
        <element> is any
        <segment name> is a string
        In other words a dict where all values are lists of something or other.

    Iteration effectively though not literally flattens the dict's values to one large list.
    if a segment is an empty list None is returned by next.
    If a segment has a value that is not a list it will be converted to a list by next.
        so <segment>:<value> becomes <segment>:[<value>]

    Attributes
        mem dict: The dictionary itself
        segment int: Counter for the segment for next.
        obj int: Counter for the element of the segment for next.
    """

    def __init__(self, mem=None):
        if mem is None:
            self.mem = {}
        else:
            self.mem = mem
        self.segment = 0
        self.obj = 0

    def __str__(self):
        """Return the str of mem."""
        return str(self.mem)

    def __iter__(self):
        return self

    def __next__(self):
        """
        Next

        This method converts values in to lists.
            None -> []
            else -> [else]

        This method will return none if the current segment is [].

        Return
         (the next element) any
        """
        if self.segment == list(self.mem.keys()).__len__():  # Check for stop iter
            self.segment = 0
            self.obj = 0
            raise StopIteration

        if not isinstance(self.mem[list(self.mem.keys())[self.segment]], list):  # Verify the segment contains a list.
            if self.mem[list(self.mem.keys())[self.segment]] is None:  # Convert otherwise.
                self.mem[list(self.mem.keys())[self.segment]] = []
            else:
                self.mem[list(self.mem.keys())[self.segment]] = [self.mem[list(self.mem.keys())[self.segment]]]

        if not self.mem[list(self.mem.keys())[self.segment]]:  # Get the object to return(None if segment is []).
            o = None
        else:
            o = self.mem[list(self.mem.keys())[self.segment]][self.obj]

        objSize = self.mem[list(self.mem.keys())[self.segment]].__len__()  # Increment counter
        if self.obj + 1 == objSize or objSize == 0:
            self.segment += 1
            self.obj = 0
        else:
            self.obj += 1

        return o  # Return.
