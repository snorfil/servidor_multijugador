import asyncio
import socket
import json


class Connection:
    def __init__(self):
        self.active = True
        self.w = None
        self.r = None

    async def conectar(self):
        self.r, self.w = await asyncio.open_connection('127.0.0.1', 5666)

    def transformar(self, data):
        return json.loads(data)

    async def send_message(self, message):
        self.w.write(message.encode())
        await self.w.drain()

    async def receive_message(self):
        data = await self.r.read(1024)
        msg = data.decode()

        if data == '':
            return ''
        try:
            msg = self.transformar(data)
        except Exception:
            print(msg)
        return msg

    def activate(self):
        self.active = True

    def close(self):
        self.w.close()
        self.r.close()
