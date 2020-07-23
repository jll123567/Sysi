class Switcher:
    """
    Base class for Switcher type modules.
    Use this to create modules for switching between prefab modules.

    :param dict elements: The elements that can be swapped between.
        Format should be {"unique name of element": element}
    :param str current: The name of the currently used element.
    """

    def __init__(self, elements=None, current=None):
        if self.elements is None:
            self.elements = {}
        else:
            self.elements = elements
        self.current = current
        self._previous = None

    def setCurrent(self, name):
        """
        Set the current element to that of <name>.
        Sets previous.

        :param str name: The name of the element. Should be a valid index to elements.
        """
        self._previous = self.current
        self.current = name

    def switchWithPrevious(self):
        """Swap the contents of current and previous."""
        c = self.current
        self.current = self._previous
        self._previous = c

    def getCurrentFromElements(self):
        """Return an element from elements using current as the index."""
        if self.current is not None:
            return self.elements[self.current]
        else:
            return None


class ModelSwitcher(Switcher):
    """
    Switcher for model.

    :param Taskable owner: The owner of this module.
    :param dict elements: The elements that can be swapped between.
        Format should be {"unique name of element": element}
    :param str current: The name of the currently used element.
    """

    def __init__(self, owner, elements=None, current=None):
        self.owner = owner
        if elements is None:
            super().__init__()
        else:
            super().__init__(elements, current)

    def setCurrentModel(self, name):
        """
        Set the current Model using <name>.
        Sets previous.

        :param str name: The name of the element. Should be a valid index to elements.
        """
        self.setCurrent(name)
        self.owner.model = self.getCurrentFromElements()

    def switchModelWithPrevious(self):
        """Swap the contents of current and previous and set model."""
        self.switchWithPrevious()
        self.owner.model = self.getCurrentFromElements()


class PersonalitySwitcher(Switcher):
    """
    Switcher for personality.

    :param Taskable owner: The owner of this module.
    :param dict elements: The elements that can be swapped between.
        Format should be {"unique name of element": element}
    :param str current: The name of the currently used element.
    """

    def __init__(self, owner, elements=None, current=None):
        self.owner = owner
        if elements is None:
            super().__init__()
        else:
            super().__init__(elements, current)

    def setCurrentModel(self, name):
        """
        Set the current personality using <name>.
        Sets previous.

        :param str name: The name of the element. Should be a valid index to elements.
        """
        self.setCurrent(name)
        self.owner.personality = self.getCurrentFromElements()

    def switchModelWithPrevious(self):
        """Swap the contents of current and previous and set personality."""
        self.switchWithPrevious()
        self.owner.personality = self.getCurrentFromElements()
