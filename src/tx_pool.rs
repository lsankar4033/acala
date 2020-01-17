use crate::chain_state::ChainState;

type Address = String;

// NOTE: signature omitted for now
pub struct Transaction {
    from: Address,
    to: Address,

    coin: u32,
    amount: u64,
    fee: u64,

    nonce: u32,
}

pub struct TxPool {
    txes: Vec<Transaction>,
}

// NOTE: I may generalize this in the future
#[derive(Debug, PartialEq)]
pub enum TxPoolInsertError {
    NoncePassed,
    NonceSkips,
    InsufficientBalance,
}

impl TxPool {
    pub fn insert(
        &self,
        tx: &Transaction,
        chain_state: &ChainState,
    ) -> Result<(), TxPoolInsertError> {
        self.check_valid_nonce(tx)?;
        self.check_sufficient_balance(tx, chain_state)?;

        // TODO: do insertion

        Ok(())
    }

    fn check_valid_nonce(&self, tx: &Transaction) -> Result<(), TxPoolInsertError> {
        Ok(())
    }

    fn check_sufficient_balance(
        &self,
        tx: &Transaction,
        chain_state: &ChainState,
    ) -> Result<(), TxPoolInsertError> {
        Ok(())
    }

    // TODO: filter based on coin too!
    fn relevant_txes(&self, address: &Address) -> Vec<&Transaction> {
        self.txes
            .iter()
            .filter(|tx| tx.from == *address || tx.to == *address)
            .map(|tx| tx.clone())
            .collect()
    }

    // TODO:
    // fn popBatch(size: u32) -> [Transaction] {
    //     []
    // }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn test_tx(nonce: u32) -> Transaction {
        let from = String::from("from");
        let to = String::from("to");
        let coin = 1;

        // NOTE: these don't matter in valid nonce tests, but will matter in balance tests
        let amount = 100;
        let fee = 10;

        Transaction {
            from,
            to,
            coin,
            amount,
            fee,
            nonce,
        }
    }

    #[test]
    fn check_valid_nonce() {
        let pool = TxPool {
            txes: (3..11).map(test_tx).collect(),
        };

        // NOTE: replacement behavior
        for nonce in 3..11 {
            assert_eq!(pool.check_valid_nonce(&test_tx(nonce)), Ok(()));
        }
        assert_eq!(pool.check_valid_nonce(&test_tx(11)), Ok(()));

        assert_eq!(
            pool.check_valid_nonce(&test_tx(2)),
            Err(TxPoolInsertError::NoncePassed)
        );
        assert_eq!(
            pool.check_valid_nonce(&test_tx(12)),
            Err(TxPoolInsertError::NonceSkips)
        )
    }

    #[test]
    fn check_sufficient_balance() {
        // TODO
    }
}
