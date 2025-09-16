import asyncio
from solana.rpc.async_api import AsyncClient
from src.transactions import full_create_transaction, CreateTxParams
from src import utils
from src.config import Config

tx_queue = asyncio.Queue()

async def main_task(client: AsyncClient, config: Config):
    signers = utils.load_signers(config.signers)
    metadata = utils.load_metadata(config.metadata)
    metadata_mapping = utils.create_metadata_mapping(metadata, signers)
    min_len = len(metadata_mapping[list(metadata_mapping.keys())[-1]])
    i = 0
    last = False
    while True:
        for signer, metadata in metadata_mapping.items():
            print(f"Processing signer: {signer.pubkey()}")
            if len(metadata) > min_len and last:
                token_metadata = metadata[-1]
            elif len(metadata) == min_len and last:
                last = False
                token_metadata = metadata[i]
            else:
                token_metadata = metadata[i]
            print(f"Processing token: {token_metadata['name']}")
            params = CreateTxParams(
                    unit_limit=250_123,
                    unit_price=config.unit_price,
                    token_name=token_metadata['name'],
                    token_symbol=token_metadata['symbol'],
                    token_uri=token_metadata['uri'],
                    buy_amount_sol=config.buy_amount_sol
                )
            tx = await full_create_transaction(client, signer, params)
            response = await client.send_transaction(tx)
            tx_hash = response.value
            print(f"Transaction sent: {tx_hash}")
            await tx_queue.put(tx_hash)
        i += 1
        if i >= min_len:
            i = 0
            last = True
        await asyncio.sleep(config.sleep_time * 60)


async def listen_for_transactions_task(client: AsyncClient):
    while True:
        try:
            tx_hash = await tx_queue.get()
            result = await client.confirm_transaction(tx_hash, commitment='confirmed')
            for res in result.value:
                if res is None:
                    continue
                if res.err:
                    print(f"Transaction {tx_hash} failed with error: {res.err}")
                else:
                    print(f"Transaction {tx_hash} finished")
            tx_queue.task_done()
        except Exception as e:
            print(f"Listener error: {e}")

async def main():
    config = utils.load_config("config.yaml")
    client = AsyncClient(config.rpc_url)

    try:
        await asyncio.gather(main_task(client, config), listen_for_transactions_task(client))
    except KeyboardInterrupt:
        print("\nCTRL+C signal received. Exiting...")
    finally:
        await client.close()

if __name__ == "__main__":
    print(utils.get_startup_logo())
    # asyncio.run(main())
