import asyncio
from asyncio import sleep

from server_multijugador.comunication.dtos import PlayerDTO
from server_multijugador.comunication.states import STATE_GAME
from server_multijugador.cliente.connection import Connection

player_dto = PlayerDTO(0, 'cliente_bot', 0, 0, 0)


async def listen_server(player):
    while True:
        try:
            msg = await player.receive_message()
            print(msg)

            if msg == '':
                player.active = False
                break

            if msg['state'] == STATE_GAME.READY.name:
                print(msg)
            elif msg['state'] == STATE_GAME.JOIN.name:
                print(msg)
            elif msg['state'] == STATE_GAME.PLAY.name:
                print(msg)
            elif msg['state'] == STATE_GAME.PRESENTATION.name:
                print(msg)
            elif msg['state'] == STATE_GAME.START.name:
                print(msg)
            elif msg['state'] == STATE_GAME.TIME.name:
                print(msg)
            elif msg['state'] == STATE_GAME.END.name:
                print(msg)
                player.active = False
                break
            # await player.send_message('te envio esto')


        except ConnectionAbortedError:
            break
        except ConnectionResetError:
            break


async def correr_automatico(player):
    while True:
        await sleep(15)
        msg = player_dto.to_dict()
        await player.send_message(msg)


async def play_game():
    # Connect to the server

    player = Connection()

    await player.conectar()
    await player.send_message(f'{player_dto.name}')
    asyncio.create_task(listen_server(player))
    # asyncio.create_task(correr_automatico(player))


# threading.Thread(target=escuchar_entrada).start()
asyncio.run(play_game())