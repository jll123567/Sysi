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
            print("server Ready")
        except asyncio.CancelledError:
            print("Tasks canceled. Live: {}".format(self.live))  # debug

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

    async def handleClient(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Read and handle data from the client.

        :param StreamReader reader: Data from client to read.
        :param StreamWriter writer: Unused
        """
        connected = True
        lastTime = time.monotonic()
        while connected:
            try:
                dataType = (await reader.readuntil(b":"))[:-1]  # Separate data type header.
                data = (await reader.readuntil(b":end"))[:-4]  # Remove footer.
            except asyncio.IncompleteReadError:
                print("client disconnected unexpectedly")  # debug
                return  # Exit due to client disconnect.
            except ConnectionResetError:
                print("client disconnected unexpectedly")  # debug
                return  # Exit due to client disconnect.

            if time.monotonic() >= (lastTime + (60 * 5)):  # DC for timeout
                break

            if dataType == b"obj":  # obj:<dirId>:<sesId>:<object>:end
                await self.receiveObject(data)
                print("server: got object")  # debug
            elif dataType == b"shift":  # shift:<objectId>:<shift>:<idx>:end
                await self.receiveShift(data)
                lastTime = time.monotonic()  # Store time object was received.
                print("server: got shift")  # debug
            elif dataType == b"newConnection":  # newConnection:<cliId>:<address>:<port>:end
                cliId = await self.registerNewClient(data)
                asyncio.create_task(self.continuousSend(cliId, writer))
                print("server: got connection")  # debug
            elif dataType == b"disconnect":  # disconnect::end
                print("server: got disconnect")  # debug
                break

        await writer.drain()  # cleanup for disconnect.
        writer.write(b"disconnect::end")
        await writer.drain()
        writer.write_eof()
        writer.close()
        print("server: disconnecting")  # debug
        await writer.wait_closed()

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
                pass  # this should never happen but if it does ignore the shift.

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

    async def continuousSend(self, cliId, writer):
        """

        :param str cliId: Client Id
        :param StreamWriter writer: Writer to client.
        """
        cliObj = None
        while self.live and not writer.is_closing():
            await asyncio.sleep(4)
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
            if cliObj is not None:
                objDt = base64.b64encode(pickle.dumps(cliObj))
                try:
                    writer.write(b"obj:" + objDt + b":end")
                    await writer.drain()
                except ConnectionResetError:
                    print("client connection reset. ending...")  # debug
                    return
                except RuntimeError:
                    print("writer from client closed. ending...")  # debug
