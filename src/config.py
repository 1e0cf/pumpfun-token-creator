from pydantic_settings import BaseSettings

class Config(BaseSettings):
    rpc_url: str = "https://api.mainnet-beta.solana.com"
    signers: str = "signers.txt"
    metadata: str = "metadata.csv"
    sleep_time: int = 5 # in minutes
    unit_price: int = 50_000 # priority fee when not use mev providers
    buy_amount_sol: float = 0.0001 # buy amount in SOL
