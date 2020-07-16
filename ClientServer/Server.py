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
    The server clients connect to. Also intended to run sessions that can communicate with eachother in a directory.

    :param str srvId: The server's Id.
    :param list dirs: The directories that this server owns, defaults to an empty list.
    :param int timeout: Time to wait for a message from a client before disconnecting in seconds,
        defaults to five minutes.
    :param dict tags: Tags like Tagable, defaults to {"id": <srvId>}.
    """

    def __init__(self, srvId, dirs=None, timeout=(5 * 60), tags=None):
        super().__init__()
        if tags is None:
            self.tags = {}
        else:
            self.tags = tags
        self.tags["id"] = srvId  # Set id.
        if dirs is None:
            self.directoryList = []
        else:
            self.directoryList = dirs
        self.timeout = timeout
        self.clientLookupTable = {}  # Holds info about clients that have connected in the past.
        self.live = True  # When false, server is kill.

    def __str__(self):
        if self.live:
            isAlive = "Alive"
        else:
            isAlive = "Dead"
        return "{}:{} Dirs:{}".format(self.tags["id"], self.directoryList.__len__(), isAlive)

    def run(self):
        """Code to run at thread start. Call with self.start()"""
        for dirr in self.directoryList:  # Start directories and sessions.
            dirr.start()
        asyncio.run(self.main())  # Start async tasks.
        for dirr in self.directoryList:  # Kill directories on server kill.
            dirr.live = False

    async def main(self):
        """
        Start the tasks to handle clients and the task manager.

        Handles CancelledError.
        """
        sockSrv = await asyncio.start_server(self.handleClient, port=8426)  # Start server on port 8426(hard coded)
        try:
            await asyncio.gather(sockSrv.serve_forever(), self.taskManager())  # Start handling clients and the task...
            # manager task
            print("server Ready")
        except asyncio.CancelledError:
            pass
            # print("Tasks canceled. Live: {}".format(self.live))  # debug

    async def taskManager(self):
        """Cancel all running tasks when self.live is false and handle CancelledErrors."""
        while self.live:
            await asyncio.sleep(0)  # Pass execution if the thread is still alive.
        tasks = asyncio.all_tasks()  # Get all running tasks.
        for task in tasks:
            try:
                task.cancel()  # Tasks...canceled!
            except asyncio.CancelledError:  # Ignore the CancelledErrors.
                pass

    async def handleClient(self, reader, writer):
        """
        Read and handle data from the client.

        :param StreamReader reader: Data from client to read.
        :param StreamWriter writer: Unused
        """
        connected = True
        lastTime = time.monotonic()  # Store the time.
        while connected:
            try:
                dataType = (await reader.readuntil(b":"))[:-1]  # Separate data type header.
                data = (await reader.readuntil(b":end"))[:-4]  # Remove footer.
            except asyncio.IncompleteReadError:
                # print("client disconnected unexpectedly")  # debug
                return  # Exit due to client disconnect.
            except ConnectionResetError:
                # print("client disconnected unexpectedly")  # debug
                return  # Exit due to client disconnect.

            if time.monotonic() >= (lastTime + self.timeout):  # Break connection if <timeout> since last message.
                break

            if dataType == b"obj":  # obj:<dirId>:<sesId>:<object>:end
                await self.receiveObject(data)  # Take the object from the client and put it somewhere.
                # print("server: got object")  # debug
            elif dataType == b"shift":  # shift:<objectId>:<shift>:<idx>:end
                await self.receiveShift(data)  # Give the shift to the specified object.
                lastTime = time.monotonic()  # Store time shift was received.
                # print("server: got shift")  # debug
            elif dataType == b"newConnection":  # newConnection:<cliId>:<address>:<port>:end
                cliId = await self.registerNewClient(data)  # Register a new client and return Id.
                asyncio.create_task(self.continuousSend(cliId, writer))  # Start a task to send object updates.
                # print("server: got connection")  # debug
            elif dataType == b"disconnect":  # disconnect::end
                # print("server: got disconnect")  # debug
                break

        await writer.drain()  # cleanup for disconnect.
        writer.write(b"disconnect::end")  # Send disconnect to client.
        await writer.drain()
        writer.write_eof()  # Close connection.
        writer.close()
        # print("server: disconnecting")  # debug
        await writer.wait_closed()

    async def receiveObject(self, data):
        """
        Take an object from the client and put it where specified.

        :param bytes data: <dirId>:<sesId>:<object>
        """
        data = data.split(b":")  # <dirId>:<sesId>:<object> -> [<dirId>, <sesId>, <object>]
        dirId = base64.b64decode(data[0]).decode()  # Decode directory Id.
        sesId = base64.b64decode(data[1]).decode()  # Decode session Id.
        obj = pickle.loads(base64.b64decode(data[2]))  # Decode object.
        for dirr in self.directoryList:  # Search for the right session in the specified directory.
            if dirr.tags["id"] == dirId:
                for ses in dirr.sessionList:
                    if ses.tags["id"] == sesId:
                        ses.addObject(obj)  # Put the object in the session.
                        return  # All done.

    async def receiveShift(self, data):
        """
        Take a shift from the client and pass it to it's networked object.

        :param bytes data: <objectId>:<shift>:<idx>
        """
        data = data.split(b":")  # <objectId>:<shift>:<idx> -> [<objectId>, <shift>, <idx>]
        objId = base64.b64decode(data[0]).decode()  # Decode the target object's id.
        shift = pickle.loads(base64.b64decode(data[1]))  # assuming shift is pickled b64-encoded Shift.
        idx = base64.b64decode(data[2]).decode()  # idx is either an int for insert or "append" to append.
        o = None
        for dirr in self.directoryList:  # Find the object by objId..
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
        if idx == "append":  # Handle if idx == "append"
            o.tasker.shifts.append(shift)  # Append shift to object tasker.
        else:
            try:
                o.tasker.shifts.insert(int(idx), shift)  # If not "append" convert str -> int and insert using idx
            except ValueError:  # If the idx cant be converted to int.
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
        Continuously send updates of the client's networked object to the client.

        Handles ConnectionResetError and RuntimeError by return.

        :param str cliId: Client Id
        :param StreamWriter writer: Writer to client.
        """
        cliObj = None
        while self.live and not writer.is_closing():  # Keep sending updates while alive and client is accessible.
            await asyncio.sleep(0)  # Pass so other stuff can work after an update is sent.
            if cliObj is None or ("networkObject" not in cliObj.tags.keys()) or cliObj.tags["networkObject"] != cliId:
                # acquire the networkObject if necessary.
                cliObj = None
                for dirr in self.directoryList:  # run though all directories and allow execution to move.
                    for ses in dirr.sessionList:  # run though all sessions in dirr and allow execution to move.
                        await asyncio.sleep(0)  # Pass execution because sessions can be large.
                        for obj in ses.objectList:  # run though all objects in ses but be blocking at this part.
                            if ("networkObject" in obj.tags.keys()) and obj.tags['networkObject'] == cliId:
                                cliObj = obj
                                break  # Exit loop on acquisition
                        if cliObj is not None:  # Exit loop on acquisition
                            break
                    if cliObj is not None:  # Exit loop on acquisition
                        break
            if cliObj is not None:  # If the search did not come back empty.
                objDt = base64.b64encode(pickle.dumps(cliObj))
                try:
                    writer.write(b"obj:" + objDt + b":end")  # Send it.
                    await writer.drain()
                except ConnectionResetError:
                    # print("client connection reset. ending...")  # debug
                    return
                except RuntimeError:
                    # print("writer from client closed. ending...")  # debug
                    return
