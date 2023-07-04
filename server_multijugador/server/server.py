import asyncio
from asyncio import StreamWriter, StreamReader

from server_multijugador.player_proxy import Player
from server_multijugador.player_manager import GestorCola


class Server:
    def __init__(self):
        self.player_manager = GestorCola()

    async def handle_client(self, reader:StreamReader, writer:StreamWriter):
        # Registrar nuevo jugador
        player_name = await reader.read(1024)
        print(player_name)
        player_name = player_name.decode().strip()
        player = Player(player_name, reader, writer)
        asyncio.create_task(self.player_manager.add_player(player))

    async def main(self):
        server = await asyncio.start_server(self.handle_client, '127.0.0.1', 5666)

        print('Servidor iniciado en', server.sockets[0].getsockname())

        async with server:
            await server.serve_forever()


game_server = Server()
asyncio.run(game_server.main())
