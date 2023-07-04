import random

import asyncio
from asyncio import sleep

numero = 0
async def tareaproductora():
    global numero
    while True:

        numero +=  1
        await sleep(0.5)
        print('produciendo')

async def tareaConsumidor(tiempo):
    global numero
    await sleep(tiempo)
    numero -= 1
    print('consumiendo' + str(numero))
    time = numero_aleatorio = random.randint(1, 2)
    for i in range(2):
        asyncio.create_task(tareaConsumidor(time))

async def main():
    await asyncio.gather(tareaproductora(), tareaConsumidor(2))

asyncio.run(main())