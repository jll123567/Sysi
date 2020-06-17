"""
The Server

Classes
    SysServer
"""
import asyncio
import base64
import pickle
import threading
import time
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
        for dirr in self.directories:  # Start directories and sessions.
            dirr.start()
        asyncio.run(self.main())
        for dirr in self.directories:  # Kill directories on server kill.
            dirr.live = False

    async def main(self):
        """

        """
        sockSrv = await asyncio.start_server(self.handleNetworkRequests, port=8426)
        try:
            await asyncio.gather(sockSrv.serve_forever(), self.sendNetworkedObjects(), self.taskManager())
        except asyncio.CancelledError:
            print("canceled")

    async def sendNetworkedObjects(self):
        """

        :return: Networked objects.
        :rtype: list
        """
        while self.live:
            netObjs = []
            await asyncio.sleep(0)
            for dirr in self.directories:  # run though all directories and allow execution to move.
                for ses in dirr.sessionList:  # run though all sessions in dirr and allow execution to move.
                    for obj in ses.objectList:  # run though all objects in ses but be blocking at this part.
                        if "networkObject" in obj.tags.keys():
                            netObjs.append(obj)
            await asyncio.gather(*(self.sendNetworkObject(obj) for obj in netObjs))

    async def sendNetworkObject(self, obj):
        """

        :param Tagable obj:
        """
        address, port = self.clientLookupTable[
            obj.tags["networkObject"]]  # Lookup the address and port of the client.
        writer = (await asyncio.open_connection(address, port))[1]  # Open a connection and get the writer.
        obj = base64.b64encode(pickle.dumps(obj))
        writer.write(obj)
        await writer.drain()

    async def handleNetworkRequests(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Read and handle data from the client.

        :param StreamReader reader: Data from client to read.
        :param StreamWriter writer: Unused
        """
        print("handleNetworkRequets hit")
        connected = True
        lastMessage = time.monotonic()
        while connected:
            if reader.at_eof():
                if time.monotonic() >= (lastMessage + 60):  # If its been a minute since last message, disconnect.
                    connected = False
                await asyncio.sleep(0)  # Pass execution while doing nothing.
                continue  # Otherwise wait for next message.
            lastMessage = time.monotonic()  # Store time message was received.
            dataType = (await reader.readuntil(b":"))[:-1]  # Separate data type header.
            data = (await reader.readuntil(b":end"))[:-4]  # Remove footer.
            if dataType == b"obj":  # obj:<dirId>:<sesId>:<object>:end
                await self.receiveObject(data)
            elif dataType == b"shift":  # shift:<objectId>:<shift>:<idx>:end
                await self.receiveShift(data)
            elif dataType == b"newConnection":  # newConnection:<cliId>:<address>:<port>:end
                await self.registerNewClient(data)
            elif dataType == b"disconnect":  # disconnect::end
                print("dc reached")
                connected = False

    async def registerNewClient(self, data):
        """
        Add a new entry to the clientLookupTable.

        :param bytes data: The data from the client.
            <cliId>:<address>:<port> where cliId, address, and port are base64 encoded.
        """
        data = data.split(b":")  # <cliId>:<address>:<port> -> [cliId, address, port]
        newData = []
        for idx in range(data.__len__()):  # Base64 decode and convert to string.
            newData.append(str(base64.b64decode(data[idx])))
        self.clientLookupTable[newData[0]] = (
            newData[1], newData[2])  # add {<cliId>:(<address>, <port>)} to cliLookupTable.

    async def taskManager(self):
        """

        """
        while self.live:
            await asyncio.sleep(0)
        tasks = asyncio.all_tasks()
        for task in tasks:
            try:
                task.cancel()
            except asyncio.CancelledError:
                pass

    async def receiveObject(self, data):
        """

        :param data:
        """
        data = data.split(b":")  # <dirId>:<sesId>:<object> -> [<dirId>, <sesId>, <object>]
        dirId = str(base64.b64decode(data[0]))
        sesId = str(base64.b64decode(data[1]))
        obj = pickle.loads(base64.b64decode(data[0]))
        for dirr in self.directories:
            if dirr.tags["id"] == dirId:
                for ses in dirr.sessions:
                    if ses.tags["id"] == sesId:
                        ses.addObject(obj)

    async def receiveShift(self, data):
        """

        :param data:
        """
        data = data.split(b":")  # <objectId>:<shift>:<idx> -> [<objectId>, <shift>, <idx>]
        objId = str(base64.b64decode(data[0]))
        shift = pickle.loads(base64.b64decode(data[1]))  # assuming shift is pickled b64-encoded Shift.
        idx = str(base64.b64decode(data[0]))  # idx is either an int for insert or "append" to append.
        o = None
        for dirr in self.directories:
            for ses in dirr.sessions:
                for obj in ses.objectList:
                    if obj.tags["id"] == objId:
                        o = obj
        if idx == "append":
            o.tasker.shifts.append(shift)
        else:
            try:
                o.tasker.shifts.insert(int(idx))
            except ValueError:
                pass  # ???
