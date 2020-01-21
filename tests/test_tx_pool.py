import pytest

from acala.tx_pool import Tx, TxPool

def build_tx(nonce, from_address = '0x0', data='foo'):
    return Tx(from_address, '0x1', 1, data, nonce)

def test_init_tx_pool():
    tp = TxPool()
    assert dict(tp.from_address_to_txes) == {}

class TestAddTx:
    @pytest.mark.asyncio
    async def test_append_tx(self):
        tp = TxPool()

        await tp.add_tx(build_tx(3))
        assert dict(tp.from_address_to_txes) == {'0x0': [build_tx(3)]}

        await tp.add_tx(build_tx(4))
        assert dict(tp.from_address_to_txes) == {'0x0': [build_tx(3), build_tx(4)]}

        await tp.add_tx(build_tx(2, from_address='0x2'))
        assert dict(tp.from_address_to_txes) == {'0x0': [build_tx(3), build_tx(4)],
                                                 '0x2': [build_tx(2, from_address='0x2')]}

    @pytest.mark.asyncio
    async def test_insert_tx(self):
        tp = TxPool()
        await tp.add_tx(build_tx(3))
        await tp.add_tx(build_tx(2))
        await tp.add_tx(build_tx(6))
        await tp.add_tx(build_tx(4))

        assert dict(tp.from_address_to_txes) == {'0x0': [build_tx(2), build_tx(3), build_tx(4), build_tx(6)]}

    @pytest.mark.asyncio
    async def test_replace_tx(self):
        tp = TxPool()
        await tp.add_tx(build_tx(3))
        await tp.add_tx(build_tx(3, data='bar'))

        assert dict(tp.from_address_to_txes) == {'0x0': [build_tx(3, data='bar')]}
