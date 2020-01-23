import asyncio

from collections import defaultdict, namedtuple

# TODO: add coin?
Tx = namedtuple('Tx', ['from_address', 'to_address', 'value', 'data', 'nonce'])


class TxPool():
    def __init__(self, tx_transition_fn=None, max_size=1000):
        self.lock = asyncio.Lock()

        self.from_address_to_last_nonce = defaultdict(lambda: -1)
        self.txes = []

        self.tx_transition_fn = tx_transition_fn
        self.max_size = max_size

    # NOTE: only replace or append allowed. no 'insertion'
    async def add_tx(self, tx: Tx):
        async with self.lock:

            if self.max_size is not None and len(self.txes) >= self.max_size:
                raise ValueError(
                    f"Can't add more txes: max size {self.max_size} has been reached")

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
