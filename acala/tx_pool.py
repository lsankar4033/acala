import asyncio

from collections import defaultdict, namedtuple

# TODO: add coin?
Tx = namedtuple('Tx', ['from_address', 'to_address', 'value', 'data', 'nonce'])

# TODO: add max pool size (ddos protection)
class TxPool():
    def __init__(self, tx_transiation_fn):
        self.lock = asyncio.Lock()
        self.from_address_to_txes = defaultdict(list)

        self.tx_transition_fn = tx_transition_fn

    # TODO: global ordering on txes?
    async def add_tx(self, tx: Tx):
        async with self.lock:
            existing_txes = self.from_address_to_txes[tx.from_address]

            # insert or replace.
            # NOTE: adds txes to pool with nonces that are greater than (1 + largest_existing_nonce).
            # Subsequent txes with nonces that fit in any gaps are added to the appropriate gap.
            # This method is assumed to be called after the nonce is checked with ChainState
            if tx.nonce > 0:
                replacement_idx = -1
                insertion_idx = -1
                for (i, existing_tx) in enumerate(existing_txes):
                    if existing_tx.nonce == tx.nonce:
                        replacement_idx = i
                        break
                    elif existing_tx.nonce > tx.nonce:
                        insertion_idx = i
                        break

                if insertion_idx != -1:
                    existing_txes.insert(insertion_idx, tx)
                elif replacement_idx != -1:
                    existing_txes[replacement_idx] = tx
                else:
                    existing_txes.append(tx)

    # NOTE: removes txes that are selected from the tx pool
    async def retrieve_batch(self, rollup_state):
        async with self.lock:
            pass
