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

    """

    def __init__(self, cliId, server, obj, port=6248, shifts=None, ses=None, tags=None):
        super().__init__()
        if tags is None:
            self.tags = {}
        else:
            self.tags = tags
        self.tags["id"] = cliId
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

        self.address = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.live = True

    def __str__(self):
        if self.live:
            isAlive = "Alive"
        else:
            isAlive = "Dead"
        return "{}:{}:{}:".format(self.tags["id"], self.obj, self.server, isAlive)

    def run(self):
        asyncio.run(self.main())


    async def main(self):
        try:
            await asyncio.gather(self.connectToServer(), self.taskManager())
        except asyncio.CancelledError:
            print("Tasks canceled. Live: {}".format(self.live))  # debug

    async def taskManager(self):
        while self.live:
            await asyncio.sleep(0)
        tasks = asyncio.all_tasks()
        for task in tasks:
            try:
                task.cancel()
            except asyncio.CancelledError:
                pass

    async def connectToServer(self):
        """
        """
        connected = False
        while not connected:
            try:
                reader, writer = await asyncio.open_connection(host=self.server[0], port=self.server[1])
                connected = True
                print("client connected")  # debug
            except ConnectionRefusedError:
                print("connect refused. ending...")  # debug
                await asyncio.sleep(0)
        cliId = base64.b64encode(self.tags["id"].encode())
        address = base64.b64encode(self.address.encode())
        port = base64.b64encode(str(self.port).encode())
        connectB = b"newConnection:" + cliId + b":" + address + b":" + port + b":end"

        dirId = base64.b64encode(self.obj[0].encode())
        sesId = base64.b64encode(self.obj[1].encode())
        obj = base64.b64encode(pickle.dumps(self.obj[2]))
        objB = b"obj:" + dirId + b":" + sesId + b":" + obj + b":end"

        fullB = connectB + objB
        writer.write(fullB)
        print("client: registration sent")  # debug
        try:
            await writer.drain()
        except ConnectionResetError:
            print("connection reset. ending...")  # debug
            return
        await asyncio.gather(self.sendShifts(writer), self.handleServer(reader, writer))

    async def sendShifts(self, writer):
        while self.live and not writer.is_closing():  # Exit on cli death or writer close.
            if self.shiftQueue:  # Only try to send a shift if there are any to send.
                shift, idx = self.shiftQueue.pop()
                shiftDt = base64.b64encode(pickle.dumps(shift))
                idxDt = base64.b64encode(str(idx).encode())
                objIdDt = base64.b64encode(self.obj[2].tags["id"].encode())
                writer.write(b"shift:" + objIdDt + b":" + shiftDt + b":" + idxDt + b":end")
                try:
                    await writer.drain()
                except ConnectionResetError:
                    print("server connection reset. ending...")  # debug
                    return
            else:
                await asyncio.sleep(0)

    async def handleServer(self, reader, writer):
        connected = True
        lastTime = time.monotonic()
        while connected:
            try:
                dataType = (await reader.readuntil(b":"))[:-1]  # Separate data type header.
                data = (await reader.readuntil(b":end"))[:-4]  # Remove footer.
            except asyncio.IncompleteReadError:
                print("Server Disconnected Unexpectedly")  # debug
                return
            except ConnectionResetError:
                print("Server Disconnected Unexpectedly")  # debug
                return

            if time.monotonic() >= (lastTime + (60 * 5)):  # DC for timeout
                break

            if dataType == b"obj":  # obj:<object>:end
                await self.receiveObject(data)
                lastTime = time.monotonic()  # Store time object was received.
                print("client: got obj update")  # debug
            elif dataType == b"disconnect":  # disconnect::end
                print("client: got disconnect")  # debug
                break

        await writer.drain()  # cleanup for disconnect.
        writer.write(b"disconnect::end")
        await writer.drain()
        writer.write_eof()
        writer.close()
        print("client: disconnecting")  # debug
        await writer.wait_closed()

    async def receiveObject(self, data):
        """
        Update self.obj with the object received from the server encoded in <data>.

        :param bytes data:
        """
        obj = pickle.loads(base64.b64decode(data))
        self.obj[2] = obj
        # await self.display_update()  # At some point...

    def enqueueShift(self, shift, idx):
        self.shiftQueue.append((shift, idx))
