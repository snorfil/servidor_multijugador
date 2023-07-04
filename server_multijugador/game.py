import asyncio
import json

from server_multijugador.comunication.dtos import createMensaje
from server_multijugador.comunication.states import STATE_GAME
from server_multijugador.wires import Wire


class Game(Wire):
    def __init__(self, players):
        self.players = players
        self.bind()
        self.duration = 5  # Duración de la partida en segundos
        self.dto = None

    def bind(self):
        for p in self.players:
            p.setWire(self)

    async def cancel(self, player):
        pass

    async def start(self):
        await self.__presentation()
        # await self.__countDown()
        # timer_task = asyncio.create_task(self.__game_timer())
        # await timer_task

    async def broadcast(self, msg):
        for player in self.players:
            await player.send_message(msg=msg)

    async def __broadcast_results(self):
        results = [player.get_info().to_dict() for player in self.players]
        results_message = json.dumps(results)
        await self.broadcast(msg=results_message)
        await self.__close_conexion()

    async def __close_conexion(self):
        for player in self.players:
            player.writer.close()
            await player.writer.wait_closed()

    async def __countDown(self):
        contador = 3

        while contador > 0:
            msg = createMensaje(STATE_GAME.READY,str(contador))
            await self.broadcast(msg=msg)
            contador -= 1
            await asyncio.sleep(1)  # Wait for 1 second between countdown numbers
        msg = createMensaje(STATE_GAME.START,'GO')
        await self.broadcast(msg=msg)
        for p in self.players:
            p.enablePulse()

    async def __game_timer(self):
        contador = 0
        while contador < self.duration:
            contador += 1
            await asyncio.sleep(1)
            msg = createMensaje(STATE_GAME.TIME, str(contador))
            await self.broadcast(msg)
        await self.__broadcast_results()

    async def pulse(self, msg):
        asyncio.create_task(self.broadcast(msg))

    async def __presentation(self):

        msg = ""
        for player in self.players:
            msg += f"{player.get_info()}"

        msg = createMensaje(STATE_GAME.PRESENTATION, msg)

        await self.broadcast(msg=msg)

    def endGame(self, id):

        self.__broadcast_results()


