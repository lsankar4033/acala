use std::collections::HashMap;

use crate::chain_state::ChainState;

type Address = String;

// TODO: Make sure types are what we expect
struct Transaction {
    from: Address,
    to: Address,

    coin: u32,
    amount: u64,
    fee: u64,

    nonce: u32,
    signature: String,
}

// TODO: concurrency necessary? depends on implementation of webserver threads
// TODO: might want other aggregate structures to improve performance
pub struct TxPool {
    txes: Vec<Transaction>,
}

impl TxPool {
    pub fn insert(&self, tx: Transaction, chain_state: ChainState) -> Result<Transaction, String> {
        // TODO: Put in verification + add logic:
        // 1. if nonce < all existing nonces, fail
        // 2. elsif nonce > 1 + last nonce, fail
        // 3. elsif nonce == nonce already in there, pass through balance check and replace if it passes
        // 4. elsif balance issue, fail (w/ message about conflict!)
        // 5. else, add tx

        Ok(tx)
    }

    // TODO:
    fn relevant_txes(&self, address: Address) -> Vec<Transaction> {
        self.txes
    }

    // TODO:
    // fn popBatch(size: u32) -> [Transaction] {
    //     []
    // }
}
