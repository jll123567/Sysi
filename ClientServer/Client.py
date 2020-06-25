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
        self.server = server  # (address, port)
        self.obj = obj  # (dir, ses, obj)
        self.shiftQueue = shifts
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

    async def handleServerRequests(self, reader):
        pass  # TODO: Make me work lol.

    async def sendShifts(self, writer):
        while self.live:
            if self.shiftQueue:  # Only try to send a shift if there are any to send.
                shift, idx = self.shiftQueue.pop()
                shiftDt = base64.b64encode(pickle.dumps(shift))
                idxDt = base64.b64encode(str(idx).encode())
                objIdDt = base64.b64encode(self.obj.tags["id"].encode())
                writer.write(b"shift:" + objIdDt + b":" + shiftDt + b":" + idxDt + b":end")
                try:
                    await writer.drain()
                except ConnectionResetError:
                    # print("connection reset. ending...")  # debug
                    return
                writer.close()
                await writer.wait_closed()
            else:
                await asyncio.sleep(0)

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
        try:
            reader, writer = await asyncio.open_connection(self.server[0], self.server[1])
        except ConnectionRefusedError:
            # print("connect refused. ending...")  # debug
            return
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
        try:
            await writer.drain()
        except ConnectionResetError:
            # print("connection reset. ending...")  # debug
            return
        await asyncio.gather(self.sendShifts(writer), self.handleServerRequests(reader))
