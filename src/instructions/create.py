from solders.instruction import Instruction, AccountMeta
from solders.pubkey import Pubkey
from solders.system_program import ID as SYSTEM_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID

from src import constants, utils

DISCRIMINATOR = bytes([24, 30, 200, 40, 5, 28, 7, 119])

def create_instruction(mint: Pubkey, name: str, symbol: str, uri: str, user: Pubkey) -> Instruction:
    instruction_data = create_instruction_data(name, symbol, uri, user)
    accounts = create_instruction_accounts(mint, user)
    return Instruction(
        program_id=constants.PUMPFUN_PROGRAM_ID,
        data=instruction_data,
        accounts=accounts
    )

def create_instruction_data(name: str, symbol: str, uri: str, user: Pubkey) -> bytes:
    instruction_data = DISCRIMINATOR
    instruction_data += len(name).to_bytes(4, byteorder='little') + name.encode("utf-8")
    instruction_data += len(symbol).to_bytes(4, byteorder='little') + symbol.encode("utf-8")
    instruction_data += len(uri).to_bytes(4, byteorder='little') + uri.encode("utf-8")
    instruction_data += bytes(user)
    return instruction_data

def create_instruction_accounts(mint: Pubkey, user: Pubkey) -> list[AccountMeta]:
    pda = create_instruction_pda(mint)
    return [
        AccountMeta(mint, is_signer=True, is_writable=True),
        AccountMeta(pda["mint_authority"], is_signer=False, is_writable=False),
        AccountMeta(pda["bonding_curve"], is_signer=False, is_writable=True),
        AccountMeta(pda["associated_bonding_curve"], is_signer=False, is_writable=True),
        AccountMeta(constants.GLOBAL, is_signer=False, is_writable=False),
        AccountMeta(constants.MPL_TOKEN_METADATA, is_signer=False, is_writable=False),
        AccountMeta(pda["metadata"], is_signer=False, is_writable=True),
        AccountMeta(user, is_signer=True, is_writable=True),
        AccountMeta(SYSTEM_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(RENT, is_signer=False, is_writable=False),
        AccountMeta(constants.EVENT_AUTHORITY, is_signer=False, is_writable=False),
        AccountMeta(constants.PUMPFUN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]


def create_instruction_pda(mint: Pubkey) -> dict[str, Pubkey]:
    res = {}
    res["mint_authority"], _ = Pubkey.find_program_address([b"mint-authority"], constants.PUMPFUN_PROGRAM_ID)
    res["bonding_curve"] = res["bonding_curve"] = utils.get_bonding_curve(mint)
    res["associated_bonding_curve"] = utils.get_associated_bonding_curve(res["bonding_curve"], mint)
    res["metadata"], _ = Pubkey.find_program_address([
        b"metadata",
        bytes(constants.MPL_TOKEN_METADATA),
        bytes(mint)
    ], constants.MPL_TOKEN_METADATA)
    return res
