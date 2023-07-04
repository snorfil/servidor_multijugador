import asyncio
import json

from server_multijugador.comunication.states import STATE_GAME
from server_multijugador.comunication.dtos import ComunicationDTO, createMensaje
from server_multijugador.comunication.msg import Mensaje
from server_multijugador.game import Game


class PlayerProvider:
    async def getMatchPlayers(self) -> list:
        pass


class GameManager:
    def __init__(self, provider: PlayerProvider):
        self.proveedor = provider
        self.games = list()

    async def gotPlayers(self):
        players: list = await self.proveedor.getMatchPlayers()
        count = 1

        for p in players:
            p.setId(count)
            count += 1

            msg = createMensaje(STATE_GAME.JOIN, Mensaje.JOIN)

            await p.send_message(msg=msg)

        game = Game(players)
        self.games.append(game)
        asyncio.create_task(game.start())
