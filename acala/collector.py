import asyncio

class Collector():
    def __init__(self, chain_state, tx_pool):
        self.chain_state = chain_state
        self.tx_pool = tx_pool
        self.period_secs = period_secs

    async def start(self, period_secs=15):
        while True:
            # TODO: check chain state for pos slot
            # TODO: if our slot, then get a batch from the tx pool and publish
            await asyncio.sleep(period_secs)
