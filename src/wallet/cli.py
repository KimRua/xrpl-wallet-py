import json
import sys
from pathlib import Path

import click
from .generator import create_wallet
from .secure_store import encrypt_to_file, decrypt_from_file


@click.group()
def cli() -> None: ...


@cli.command()
@click.option("--network", default="testnet", show_default=True)
@click.option("--out", type=click.Path(), default="mywallet.vault", show_default=True)
@click.option("--passphrase", prompt=True, hide_input=True,
              confirmation_prompt=True)
def create(network: str, out: str, passphrase: str) -> None:
    "Generate wallet and save encrypted vault."
    wallet = create_wallet(network)
    encrypt_to_file(wallet.__dict__, passphrase, out)
    click.echo(f"✅  wallet saved: {out}")


@cli.command()
@click.argument("vault", type=click.Path(exists=True))
@click.option("--passphrase", prompt=True, hide_input=True)
def show(vault: str, passphrase: str) -> None:
    "Decrypt vault and print wallet info."
    wallet = decrypt_from_file(passphrase, vault)
    click.echo(json.dumps(wallet, indent=2))


if __name__ == "__main__":
    cli(sys.argv[1:])
