"""
The Client

Classes
    Client
"""
import threading
import sysObjects.Tagable
import asyncio
import base64
import pickle
import socket
import time


class SysClient(threading.Thread, sysObjects.Tagable.Tagable):
    """
    A client the handles communication between this device and a server. Represents a single networked object that is
        on the server and shown to this device.

    :param str cliId: The client's Id.
    :param tuple server: An address, port pair for the server.
    :param list obj: An object to send to the server and get updates to. List is directoryId, sessionId, object.
    :param int port: The client's port, defaults to 6248.
    :param list shifts: A queue of shifts to send to the networked object, defaults to an empty list.
    :param list ses: A list of local sessions. Use these however.
    :param dict tags: Tags like Tagable.
    """

    def __init__(self, cliId, server, obj, port=6248, shifts=None, ses=None, tags=None):
        """Constructor"""
        super().__init__()  # Get thread stuff(super() points to parent 0).
        if tags is None:  # Manually add tags cuz super won't.
            self.tags = {}
        else:
            self.tags = tags
        self.tags["id"] = cliId  # Set id.
        if ses is None:
            self.sessionList = []
        else:
            self.directoryList = ses
        if shifts is None:
            self.shiftQueue = []
        else:
            self.shiftQueue = shifts
        self.server = server  # (address, port)
        self.obj = obj  # [dir, ses, obj]

        self.address = socket.gethostbyname(socket.gethostname())  # Own address.
        self.port = port
        self.live = True  # When false, client is kill.

    def __str__(self):
        if self.live:
            isAlive = "Alive"
        else:
            isAlive = "Dead"
        return "{}:{}:{}:".format(self.tags["id"], self.obj, self.server, isAlive)

    def run(self):
        """Code to run at thread start. Call with self.start()"""
        asyncio.run(self.main())

    async def main(self):
        """
        Start the tasks to connect to server and handle task canceling on thread death.

        Handles CancelledError.
        """
        try:
            await asyncio.gather(self.connectToServer(), self.taskManager())
        except asyncio.CancelledError:  # Do this when canceled.
            pass
            # print("Tasks canceled. Live: {}".format(self.live))  # debug

    async def taskManager(self):
        """
        Cancel all running tasks when self.live is false and handle Cancelled Errors.

        Handles CancelledError.
        """
        while self.live:
            await asyncio.sleep(0)  # Pass execution if the thread is still live.
        tasks = asyncio.all_tasks()  # Get all running tasks.
        for task in tasks:
            try:
                task.cancel()  # Tasks...canceled!
            except asyncio.CancelledError:  # Ignore the CancelledErrors.
                pass

    async def connectToServer(self):
        """
        Start a connection to the server, send the newConnection and obj message, then start the sendShift and
            handleServer tasks.

        Handles ConnectionRefusedError and ConnectionResetError.
        """
        connected = False
        while not connected:  # Keep trying to connect until it works.
            try:
                reader, writer = await asyncio.open_connection(host=self.server[0], port=self.server[1])
                connected = True
                # print("client connected")  # debug
            except ConnectionRefusedError:
                # print("connect refused. ending...")  # debug
                await asyncio.sleep(0)  # pass to task manager before trying again.

        cliId = base64.b64encode(self.tags["id"].encode())  # Encode the client id.
        address = base64.b64encode(self.address.encode())  # Encode this address.
        port = base64.b64encode(str(self.port).encode())  # Encode this port.
        connectB = b"newConnection:" + cliId + b":" + address + b":" + port + b":end"  # Structure message.

        dirId = base64.b64encode(self.obj[0].encode())  # Encode target directory id.
        sesId = base64.b64encode(self.obj[1].encode())  # Encode target session id.
        obj = base64.b64encode(pickle.dumps(self.obj[2]))  # Encode this object.
        objB = b"obj:" + dirId + b":" + sesId + b":" + obj + b":end"  # Structure message.

        fullB = connectB + objB  # Put all messages together.
        writer.write(fullB)  # Write the messages to the writer.
        # print("client: registration sent")  # debug
        try:
            await writer.drain()  # Wait for the writer to send the data.
        except ConnectionResetError:  # Handle the connection dying.
            # print("connection reset. ending...")  # debug
            return
        await asyncio.gather(self.sendShifts(writer), self.handleServer(reader, writer))  # Start sendShifts and ...
        # handleServer tasks with the reader and writer.

    async def sendShifts(self, writer):
        """
        Send shifts in the shift queue to the networked object on the server.

        Handles ConnectionResetError by return.

        :param StreamWriter writer: Writer to send to the server.
        """
        while self.live and not writer.is_closing():  # Exit on cli death or writer close.
            if self.shiftQueue:  # Only try to send a shift if there are any to send.
                shift, idx = self.shiftQueue.pop()  # Get the shift and the index to put it at.
                shiftDt = base64.b64encode(pickle.dumps(shift))  # Encode the shift.
                idxDt = base64.b64encode(str(idx).encode())  # Encode the index.
                objIdDt = base64.b64encode(self.obj[2].tags["id"].encode())  # Encode the id of the networked object.
                writer.write(b"shift:" + objIdDt + b":" + shiftDt + b":" + idxDt + b":end")  # Write to writer the
                # message.
                try:
                    await writer.drain()  # Send to server.
                except ConnectionResetError:  # Die on disconnect.
                    # print("server connection reset. ending...")  # debug
                    return
            else:
                await asyncio.sleep(0)  # Pass execution after sending the shift.

    async def handleServer(self, reader, writer):
        """
        Handle messages from the server.

        Handles IncompleteReadError and ConnectionResetError by return.

        :param StreamWriter reader: Reader to receive from the server.
        :param StreamWriter writer: Writer to send to the server.
        """
        connected = True
        lastTime = time.monotonic()  # Store the time.
        while connected:
            try:
                dataType = (await reader.readuntil(b":"))[:-1]  # Separate data type header.
                data = (await reader.readuntil(b":end"))[:-4]  # Remove footer.
            except asyncio.IncompleteReadError:
                # print("Server Disconnected Unexpectedly")  # debug
                return
            except ConnectionResetError:
                # print("Server Disconnected Unexpectedly")  # debug
                return

            if time.monotonic() >= (lastTime + (60 * 5)):  # Break connection if 5 minutes since last message.
                break

            if dataType == b"obj":  # obj:<object>:end
                await self.receiveObject(data)  # take the object update message and process it.
                lastTime = time.monotonic()  # Store time object update was received.
                # print("client: got obj update")  # debug
            elif dataType == b"disconnect":  # disconnect::end
                # print("client: got disconnect")  # debug
                break  # Disconnect from server.

        await writer.drain()  # Cleanup for disconnect.
        writer.write(b"disconnect::end")  # Send disconnect to server.
        await writer.drain()
        writer.write_eof()  # Close writer.
        writer.close()
        # print("client: disconnecting")  # debug
        await writer.wait_closed()

    async def receiveObject(self, data):
        """
        Update self.obj with the object received from the server encoded in <data>.

        :param bytes data:
        """
        obj = pickle.loads(base64.b64decode(data))  # Decode the object.
        self.obj[2] = obj  # Update the object.
        # await self.display_update()  # At some point...

    def enqueueShift(self, shift, idx):
        """
        Add a shift to the shiftQueue.

        Idx can be either an integer or the string "append".

        :param Shift shift: The shift to add.
        :param idx: The index where the shift will pe placed.
        :type idx: int, str
        """
        self.shiftQueue.append((shift, idx))
