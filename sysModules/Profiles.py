"""
Profile stuff

Classes:
    Profile
    GeneticProfile
"""
from random import Random


class Profile:
    """
    Produce objects randomly.

    Overload factoryProfile and use it to produce objects using random values.

    :param int mainSeed: The seed for the mainRandom used to generate seeds for Randoms in produceRandint, defaults to
        None.
    :param tuple mainState: A state to use for mainRandom, defaults to None, not used if set to None.
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
        Produce an object using factoryProfile and a Random produced by <rRange>.

        :param tuple rRange: Range of ints to use when making a seed for the random passed to factoryProfile.
        :return: An object defined by factoryProfile.
        """
        return self.factoryProfile(Random(self.mainRandom.randint(rRange[0], rRange[1])))

    def produceRand(self):
        """
        Produce an object using factoryProfile and a Random().

        :return: An object defined by factoryProfile.
        """
        return self.factoryProfile(Random())

    def produceSeed(self, seed):
        """
        Produce an object using factoryProfile and Random with <seed>.

        :param int seed: The seed for the Random passed to factoryProfile.
        :return: An object defined by factoryProfile.
        """
        return self.factoryProfile(Random(seed))

    def getMainRandomState(self):
        """
        Get the state of the mainRandom.
        :return: The state as a Tuple
        """
        return self.mainRandom.getstate()

    @staticmethod
    def factoryProfile(rand):
        """
        Overload this method. Take the Random <rand> and output an object.

        :param Random rand: The Random.
        :return: What you return.
        :rtype: Any
        """
        return
