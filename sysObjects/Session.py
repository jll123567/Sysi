"""
Module for session.

Classes
    Session(Thread, Tagable)
"""
from sysObjects.Tagable import Tagable
from sysObjects.Taskable import Taskable
from threading import Thread


class Session(Thread, Tagable):
    """
    An instance of objects that interact with each-other.

    Like a live Universe.

    Attributes
        _ops [Operation]: Operations to execute in current shift.
        directory Directory: The Directory that this session is within.
        objectList [object]: The objects in the session.
            Preferably they are all Taskable.
        scene Scene: The scene to save shifts to.
        rules [Operation]: List of operations to run every shift.
        tags dict: Tags.

    Tags
        id str: Session's id.
            Format: "dr/<directory>/un/<universe this session represents>"
        errs [BaseExecption]: Stores all logged exceptions.
        opLog [tuple]: Stores executed ops.
            Format: (<function>, <target>, <source>)

    Methods
        getObjectFromId(str objectId) -> Tagable: Get the object with a matching id tag.
        update(): Preform all the operations of a shift.
        objectOpCollect(): Get operations from objects in objectList.
        ruleOpCollect(): Get operations from rules.
        objectOpCheck(Operation op) -> bool: Check an operation from an object and return True if its good and false if
            its bad.
        fullOpCheck(Operation op) -> bool: Check an operation from an object or rules and return True if its good and
            false if its bad.
        resolve(): Change keywords and ids in Operations to references to the actual objects.
        execute(Operation op): Take an operation and execute the listed function on the target object or objects.
        log(): Save details of what happened this shift to various locations.
        cleanup(): Cleanup the session for the next shift.
        run(): Obligatory run method.
            Called with start().
    """

    def __init__(self, sesId, parentDir, obj, scn=None, rul=None, tags=None):
        super().__init__()  # Init thread
        self._ops = []
        if tags is None:
            self.tags = {}
        else:
            self.tags = tags
        self.directory = parentDir
        self.objectList = obj
        self.scene = scn
        self.rules = rul
        self.tags["id"] = sesId
        self.tags["errs"] = []
        self.tags["opLog"] = []
        self.live = True

    def __str__(self):
        aliveOrDead = "Dead"
        if self.live:
            aliveOrDead = "Alive"
        return "{}:{}:objects:{}".format(self.tags["id"], aliveOrDead, self.objectList.__len__())

    def getObjectFromId(self, objId):
        """
        Get the object with a matching id tag.

        :param str objId: The id to match for.
        :return: The object with matching id.
        :rtype: Tagable
        """
        for o in self.objectList:
            try:
                if objId == o.tags["id"]:
                    return o
            except AttributeError:
                # Error for object with no tags.
                # print("{} object found with no tags.".format(type(o)))
                pass
        return None

    def update(self):
        """Preform all the operations of a shift."""
        self.objectOpCollect()  # get object ops
        for op in self._ops:  # check em all
            if not self.objectOpCheck(op):  # if they are bad make target none.
                op.target = "none"

        self.ruleOpCollect()  # get rule ops
        for op in self._ops:  # checking like before, but for different criteria.
            if not self.fullOpCheck(op):
                op.target = "none"

        self.resolve()  # Replace some things.
        for op in self._ops:
            self.execute(op)  # Call the functions on the objects.
        self.log()  # Log what happened.
        self.cleanup()  # Prepare for next shift.

    def objectOpCollect(self):
        """Get operations from objects in objectList."""
        for o in self.objectList:  # Get all ops from objects.
            try:
                objShift = o.tasker.__next__()  # Pops shift from o's tasker!
                for op in objShift:  # Pops op from objShift!
                    self._ops.append(op)
            except BaseException as e:
                self.tags["errs"].append(e)  # Log error

    def ruleOpCollect(self):
        """Get operations from rules."""
        for op in self.rules:  # Unlike in objectOpCollect, no popping.
            self._ops.append(op)

    @staticmethod
    def objectOpCheck(op):
        """
        Check an operation from an object and return True if its good and false if its bad.

        :param Operation op: The operation to check.
        :return: Operation's validity.
        :rtype: bool
        """
        if op.target == "all":  # all is not a valid target from objects.
            return False
        if not isinstance(op.source, (str, Taskable)):  # ops must have the object that created them as a source.(so
            # a str for id or a Taskable object at least)
            return False
        return True

    @staticmethod
    def fullOpCheck(op):
        """
        Check an operation from an object or rules and return True if its good and false if its bad.

        :param Operation op: The operation to check.
        :return: Operation's validity.
        :rtype: bool
        """
        if op.target is None:  # target should never be none. Use "none" as a keyword instead.
            return False
        return True

    def resolve(self):
        """Change keywords and ids in Operations to references to the actual objects."""
        for op in self._ops:
            if op.target == "none":  # Skip ops that wont run.(none is trg)
                continue
            for o in self.objectList:
                if op.target == o.tags["id"]:  # Replace the object's id with a reference to the object itself.
                    op.target = o
                if op.source == o.tags["id"]:
                    op.source = o

            if op.source == "ses":  # Not sure if this resolution is the best idea yet.
                op.source = self
            elif op.source == "dir":
                op.source = self.directory
            if op.target == "ses":
                op.target = self
            elif op.target == "dir":
                op.target = self.directory

            for pIdx in range(op.parameters.__len__()):
                if op.parameters[pIdx] == "trg":  # Replace trg keyword with target.
                    op.parameters[pIdx] = op.target
                elif op.parameters[pIdx] == "src":  # And so on...
                    op.parameters[pIdx] = op.source
                elif op.parameters[pIdx] == "ses":
                    op.parameters[pIdx] = self
                elif op.parameters[pIdx] == "dir":
                    op.parameters[pIdx] = self.directory
                elif op.parameters[pIdx] in ("\\trg", "\\src", "\\ses", "\\dir"):  # Replace escaped versions of
                    # keywords with the intended string(consume a \).
                    op.parameters[pIdx] = op.parameters[pIdx][1:]

    def execute(self, op):
        """
        Take an operation and execute the listed function on the target object or objects.

        :param Operation op: Operation to use for execution.
        """
        try:
            if op.target == "none":
                return
            elif op.target == "all":
                for o in self.objectList:
                    if op.parameters:
                        getattr(o, op.function)(*op.parameters)
                    else:
                        getattr(o, op.function)()
            else:
                if op.parameters:
                    getattr(op.target, op.function)(*op.parameters)
                else:
                    getattr(op.target, op.function)()
        except BaseException as e:
            self.tags["errs"].append(e)

    def log(self):
        """Save details of what happened this shift to various locations."""
        for op in self._ops:
            if op.target == "none":  # Skip if none
                continue
            if isinstance(op.target, Tagable):  # Grab object id
                trg = op.target.tags['id']
            else:
                trg = op.target  # If not id copy verbatim.
            if isinstance(op.source, Tagable):
                src = op.source.tags['id']
            else:
                src = op.source
            self.tags["opLog"].append((op.function, trg, src))  # Log format (function, target, source).

    def cleanup(self):
        """Cleanup the session for the next shift."""
        for o in self.objectList:  # Remove objects with no more shifts.(should this be enable-able/disable-able).
            if not o.tasker.shifts:
                self.objectList.remove(o)
        self._ops = []
        print("-----------Shift End-----------")  # TODO: remove this line.

    def run(self):
        """Obligatory run method; Called with start()."""
        while self.live:
            self.update()
            if not self.objectList:
                self.live = False
