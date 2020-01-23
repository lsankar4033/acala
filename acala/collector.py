import asyncio

# TODO: configure somewhere else
import os
operator_address = os.environ['OPERATOR_ADDRESS']

class Collector():
    def __init__(self, chain_state, tx_pool):
        self.chain_state = chain_state
        self.tx_pool = tx_pool

    async def start(self, period_secs=15):
        while True:
            chain_state = await self.chain_state.get_state()

            # TODO: make sure that both are checksummed version?
            if chain_state['slot_owner'] is operator_address:
                tx_batch = await self.tx_pool.retrieve_batch(rollup_state)
                # TODO: submit to queue or use callback!

            await asyncio.sleep(period_secs)
