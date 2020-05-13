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

    Attributes
        visual Visual: Reserved space for visual input.
        auditory Auditory: Reserved space for auditory io.
        tactile Tactile: Reserved space for tactile input.
        taste Taste: Reserved space for taste input.
        smell Smell: Reserved space for smell input.
    """

    def __init__(self, vis=None, aud=None, tact=None, tst=None, sml=None):
        """
        Constructor

        All sensory modules are defaulted to None.

        Parameters
            vis Visual/None: Reserved for visual.
            aud Auditory/None: Reserved for auditory.
            tact Tactile/None: Reserved for tactile.
            tst Taste/None: Reserved for taste.
            sml Smell/None: Reserved for smell.
        """
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

    Attributes
        i any: Input from session.
        o any: Output to session.

    Methods
        package(inOrOut bool): Implement this as to return useful data object.
    """

    def __init__(self, i=None, o=None):
        self.i = i
        self.o = o

    def __str__(self):
        """You should implement this."""
        pass

    def package(self, inOrOut):
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
        super().__init__(i, None)  # TODO: Vis out holds camera info for session.

    def __str__(self):
        return "image?:{}".format(self.i is not None)

    def package(self, inOrOut=True):
        """
        Package visual input as a data object.

        if <inOrOut> is false this function returns None.

        Parameters
            inOrOut bool: Weather to return self.in or self.out.
        """
        if inOrOut:
            d = Data(None, self.i)
            d.setDataType("visual")
            return d
        else:
            return None
