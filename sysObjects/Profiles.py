"""
Profile stuff

Classes:
    :class:`Profile`
    :class:`GeneticProfile`
"""
from random import Random


# TODO: This needs to be entirely redone.
class Profile:
    """
    Produce objects randomly.

    Overload :py:meth:`factoryProfile` and use it to produce objects using random values.

    :param int mainSeed: The seed for the :py:attr:`mainRandom` used to generate seeds for Randoms in produceRandint,
        defaults to ``None``.
    :param tuple mainState: A state to use for :py:attr:`mainRandom`, defaults to ``None``, not used if set to ``None``.
    """

    def __init__(self, mainSeed=None, mainState=None):
        if mainSeed is None:
            self.mainRandom = Random()
        else:
            self.mainRandom = Random(mainSeed)
            self.mainSeed = mainSeed
        if mainState is not None:
            self.mainRandom.setstate(mainState)

    def produceRandint(self, rRange):
        """
        Produce an object using :py:meth:`factoryProfile` and a :py:class:`Random` produced by :py:attr:`rRange`.

        :param tuple rRange: Range of ints to use when making a seed for the random passed to :py:attr:`factoryProfile`.
        :return: An object defined by factoryProfile.
        :rtype: any
        """
        return self.factoryProfile(Random(self.mainRandom.randint(rRange[0], rRange[1])))

    def produceRand(self):
        """
        Produce an object using :py:meth:`factoryProfile` and a :py:class:`Random`.

        :return: An object defined by :py:meth:`factoryProfile`.
        :rtype: any
        """
        return self.factoryProfile(Random())

    def produceSeed(self, seed):
        """
        Produce an object using :py:meth:`factoryProfile` and :py:class:`Random` with `seed`.

        :param int seed: The seed for the :py:class:`Random` passed to :py:meth:`factoryProfile`.
        :return: An object defined by factoryProfile.
        :rtype: any
        """
        return self.factoryProfile(Random(seed))

    def getMainRandomState(self):
        """
        Get the state of the :py:attr:`mainRandom`.

        :return: The state of :py:attr:`mainRandom`.
        :rtype: tuple
        """
        return self.mainRandom.getstate()

    @staticmethod
    def factoryProfile(rand):
        """
        Overload this method. Take the :py:class:`Random` and output an object.

        :param Random rand: The :py:class:`Random` that you use to create your object.
        :return: The object you make.
        :rtype: any
        """
        return


class GeneticProfile:
    """
    Produce objects based on values from their parents.

    Overload :py:meth:`factoryProfile` and use it to produce objects using semi-random values.

    :param walkBounds: Bounds for how far to randomly walk averaged values from parents.
        A single float can be used for all walks or a list of floats can be used to specify bounds for each value.
    :type walkBounds: float or list
    :param int mainSeed: The seed for the :py:attr:`mainRandom` used to generate seeds for Randoms in
        :py:meth:`produceRandint`. If ``None`` is provided then dont provide a seed for the :py:attr:`mainRandom`.
        Defaults to ``None``.
    :type mainSeed: int or None
    :param tuple mainState: A state to use for py:attr:`mainRandom`, defaults to ``None``, not used if set to ``None``.
    """

    def __init__(self, walkBounds, mainSeed=None, mainState=None):
        if mainSeed is None:
            self.mainRandom = Random()
        else:
            self.mainRandom = Random(mainSeed)
            self.mainSeed = mainSeed
        if mainState is not None:
            self.mainRandom.setstate(mainState)
        self.walkBounds = walkBounds

    @staticmethod
    def getLongest(vals):
        """
        Get the length of the longest sublist of ``vals``.

        :param list vals: A ``list`` of lists.
        :return: The length of the longest sublist of vals.
        :rtype: int
        """
        longest = 0  # Get length of longest parent.
        for parent in vals:
            if longest < parent.__len__():
                longest = parent.__len__()
        return longest

    @staticmethod
    def convertToSetsList(vals, longest):
        """
        Convert vals from a ``list`` of parents values to a list of the 0 to nth of value from each parent.

        The length of the outputted lists of values are determined by longest.

        :param list vals: The list of values to convert the formatting of.
        :param int longest: The length of the parent values which have the longest length.
        :return: The converted values.
        :rtype: list
        """
        sets = []  # Go from  vals = [<parent>, ...] parent=[<num>, ...]
        # to sets = [<numSet>, ...] numSet = [<numFromParent>, ...].
        for idx in range(longest):
            numSet = []
            for parent in vals:
                try:  # If a list is shorter than longest. When trying to index an out of bound value just skip this
                    # list.
                    numSet.append(parent[idx])
                except IndexError:
                    pass
            sets.append(numSet)
        return sets

    @staticmethod
    def average(vals):
        """
        Take a ``list`` of lists of values and return the average of each list's values.

        :param list vals: A ``list`` of lists of values.
        :return: A ``list`` of averages.
        :rtype: list
        """
        for idx in range(vals.__len__()):  # Average each numSet
            some = 0
            for num in vals[idx]:
                some += num
            vals[idx] = some / vals[idx].__len__()
        return vals

    def applyRandomWalk(self, val, walkBounds):
        """
        Add a random value between ``-randomWalk`` and ``randomWalk`` to ``val``.

        :param float val: ``List`` of values to apply the walk to.
        :param float walkBounds: The bounds between to get the value of represented by one value.
        :return: Walked value.
        :rtype: float
        """
        rand = self.mainRandom
        return val + rand.triangular((-1 * walkBounds), walkBounds)

    def applyRandomWalks(self, vals, walkBounds):
        """
        Apply a Random walk to eac value in <vals>. Bounds are defined by walkBounds.

        Where the length of vals and walkBounds mismatch a walk wont be applied so keep them same length.

        :param list vals: The list of values to apply walks to.
        :param float/list walkBounds: The bound for each value. Can use a single float for all values.
        :return: List of walked values.
        :rtype: list
        """
        bounds = []
        if isinstance(walkBounds, int):
            for _ in range(vals.__len__()):
                bounds.append(walkBounds)
        else:
            bounds = walkBounds

        for idx in range(vals.__len__()):
            try:
                vals[idx] = self.applyRandomWalk(vals[idx], bounds[idx])
            except IndexError:  # If bounds are shorter than averages. Don't apply walk.
                pass
        return vals

    def produceWithParents(self, pVals):
        """
        Produce an object using a list of values from multiple parents and the :py:meth:`factoryProfile`.

        This method creates a list of average values from the values of all the parents. Then applies a random walk to
        each average who's bounds are defined by :py:attr:`walkBounds`. It then feeds these walked averages into
        :py:meth:`factoryProfile` and returns the the averages and produced object in a tuple.

        :param list pVals: List of the input values from each parent.
        :return: Tuple of the values fed into :py:meth:`factoryProfile`.
        :rtype: tuple
        """
        longest = self.getLongest(pVals)
        sets = self.convertToSetsList(pVals, longest)
        averages = self.average(sets)
        averages = self.applyRandomWalks(averages, self.walkBounds)
        return averages, self.factoryProfile(averages)

    def getMainRandomState(self):
        """
        Get the state of the :py:attr:`mainRandom`.

        :return: The state as a Tuple
        :rtype: tuple
        """
        return self.mainRandom.getstate()

    @staticmethod
    def factoryProfile(vals):
        """
        Overload this method. Take the :py:class:`Random` and output an object.

        :param list vals: List of values.
        :return: What you return.
        :rtype: any
        """
        return
