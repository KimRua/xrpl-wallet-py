"""
Wallet generation utilities.
"""
from dataclasses import dataclass
from typing import Literal
from xrpl.wallet import Wallet


@dataclass(frozen=True, slots=True)
class WalletInfo:
    classic_address: str
    seed: str
    pub_key: str
    priv_key: str


def create_wallet(network: Literal["testnet", "mainnet"] = "testnet") -> WalletInfo:
    """
    Create a new ED25519 wallet.
    On mainnet generation is allowed, but funding is _your_ responsibility.
    """
    wallet = Wallet.create()  # ED25519 by default
    return WalletInfo(
        classic_address=wallet.classic_address,
        seed=wallet.seed,
        pub_key=wallet.public_key,
        priv_key=wallet.private_key,
    )
