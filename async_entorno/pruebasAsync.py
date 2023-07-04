from asyncio import sleep, Semaphore
import functools
import asyncio as asyncio
import threading

numero = 0

class Leandro:
    def __init__(self, loop1, loop2, loop3):
        self.l1 = loop1
        self.l2 = loop2
        self.l3 = loop3
        self.yo = self
        self.semaphore = Semaphore(value=1)

    async def produce(self, padre, name):
        global numero
        numero = 0
        while numero < 30:
            await sleep(1)
            async with self.semaphore:
                numero += 2
                print(f'produce {numero} {name}')
        await padre.produje()

    def produje(self):
        fun = functools.partial(self.produce, self.yo, 'productor')
        asyncio.run_coroutine_threadsafe(fun(), self.l1)

    async def consume(self, padre, name):
        global numero
        while numero < 30:
            await sleep(1)
            async with self.semaphore:
                numero -= 1
                print(f'consume {name} {numero}')
        await padre.comi()

    def comi(self):
        fun = functools.partial(self.consume, self.yo, 'consumidor')
        asyncio.run_coroutine_threadsafe(fun(), self.l2)

    def start(self):
        self.produje()
        self.comi()
        

def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop1 = asyncio.new_event_loop()
thread1 = threading.Thread(target=run_loop, args=(loop1,))
thread1.start()

loop2 = asyncio.new_event_loop()
thread2 = threading.Thread(target=run_loop, args=(loop2,))
thread2.start()

loop3 = asyncio.new_event_loop()
thread3 = threading.Thread(target=run_loop, args=(loop3,))
thread3.start()

leandro = Leandro(loop1, loop2, loop3)

leandro.start()