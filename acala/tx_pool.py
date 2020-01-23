import asyncio

from collections import defaultdict, namedtuple

# TODO: add coin?
Tx = namedtuple('Tx', ['from_address', 'to_address', 'value', 'data', 'nonce'])

# TODO: add max pool size (ddos protection)


class TxPool():
    def __init__(self, tx_transition_fn=None):
        self.lock = asyncio.Lock()

        self.from_address_to_last_nonce = defaultdict(lambda: -1)
        self.txes = []

        self.tx_transition_fn = tx_transition_fn

    # NOTE: only replace or append allowed. no 'insertion'
    async def add_tx(self, tx: Tx):
        async with self.lock:
            last_nonce = self.from_address_to_last_nonce[tx.from_address]
            if last_nonce is -1 or tx.nonce == last_nonce + 1:
                self.txes.append(tx)
                self.from_address_to_last_nonce[tx.from_address] = tx.nonce

            elif tx.nonce > last_nonce + 1:
                raise ValueError(
                    f"Nonce {tx.nonce} is too much larger than previous nonce {last_nonce}")

            else:
                matching_indices = [i for (i, existing_tx) in enumerate(self.txes) if
                                    existing_tx.nonce is tx.nonce and
                                    existing_tx.from_address is tx.from_address]

                if len(matching_indices) is 0:
                    raise ValueError(
                        f"Nonce {tx.nonce} is less than all nonces in tx pool for the same sender")

                self.txes[matching_indices[0]] = tx

    # NOTE: removes txes that are selected from the tx pool
    # resets internal state as necessary
    async def retrieve_batch(self, rollup_state):
        async with self.lock:
            pass
