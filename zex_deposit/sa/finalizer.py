import asyncio

from db.transfer import get_pending_transfers_block_number, to_finalized, to_reorg
from utils.web3 import (
    async_web3_factory,
    filter_blocks,
    get_block_tx_hash,
    get_finalized_block_number,
)
from .config import (
    BATCH_BLOCK_NUMBER_SIZE,
    CHAINS_CONFIG,
    MAX_DELAY_PER_BLOCK_BATCH,
    ChainConfig,
)


async def update_finalized_transfers(chain: ChainConfig):
    while True:
        w3 = await async_web3_factory(chain)
        finalized_block_number = await get_finalized_block_number(w3)
        pending_blocks_number = await get_pending_transfers_block_number(
            chain_id=chain.chain_id, finalized_block_number=finalized_block_number
        )

        if len(pending_blocks_number) == 0:
            print(
                f"No pending tx has been found. finalized_block_number: {finalized_block_number}"
            )
            await asyncio.sleep(MAX_DELAY_PER_BLOCK_BATCH)
            continue

        for i in range(len(pending_blocks_number)):
            blocks_to_check = pending_blocks_number[
                (i * BATCH_BLOCK_NUMBER_SIZE) : (i * (BATCH_BLOCK_NUMBER_SIZE + 1) + 1)
            ]
            results = await filter_blocks(
                w3,
                blocks_to_check,
                get_block_tx_hash,
                max_delay_per_block_batch=MAX_DELAY_PER_BLOCK_BATCH,
            )
            await to_finalized(chain.chain_id, finalized_block_number, results)
            await to_reorg(chain.chain_id, min(blocks_to_check), max(blocks_to_check))


if __name__ == "__main__":
    asyncio.run(update_finalized_transfers(CHAINS_CONFIG["11155111"]))
