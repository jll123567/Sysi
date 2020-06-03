"""
The Server

Classes
    SysServer
"""
import asyncio
import base64
import pickle
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

    def run(self):
        """

        """
        for dir in self.directories:  # Start directories and sessions.
            dir.start()
        while self.live:
            # Handle requets from server.

            objs = asyncio.run(self.scanForNetworkedObject())  # Find all the networked objects to send.
            asyncio.gather(*(self.sendNetworkObject(o) for o in objs))  # Send all networked objects concurrently.

        for dir in self.directories:  # Kill directories on server kill.
            dir.live = False

    async def scanForNetworkedObject(self):
        """

        :return: Networked objects.
        :rtype: list
        """
        netObjs = []
        async for dirr in self.directories:  # run though all directories and allow execution to move.
            async for ses in dirr.sessionList:  # run though all sessions in dirr and allow execution to move.
                for obj in ses.objectList:  # run though all objects in ses but be blocking at this part.
                    if "networkObject" in obj.tags.keys():
                        netObjs.append(obj)
        return netObjs

    async def sendNetworkObject(self, obj):
        """

        :param Tagable obj:
        """
        address, port = self.clientLookupTable[obj.tags["networkObject"]]  # Lookup the address and port of the client.
        writer = (await asyncio.open_connection(address, port))[1]  # Open a connection and get the writer.
        obj = base64.b64encode(pickle.dumps(obj))
        writer.write(obj)
        await writer.drain()
