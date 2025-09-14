import yaml
import csv
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from solders.keypair import Keypair
from src import constants
from src.config import Config

def get_bonding_curve(mint: Pubkey) -> Pubkey:
    bonding_curve, _ = Pubkey.find_program_address([b"bonding-curve", bytes(mint)], constants.PUMPFUN_PROGRAM_ID)
    return bonding_curve

def get_associated_bonding_curve(bonding_curve: Pubkey, mint: Pubkey) -> Pubkey:
    associated_bonding_curve, _ = Pubkey.find_program_address([
        bytes(bonding_curve),
        bytes(TOKEN_PROGRAM_ID),
        bytes(mint)
    ], ASSOCIATED_TOKEN_PROGRAM_ID)
    return associated_bonding_curve

def load_config(path: str) -> Config:
    with open(path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
    return Config(**yaml_data)

def load_signers(path: str) -> list[Keypair]:
    accounts = []
    with open(path, "r") as file:
        accounts_raw = file.readlines()
    for account in accounts_raw:
        if account == "":
            continue
        keypair = Keypair.from_base58_string(account.strip())
        if keypair not in accounts:
            accounts.append(keypair)
    return accounts


def load_metadata(path: str) -> list[dict[str, str]]:
    metadata: list[dict[str, str]] = []
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        for row in csv_reader:
            metadata_obj = {}
            for i, value in enumerate(row):
                metadata_obj[headers[i]] = value
            metadata.append(metadata_obj)
    return metadata

def create_metadata_mapping(metadata: list[dict[str, str]], signers: list[Keypair]) -> dict[Keypair, list[dict[str, str]]]:
    metadata_mapping = {}
    metadata_per_signer = len(metadata) // len(signers)
    remainder = len(metadata) % len(signers)
    if metadata_per_signer <= 0:
        raise ValueError(f"Not enough metadata for signers. Metadata lines lengh: {len(metadata)}. Signers length: {len(signers)}")
    c = 0
    for i in range(len(metadata) - remainder):
        metadata_mapping.setdefault(signers[c], [])
        metadata_mapping[signers[c]].append(metadata[i])
        ci = (i + 1) / metadata_per_signer
        if ci == int(ci):
            c += 1
    c = 0
    length_without_remainder = len(metadata) - remainder
    for i in range(1, remainder + 1):
        metadata_mapping.setdefault(signers[c], [])
        metadata_mapping[signers[c]].append(metadata[length_without_remainder - 1 + i])
        c += 1
    return metadata_mapping
