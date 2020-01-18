import asyncio

class TxPool():

    def __init__(self):
        self.lock = asyncio.Lock()

    async def add_tx(self, tx):
        async with self.lock:
            pass

    async def retrieve_valid_batch(self, chain_state):
        async with self.lock:
            pass
