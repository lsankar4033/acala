import pytest

from collections import defaultdict
from acala.tx_pool import Tx, TxPool


def build_tx(nonce, from_address='0x0', data='foo'):
    return Tx(from_address, '0x1', 1, data, nonce)


def check_tx_pool(tx_pool, expected_txes):
    from_to_last_nonce = defaultdict(lambda: -1)
    for tx in expected_txes:
        if tx.nonce > from_to_last_nonce[tx.from_address]:
            from_to_last_nonce[tx.from_address] = tx.nonce

    assert dict(tx_pool.from_address_to_last_nonce) == dict(from_to_last_nonce)
    assert tx_pool.txes == expected_txes


def test_init_tx_pool():
    tp = TxPool()

    assert dict(tp.from_address_to_last_nonce) == {}
    assert tp.txes == []


@pytest.mark.asyncio
class TestAddTx:
    async def test_fresh_append(self):
        tp = TxPool()
        await tp.add_tx(build_tx(3))

        check_tx_pool(tp, [build_tx(3)])

    async def test_append(self):
        tp = TxPool()
        txes = [build_tx(i) for i in range(3)]
        for tx in txes:
            await tp.add_tx(tx)

        check_tx_pool(tp, txes)

    async def test_replace(self):
        tp = TxPool()
        await tp.add_tx(build_tx(3))
        await tp.add_tx(build_tx(3, data='bar'))

        check_tx_pool(tp, [build_tx(3, data='bar')])

    async def test_multiple_from(self):
        tp = TxPool()
        await tp.add_tx(build_tx(1))
        await tp.add_tx(build_tx(1, from_address='0x1'))

        check_tx_pool(tp, [build_tx(1), build_tx(1, from_address='0x1')])

    async def test_skipped_nonce(self):
        tp = TxPool()
        await tp.add_tx(build_tx(1))

        with pytest.raises(ValueError):
            await tp.add_tx(build_tx(3))

    async def test_early_nonce(self):
        tp = TxPool()
        await tp.add_tx(build_tx(2))

        with pytest.raises(ValueError):
            await tp.add_tx(build_tx(1))

    async def test_max_size(self):
        tp = TxPool(max_size=2)
        await tp.add_tx(build_tx(1))
        await tp.add_tx(build_tx(2))

        # NOTE: should this be a ValueError?
        with pytest.raises(ValueError):
            await tp.add_tx(build_tx(3))
