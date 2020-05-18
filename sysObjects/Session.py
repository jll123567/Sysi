from sysObjects.Tagable import Tagable
from threading import Thread


class Session(Thread, Tagable):
    def __init__(self, id, obj=None, scn=None, rul=None, tags=None):
        super().__init__()
        if tags is None:
            self.tags = {}
        else:
            self.tags = tags
        self.objectList = obj
        self.scene = scn
        self.rules = rul
        self.tags["id"] = id
        self.live = True

    def __str__(self):
        aliveOrDead = "Dead"
        if self.live:
            aliveOrDead = "Alive"
        return "{}:{}\nobjects:{}\n{}".format(self.tags["id"], aliveOrDead, self.objectList.__len__(), self.tags)

    def getObjectFromId(self, id: str):
        """Get the object with a matching id tag."""
        for o in self.objectList:
            try:
                if id == o.tags["id"]:
                    return o
            except AttributeError:
                # Error for object with no tags.
                # print("{} object found with no tags.".format(type(o)))
                pass
        return None

    def update(self):
        pass

    def collect(self):
        pass

    def check(self):
        pass

    def execute(self):
        pass

    def log(self):
        pass

    def cleanup(self):
        pass

    def run(self):
        pass
