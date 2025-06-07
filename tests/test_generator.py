from wallet.generator import create_wallet


def test_create_wallet() -> None:
    w = create_wallet()
    assert w.classic_address.startswith("r")
    assert len(w.seed) > 10
