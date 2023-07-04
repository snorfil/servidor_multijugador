import asyncio
import json
from asyncio import StreamWriter, StreamReader

from server_multijugador.comunication.dtos import PlayerDTO
from server_multijugador.wires import Wire


class Player:
    def __init__(self, name, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer

        self.info: PlayerDTO = PlayerDTO(identificacion=-1,
                                         velocidad=0,
                                         posicion=0,
                                         puesto=0,
                                         name=name)

        self.canRead = False
        self.interruptor = True
        self.semafore = asyncio.Semaphore(1)
        self.wire: Wire = None
        self.me = self

    def setWire(self, wire: Wire):
        self.wire = wire

    def setId(self, id):
        self.info.id = id

    async def send_message(self, msg):
        self.writer.write(msg.encode())
        await self.writer.drain()

    def get_info(self):
        return self.info.to_dict()

    async def handle_input(self):

        while self.interruptor:
            data = await self.reader.read(1024)
            data = data.decode().strip()
            if data == '':
                self.interruptor = False
            print(str(data))

    def disable(self):
        self.canRead = False
        self.interruptor = False
        self.writer.close()

    def enablePulse(self):
        self.canRead = True
