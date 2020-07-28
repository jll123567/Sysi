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

    :param int mainSeed: The seed for the mainRandom used to generate seeds for Randoms in produceRand.
    """

    def __init__(self, mainSeed):
        self.mainRandom = Random(mainSeed)

    def produceRand(self, rRange):
        """
        Produce an object using factoryProfile and a Random produced by <rRange>.

        :param tuple rRange: Range of ints to use when making a seed for the random passed to factoryProfile.
        :return: An object defined by factoryProfile.
        """
        return self.factoryProfile(Random(self.mainRandom.randint(rRange[0], rRange[1])))

    def produceSeed(self, seed):
        """
        Produce an object using factoryProfile and Random with <seed>.

        :param int seed: The seed for the Random passed to factoryProfile.
        :return: An object defined by factoryProfile.
        """
        return self.factoryProfile(Random(seed))

    @staticmethod
    def factoryProfile(rand):
        """
        Overload this method. Take the Random <rand> and output an object.

        :param Random rand: The Random.
        :return: What you return.
        :rtype: Any
        """
        return
