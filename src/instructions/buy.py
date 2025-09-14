from typing import Optional
import struct
from solders.instruction import Instruction, AccountMeta
from solders.pubkey import Pubkey
from solders.system_program import ID as SYSTEM_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID

from src import constants, utils

DISCRIMINATOR = bytes([102, 6, 61, 18, 1, 218, 235, 234])

def buy_instruction(mint: Pubkey, associated_user: Pubkey, user: Pubkey, creator: Pubkey, amount: int, max_sol_cost: int, track_volume: Optional[bool]) -> Instruction:
    accounts = buy_instruction_accounts(mint, associated_user, user, creator)
    data = buy_instruction_data(amount, max_sol_cost, track_volume)
    return Instruction(
        program_id=constants.PUMPFUN_PROGRAM_ID,
        data=data,
        accounts=accounts,
    )

def buy_instruction_data(amount: int, max_sol_cost: int, track_volume: Optional[bool]) -> bytes:
    instruction_data = DISCRIMINATOR
    instruction_data += struct.pack("<Q", amount)
    instruction_data += struct.pack("<Q", max_sol_cost)
    if track_volume is None:
        instruction_data += b'\x00'
    elif track_volume is False:
        instruction_data += b'\x01'
    else: # track_volume is True
        instruction_data += b'\x02'

    return instruction_data

def buy_instruction_accounts(mint: Pubkey, associated_user: Pubkey, user: Pubkey, creator: Pubkey) -> list[AccountMeta]:
    pda = buy_instruction_pda(mint, user, creator)
    return [
        AccountMeta(constants.GLOBAL, is_signer=False, is_writable=False),
        AccountMeta(constants.FEE_RECIPIENT, is_signer=False, is_writable=True),
        AccountMeta(mint, is_signer=False, is_writable=False),
        AccountMeta(pda["bonding_curve"], is_signer=False, is_writable=True),
        AccountMeta(pda["associated_bonding_curve"], is_signer=False, is_writable=True),
        AccountMeta(associated_user, is_signer=False, is_writable=True),
        AccountMeta(user, is_signer=True, is_writable=True),
        AccountMeta(SYSTEM_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pda["creator_vault"], is_signer=False, is_writable=True),
        AccountMeta(constants.EVENT_AUTHORITY, is_signer=False, is_writable=False),
        AccountMeta(constants.PUMPFUN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(constants.GLOBAL_VOLUME_ACCUMULATOR, is_signer=False, is_writable=True),
        AccountMeta(pda["user_volume_accumulator"], is_signer=False, is_writable=True),
        AccountMeta(constants.FEE_CONFIG, is_signer=False, is_writable=False),
        AccountMeta(constants.FEE_PROGRAM_ID, is_signer=False, is_writable=False),
    ]

def buy_instruction_pda(mint: Pubkey, user: Pubkey, creator: Pubkey) -> dict[str, Pubkey]:
    res = {}
    res["bonding_curve"] = utils.get_bonding_curve(mint)
    res["associated_bonding_curve"] = utils.get_associated_bonding_curve(res["bonding_curve"], mint)
    res["creator_vault"], _ = Pubkey.find_program_address([
        b"creator-vault",
        bytes(creator)
    ], constants.PUMPFUN_PROGRAM_ID)
    res["user_volume_accumulator"], _ = Pubkey.find_program_address([
        b"user_volume_accumulator",
        bytes(user)
    ], constants.PUMPFUN_PROGRAM_ID)
    return res
