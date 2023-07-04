import asyncio
import json

from server_multijugador.comunication.dtos import ComunicationDTO, createMensaje
from server_multijugador.comunication.msg import Mensaje
from server_multijugador.comunication.states import STATE_GAME
from server_multijugador.wires import Wire
from server_multijugador.game_manager import PlayerProvider, GameManager


class GestorCola(PlayerProvider, Wire):
    limit = 1

    def __init__(self):
        self.me = self
        self.gamesManager = GameManager(self)
        self.players = list()
        self.semafore = asyncio.Semaphore(1)

    async def getMatchPlayers(self):
        pls = list()
        for i in range(self.limit):
            pls.append(self.players.pop())
        return pls

    async def add_player(self, player):
        async with self.semafore:
            player.setWire(self.me)

            msg = createMensaje(state=STATE_GAME.WAIT, msg=Mensaje.WAIT)
            await player.send_message(msg=msg)

            asyncio.create_task(player.handle_input())
            self.players.append(player)

            if len(self.players) >= self.limit:
                await self.gamesManager.gotPlayers()

    async def cancel(self, player):
        player.disable()
        self.players.remove(player)
