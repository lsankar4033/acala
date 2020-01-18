import asyncio

class ChainState():
    def __init__(self):
        self.lock = asyncio.Lock()

    async def update_state(self):
        async with self.lock:
            pass

async def sync_chain_state(chain_state, period_secs=15):
    while True:
        # TODO: Do sync stuff
        await asyncio.sleep(period_secs)
