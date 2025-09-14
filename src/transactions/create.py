from pydantic import BaseModel
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.solders import VersionedTransaction
from solders.message import MessageV0
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from spl.token.instructions import create_idempotent_associated_token_account, get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID

from src.instructions import create_instruction, extend_account_instruction, buy_instruction
from src import utils

class CreateTxParams(BaseModel):
    unit_limit: int
    unit_price: int
    token_name: str
    token_symbol: str
    token_uri: str
    buy_amount_sol: float



async def full_create_transaction(client: AsyncClient, signer: Keypair, params: CreateTxParams) -> VersionedTransaction:
    mint_keypair = Keypair()

    compute_limit_instruction = set_compute_unit_limit(params.unit_limit)
    compute_unit_price_instruction = set_compute_unit_price(params.unit_price) # 50_000
    create = create_instruction(mint_keypair.pubkey(), params.token_name, params.token_symbol, params.token_uri, signer.pubkey())
    bonding_curve = utils.get_bonding_curve(mint_keypair.pubkey())
    extend_account = extend_account_instruction(bonding_curve, signer.pubkey())
    create_idempotent_account = create_idempotent_associated_token_account(signer.pubkey(), signer.pubkey(), mint_keypair.pubkey(), TOKEN_PROGRAM_ID)
    associated_token_address = get_associated_token_address(signer.pubkey(), mint_keypair.pubkey(), TOKEN_PROGRAM_ID)
    buy = buy_instruction(mint_keypair.pubkey(), associated_token_address, signer.pubkey(), signer.pubkey(), 10, int(params.buy_amount_sol * 1_000_000_000), None)
    recent_blockhash = (await client.get_latest_blockhash()).value.blockhash
    # msg = MessageV0.try_compile(
    #     payer=signer.pubkey(),
    #     instructions=[compute_limit_instruction, compute_unit_price_instruction, create, extend_account, create_idempotent_account, buy],
    #     address_lookup_table_accounts=[],
    #     recent_blockhash=recent_blockhash,
    # )
    msg = MessageV0.try_compile(
        payer=signer.pubkey(),
        instructions=[create_idempotent_account],
        address_lookup_table_accounts=[],
        recent_blockhash=recent_blockhash,
    )
    return VersionedTransaction(msg, [signer])
