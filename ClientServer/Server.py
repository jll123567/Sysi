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
            self.directoryList = []
        else:
            self.directoryList = dirs
        self.clientLookupTable = {}
        self.live = True

    def run(self):
        """

        """
        for dirr in self.directoryList:  # Start directories and sessions.
            dirr.start()
        asyncio.run(self.main())
        for dirr in self.directoryList:  # Kill directories on server kill.
            dirr.live = False

    async def main(self):
        """

        """
        sockSrv = await asyncio.start_server(self.handleClient, port=8426)
        try:
            await asyncio.gather(sockSrv.serve_forever(), self.taskManager())
        except asyncio.CancelledError:
            print("Tasks canceled. Live: {}".format(self.live))  # debug

    async def sendNetworkedObjects(self):
        """

        :return: Networked objects.
        :rtype: list
        """
        while self.live:
            netObjs = []
            await asyncio.sleep(0)
            for dirr in self.directoryList:  # run though all directories and allow execution to move.
                for ses in dirr.sessionList:  # run though all sessions in dirr and allow execution to move.
                    for obj in ses.objectList:  # run though all objects in ses but be blocking at this part.
                        if "networkObject" in obj.tags.keys():
                            netObjs.append(obj)
            await asyncio.gather(*(self.sendNetworkObject(obj) for obj in netObjs))

    async def sendNetworkObject(self, obj):
        """

        :param Tagable obj:
        """
        try:
            address, port = self.clientLookupTable[
                obj.tags["networkObject"]]  # Lookup the address and port of the client.
            writer = (await asyncio.open_connection(address, port))[1]  # Open a connection and get the writer.
        except ConnectionRefusedError:
            # print("connect refused. ending...")  # debug
            return
        except KeyError:
            # print("client not found. ending...")  # debug
            return
        objDt = base64.b64encode(pickle.dumps(obj))
        writer.write(b"obj:" + objDt + b":end")
        try:
            await writer.drain()
        except ConnectionResetError:
            # print("connection reset. ending...")  # debug
            return
        writer.close()
        await writer.wait_closed()

    async def handleClient(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Read and handle data from the client.

        :param StreamReader reader: Data from client to read.
        :param StreamWriter writer: Unused
        """
        connected = True
        lastMessage = time.monotonic()
        while connected:
            if reader.at_eof():
                if time.monotonic() >= (
                        lastMessage + (60 * 5)):  # If its been five minutes since last message, disconnect.
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
                cliId = await self.registerNewClient(data)
                asyncio.create_task(self.continuousSend(cliId, writer))
            elif dataType == b"disconnect":  # disconnect::end
                connected = False

        await writer.drain()  # cleanup for disconnect.
        writer.write(b"disconnect::end")
        await writer.drain()
        writer.write_eof()
        writer.close()
        await writer.wait_closed()

    async def registerNewClient(self, data):
        """
        Add a new entry to the clientLookupTable.

        :param bytes data: The data from the client.
            <cliId>:<address>:<port> where cliId, address, and port are base64 encoded.
        :return: Client Id
        :rtype: str
        """
        data = data.split(b":")  # <cliId>:<address>:<port> -> [cliId, address, port]
        newData = []
        for idx in range(data.__len__()):  # Base64 decode and convert to string.
            newData.append(base64.b64decode(data[idx]).decode())
        self.clientLookupTable[newData[0]] = (
            newData[1], int(newData[2]))  # add {<cliId>:(<address>, <port>)} to cliLookupTable.
        return newData[0]  # return client Id

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

    async def receiveShift(self, data):
        """

        :param bytes data: <objectId>:<shift>:<idx>
        """
        data = data.split(b":")  # <objectId>:<shift>:<idx> -> [<objectId>, <shift>, <idx>]
        objId = base64.b64decode(data[0]).decode()
        shift = pickle.loads(base64.b64decode(data[1]))  # assuming shift is pickled b64-encoded Shift.
        idx = base64.b64decode(data[2]).decode()  # idx is either an int for insert or "append" to append.
        o = None
        for dirr in self.directoryList:
            for ses in dirr.sessionList:
                await asyncio.sleep(0)
                for obj in ses.objectList:
                    if obj.tags["id"] == objId:
                        o = obj
                        break
                if o is not None:
                    break
            if o is not None:
                break
        if idx == "append":
            o.tasker.shifts.append(shift)
        else:
            try:
                o.tasker.shifts.insert(int(idx))
            except ValueError:
                pass  # ???

    async def receiveObject(self, data):
        """

        :param bytes data: <dirId>:<sesId>:<object>
        """
        data = data.split(b":")  # <dirId>:<sesId>:<object> -> [<dirId>, <sesId>, <object>]
        dirId = base64.b64decode(data[0]).decode()
        sesId = base64.b64decode(data[1]).decode()
        obj = pickle.loads(base64.b64decode(data[2]))
        for dirr in self.directoryList:
            if dirr.tags["id"] == dirId:
                for ses in dirr.sessionList:
                    if ses.tags["id"] == sesId:
                        ses.addObject(obj)
                        return

    async def continuousSend(self, cliId, writer):
        """

        :param str cliId: Client Id
        :param StreamWriter writer: Writer to client.
        """
        cliObj = None
        while self.live and not writer.is_closing():
            if cliObj is None or ("networkObject" not in cliObj.tags.keys()) or cliObj.tags["networkObject"] != cliId:
                # acquire the networkObject
                cliObj = None
                for dirr in self.directoryList:  # run though all directories and allow execution to move.
                    for ses in dirr.sessionList:  # run though all sessions in dirr and allow execution to move.
                        await asyncio.sleep(0)
                        for obj in ses.objectList:  # run though all objects in ses but be blocking at this part.
                            if ("networkObject" in obj.tags.keys()) and obj.tags['networkObject'] == cliId:
                                cliObj = obj
                                break  # Exit loop on acquisition
                        if cliObj is not None:  # Exit loop on acquisition
                            break
                    if cliObj is not None:  # Exit loop on acquisition
                        break
            objDt = base64.b64encode(pickle.dumps(cliObj))
            writer.write(b"obj:" + objDt + b":end")
            try:
                await writer.drain()
            except ConnectionResetError:
                # print("connection reset. ending...")  # debug
                return
