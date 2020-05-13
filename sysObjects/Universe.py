"""
Module for Universe

Classes
    Universe
"""

from sysObjects.Tagable import Tagable
from sysObjects.Taskable import Taskable
import sysObjects.Objects as Objects
from sysObjects.Data import Data
from sysObjects.Scene import Scene
# from sysObjects.Container import Container


class Universe(Tagable):
    """
    Storage method for a set of scenes and or a session.

    Attributes
        _lastId dict: Dictionary for id generation.
        timeline int: Sets the current timeline(which scenes describe the current state of the object list).
        sceneList [Scene]: List of all scenes relating to this uni.
        objectList [object]: List of all objects that can interact with each-other.
        containerList [Container]: All containers relevant to this universe.
        requiredFunctionSuite str/None: A string with all functions that need to be installed in taskable objects to work in
            this uni. None if unused
        rules [Operation]: Operations to be run on all objects every shift.
        tags dict: Tags for this uni.

    Methods
        assignId(object obj): Generate and set the id of <obj>.
        assignAllIds(): Assign ids for all objects in the universe.
        generateId(str objType): Generate an id.
        addObject(object obj): Add an object to the object list and generate an id for it.
        addScene(Scene scn): Add a scene to the scene list and generate an id for it.
        addContainer(Container cont): Add a container to the container list and generate an id for it.
        installRequiredFunctions(): Install the requiredFunctionSuite on all taskable objects in the object list.
    """

    def __init__(self, id, tl=0, scn=None, obj=None, cont=None, reqFunct=None, rule=None, tags=None):
        """
        Constructor

        Timeline defaults to 0.
        Scene, object, container, and rules lists default to an empty list.
        RequiredFucntionSuite default to None.
        _lastId is setup to have the first id generated be "00" for each type.

         Parameters
            id str: Uni id.
            tl=0 int: timeline
            scn list: sceneList
            obj list: objectList
            cont list: containerList
            reqFunct str: requiredFunctionSuite
            rule list: rules
            tags dict: tags
        """
        super().__init__(tags)
        self._lastId = {"u": -1, "so": -1, "do": -1, "t": -1, "d": -1, "sn": -1, "c": -1}
        self.tags["id"] = id
        self.timeline = tl
        if scn is None:
            self.sceneList = []
        else:
            self.sceneList = scn
        if obj is None:
            self.objectList = []
        else:
            self.objectList = obj
        if cont is None:
            self.containerList = []
        else:
            self.containerList = cont
        self.requiredFunctionSuite = reqFunct
        if rule is None:
            self.rules = []
        else:
            self.rules = rule

    def __str__(self):
        return "{}:\ntl:{}, scenes:{}, objects:{}, containers:{}, rules:{}\n{}".format(self.tags["id"], self.timeline,
                                                                                       self.sceneList.__len__(),
                                                                                       self.objectList.__len__(),
                                                                                       self.containerList.__len__(),
                                                                                       self.rules.__len__(),
                                                                                       self.tags)

    def assignId(self, obj):
        """
        Generate and set the id of <obj>.

        Ids are formatted as <srv or cli>/dr/<directoryId>/un/<universeId>/<object type>/<objectId><check character>
        User -> u
        DynamicObject -> do
        StaticObject -> so
        Taskable -> t
        Data -> d
        Scene -> sn
        Container -> c

        Parameters
            obj object: The object to set the Id of.
        """
        idStub = self.tags["id"]  # <srv>/dr/<directory>/un/<uni>
        if isinstance(obj, Objects.User):
            lastId = self._lastId["u"]  # Get, increment, and update the last id.
            lastId += 1
            self._lastId["u"] = lastId
            check = str(lastId)[-1]  # Generate check character.
            obj.tags["id"] = "{}/u/{}{}".format(idStub, lastId, check)  # Aaaaaand set.
        elif isinstance(obj, Objects.DynamicObject):  # You get the gist...
            lastId = self._lastId["do"]
            lastId += 1
            self._lastId["do"] = lastId
            check = str(lastId)[-1]
            obj.tags["id"] = "{}/do/{}{}".format(idStub, lastId, check)
        elif isinstance(obj, Objects.StaticObject):
            lastId = self._lastId["so"]
            lastId += 1
            self._lastId["so"] = lastId
            check = str(lastId)[-1]
            obj.tags["id"] = "{}/so/{}{}".format(idStub, lastId, check)
        elif isinstance(obj, Taskable):
            lastId = self._lastId["t"]
            lastId += 1
            self._lastId["t"] = lastId
            check = str(lastId)[-1]
            obj.tags["id"] = "{}/t/{}{}".format(idStub, lastId, check)
        elif isinstance(obj, Data):
            lastId = self._lastId["d"]
            lastId += 1
            self._lastId["d"] = lastId
            check = str(lastId)[-1]
            obj.tags["id"] = "{}/d/{}{}".format(idStub, lastId, check)
        elif isinstance(obj, Scene):
            lastId = self._lastId["sn"]
            lastId += 1
            self._lastId["sn"] = lastId
            check = str(lastId)[-1]
            obj.tags["id"] = "{}/sn/{}{}".format(idStub, lastId, check)
        # elif isinstance(obj, Container):
        #     lastId = self._lastId["c"]
        #     lastId += 1
        #     self._lastId["c"] = lastId
        #     check = str(lastId)[-1]
        #     obj.tags["id"] = "{}/c/{}{}".format(idStub, lastId, check)
        else:
            print("Object type not supported.\nNo changes where made.")

    def assignAllIds(self):
        """
        Generate ids for all objects in the universe.

        WARNING: this will reset all ids. Make sure all objects that originate from this uni are in its object list.
        """
        self._lastId = {"u": -1, "so": -1, "do": -1, "t": -1, "d": -1, "sn": -1, "c": -1}
        for i in self.sceneList:
            self.assignId(i)
        for i in self.objectList:
            self.assignId(i)
        for i in self.containerList:
            self.assignId(i)

    def generateId(self, objType):
        """
        Generate an id.

        Ids are formatted as <srv or cli>/dr/<directoryId>/un/<universeId>/<object type>/<objectId><check character>
        This method will set _lastId.
        User -> u
        DynamicObject -> do
        StaticObject -> so
        Taskable -> t
        Data -> d
        Scene -> sn
        Container -> c

        Parameters
            objType str: The type of the object you want to generate an id for.
        """
        idStub = self.tags["id"]  # <srv>/dr/<directory>/un/<uni>
        if objType == "u":
            lastId = self._lastId["u"]  # Get, increment, and update the last id.
            lastId += 1
            self._lastId["u"] = lastId
            check = str(lastId)[-1]  # Generate check character.
            return "{}/u/{}{}".format(idStub, lastId, check)  # Aaaaaand set.
        elif objType == "do":  # You get the gist...
            lastId = self._lastId["do"]
            lastId += 1
            self._lastId["do"] = lastId
            check = str(lastId)[-1]
            return "{}/do/{}{}".format(idStub, lastId, check)
        elif objType == "so":
            lastId = self._lastId["so"]
            lastId += 1
            self._lastId["so"] = lastId
            check = str(lastId)[-1]
            return "{}/so/{}{}".format(idStub, lastId, check)
        elif objType == "t":
            lastId = self._lastId["t"]
            lastId += 1
            self._lastId["t"] = lastId
            check = str(lastId)[-1]
            return "{}/t/{}{}".format(idStub, lastId, check)
        elif objType == "d":
            lastId = self._lastId["d"]
            lastId += 1
            self._lastId["d"] = lastId
            check = str(lastId)[-1]
            return "{}/d/{}{}".format(idStub, lastId, check)
        elif objType == "sn":
            lastId = self._lastId["sn"]
            lastId += 1
            self._lastId["sn"] = lastId
            check = str(lastId)[-1]
            return "{}/sn/{}{}".format(idStub, lastId, check)
        # elif objType == "c":
        #     lastId = self._lastId["c"]
        #     lastId += 1
        #     self._lastId["c"] = lastId
        #     check = str(lastId)[-1]
        #     return "{}/c/{}{}".format(idStub, lastId, check)
        else:
            print("Object type not supported.\nNo changes where made.")

    def addObject(self, obj):
        """Add an object to the object list and generate an id for it."""
        self.assignId(obj)
        self.objectList.append(obj)

    def addScene(self, scn):
        """Add a scene to the scene list and generate an id for it."""
        self.assignId(scn)
        self.sceneList.append(scn)

    def addContainer(self, cont):
        """Add a container to the container list and generate an id for it."""
        self.assignId(cont)
        self.containerList.append(cont)

    def installRequiredFunctions(self):
        """Install the requiredFunctionSuite on all taskable objects in the object list."""
        for o in self.objectList:
            if isinstance(o, Taskable):
                o.installFunctionSuite(self.requiredFunctionSuite)
