"""
Module for sensory in/out.

Classes
    Sensory
    SensoryModule
    Visual
"""
from sysObjects.Data import Data


class Sensory:
    """
    Module that holds an object's sensory in/out from/to the session.

    visual, auditory, tactile, taste, and smell are reserved for what you'd expect.
    If a module is un-used. Put None in its place.
    Feel free to add your own stuff to Sensory.

    :param Visual vis: Reserved space for visual input.
    :param Auditory aud: Reserved space for auditory io.
    :param Tactile tact: Reserved space for tactile input.
    :param Taste tst: Reserved space for taste input.
    :param Smell sml: Reserved space for smell input.
    """

    def __init__(self, vis=None, aud=None, tact=None, tst=None, sml=None):
        """Constructor"""
        self.visual = vis
        self.auditory = aud
        self.tactile = tact
        self.taste = tst
        self.smell = sml

    def __str__(self):
        return "vis:{}, aud:{}, tact:{}, tst:{}, sml:{}".format(self.visual is not None, self.auditory is not None,
                                                                self.tactile is not None, self.taste is not None,
                                                                self.smell is not None)


class SensoryModule:
    """
    Abstract class for sensory modules.

    Please implement all methods.

    :param any i: Input from session.
    :param any o: Output to session.
    """

    def __init__(self, i=None, o=None):
        self.i = i
        self.o = o

    def __str__(self):
        """You should implement this."""
        pass

    def package(self, inOrOut: bool):
        """Implement this as to return useful data object."""
        if inOrOut:  # True for in, False for out.
            return None
        else:
            return None


class Visual(SensoryModule):
    """
    Class for holding and handling visual input.

    There is no sensory output from this module so it is left as None.

    Attributes
        i (some visual input format): Visual input from session.
        o None: Unused.

    Methods
        package(bool inOrOut=True): Package visual input as a data object.
    """

    def __init__(self, i=None):
        super().__init__(i)  # TODO: Vis out holds camera info for session.

    def __str__(self):
        return "image?:{}".format(self.i is not None)

    def package(self, inOrOut=True):
        """
        Package visual input as a data object.

        if <inOrOut> is false this function returns None.

        :param bool inOrOut: Weather to return self.in or self.out.
        :return: The packaged data.
        :rtype: Data/None
        """
        if inOrOut:
            d = Data(None, self.i)
            d.setDataType("visual")
            return d
        else:
            return None
