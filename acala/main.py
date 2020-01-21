import asyncio

from fastapi import FastAPI

from acala.chain_state import ChainState, sync_chain_state
from acala.collector import Collector
from acala.tx_pool import TxPool

# NOTE: can change server based on what works for us
app = FastAPI()

chain_state = ChainState()
tx_pool = TxPool()

collector = Collector(chain_state, tx_pool)

# TODO: Remove!
@app.get('/')
async def test():
    return {'hello': 'world'}

# Run sync tasks
asyncio.gather(
    sync_chain_state(chain_state),
    collector.start()
)
