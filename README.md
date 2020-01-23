# rollup-verifier
Sorta described here: https://hackmd.io/2_8sliT8RdWnnNlo24_HFA . In search of a better name!

## rough structure

ws { chain_state, tx_pool }
- submit_tx(tx) ->
  - chain_state.verify(tx)
  - eth.verify_sig(tx)
  - tx_pool.insert(tx)

tx_pool
- insert(tx)
- popBatch() -> Tx[]

chain_state { web3, accountToBalance, accountToNonce, slotToOperator, curSlot }
- reload()
  - need to make sure this is < 15s (block time)
- loop(freq)
- check_tx(tx) -> bool + reason?
- register_listener(listener)
  - method for informing caller that we're ready for batch
- ready_for_batch() -> bool
  - better name necessary

collector { chain_state, tx_pool, batch_builder_location}
- wait on chain_state.ready_for_batch, or use registered listener then
  - tx_pool.pop_batch()
  - send to batch_builder
