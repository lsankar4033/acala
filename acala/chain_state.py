import asyncio

# TODO: provide specific versions of provided functions for use by iden3 (and maybe OR?)
class ChainState():
    def __init__(self, rollup_slot_fn, rollup_state_fn):
        self.lock = asyncio.Lock()

        self.rollup_slot_fn = rollup_slot_fn
        self.rollup_state_fn = rollup_state_fn

        self.slot_owner = ''
        self.rollup_state = {}

    async def update_state(self, web3):
        async with self.lock:
            self.slot_owner = await self.rollup_slot_fn(web3)
            self.rollup_state = await self.rollup_state_fn(web3)

    async def get_state(self):
        async with self.lock:
            return {
                'slot_owner': slot_owner,
                'rollup_state': rollup_state
            }

async def sync_chain_state(chain_state, web3, period_secs=15):
    while True:
        await update_state(web3)
        await asyncio.sleep(period_secs)
