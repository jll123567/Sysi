"""
The Server

Classes
    SysServer
"""
import asyncio
import threading
import sysObjects.Tagable


class SysServer(threading.Thread, sysObjects.Tagable.Tagable):
    """

    """

    def __init__(self, srvId, dirs=None, tags=None):
        super().__init__()
        if tags is None:
            self.tags = {}
        else:
            self.tags = tags
        self.tags["id"] = srvId
        if dirs is None:
            self.directories = []
        else:
            self.directories = dirs
        self.clientLookupTable = {}
        self.live = True

    async def run(self):
        """

        """
        for dir in self.directories:  # Start directories and sessions.
            dir.start()
        while self.live:
            pass

        for dir in self.directories:  # Kill directories on server kill.
            dir.live = False

    async def scanForNetworkedObject(self):
        """

        :return:
        """
        netObjs = []
        async for dirr in self.directories:  # run though all directories and allow execution to move.
            async for ses in dirr.sessionList:  # run though all sessions in dirr and allow execution to move.
                for obj in ses.objectList:  # run though all objects in ses but be blocking at this part.
                    if "networkObject" in obj.tags.keys():
                        netObjs.append(obj)
        return netObjs
