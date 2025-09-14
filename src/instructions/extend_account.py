from solders.instruction import Instruction, AccountMeta
from solders.pubkey import Pubkey
from solders.system_program import ID as SYSTEM_PROGRAM_ID

from src import constants

DISCRIMINATOR = bytes([234, 102, 194, 203, 150, 72, 62, 229])

def extend_account_instruction(account: Pubkey, user: Pubkey) -> Instruction:
    accounts = extend_account_instruction_accounts(account, user)
    data = extend_account_instruction_data()
    return Instruction(
        program_id=constants.PUMPFUN_PROGRAM_ID,
        data=data,
        accounts=accounts,
    )

def extend_account_instruction_data() -> bytes:
    instruction_data = DISCRIMINATOR
    return instruction_data

def extend_account_instruction_accounts(account: Pubkey, user: Pubkey,) -> list[AccountMeta]:
    return [
        AccountMeta(account, is_signer=False, is_writable=True),
        AccountMeta(user, is_signer=True, is_writable=True),
        AccountMeta(SYSTEM_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(constants.EVENT_AUTHORITY, is_signer=False, is_writable=False),
        AccountMeta(constants.PUMPFUN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
