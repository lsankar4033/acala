import asyncio

from collections import defaultdict, namedtuple

# TODO: add coin?
Tx = namedtuple('Tx', ['from_address', 'to_address', 'value', 'data', 'nonce'])

class TxPool():
    def __init__(self):
        self.lock = asyncio.Lock()
        self.from_address_to_txes = defaultdict(list)

    async def add_tx(self, tx: Tx):
        async with self.lock:
            existing_txes = self.from_address_to_txes[tx.from_address]
            if len(existing_txes) == 0:
                existing_txes.append(tx)

            elif tx.nonce == existing_txes[-1].nonce + 1:
                existing_txes.append(tx)

            elif any((tx.nonce == cmp_tx.nonce for cmp_tx in existing_txes)):
                # TODO: replacement
                pass

            else:
                # TODO: error!
                pass
            # if list empty, add tx
            # elif 1 greater than last one in list, add it
            # elif equal to any in list, replace old
            # else

    async def retrieve_valid_batch(self, chain_state):
        async with self.lock:
            pass
