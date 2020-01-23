import asyncio

from fastapi import FastAPI

# TODO: specify env variable configuration in binary or distribution
from web3.auto import w3

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

# TODO: route for submitting a tx

# Run sync tasks
asyncio.gather(
    sync_chain_state(chain_state, w3),
    collector.start()
)
