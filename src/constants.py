from solders.pubkey import Pubkey

PUMPFUN_PROGRAM_ID = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")
MPL_TOKEN_METADATA = Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")
FEE_RECIPIENT = Pubkey.from_string("9rPYyANsfQZw3DnDmKE3YCQF5E8oD89UXoHn9JFEhJUz")
FEE_PROGRAM_ID = Pubkey.from_string("pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ")

# ASSOCIATED_BONDING_CURVE_SEED = bytes([6, 221, 246, 225, 215, 101, 161, 147, 217, 203, 225, 70, 206, 235, 121, 172, 28, 180, 133, 237, 95, 91, 55, 145, 58, 140, 245, 133, 126, 255, 0, 169])
FEE_CONFIG_SEED = bytes([1, 86, 224, 246, 147, 102, 90, 207, 68, 219, 21, 104, 191, 23, 91, 170, 81, 137, 203, 151, 245, 210, 255, 59, 101, 93, 43, 182, 253, 109, 24, 176])


GLOBAL, _ = Pubkey.find_program_address([b"global"], PUMPFUN_PROGRAM_ID)
EVENT_AUTHORITY, _ = Pubkey.find_program_address([b"__event_authority"], PUMPFUN_PROGRAM_ID)
GLOBAL_VOLUME_ACCUMULATOR, _ = Pubkey.find_program_address([b"global_volume_accumulator"], PUMPFUN_PROGRAM_ID)
FEE_CONFIG, _ = Pubkey.find_program_address([b"fee_config", FEE_CONFIG_SEED], FEE_PROGRAM_ID)
