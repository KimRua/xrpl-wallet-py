"""
Very-lightweight AES-256-GCM file vault.
DO NOT use for production secrets; replace with KMS/HSM later.
"""
from __future__ import annotations

import json
import os
from base64 import b64encode, b64decode
from dataclasses import asdict
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

_SALT_SIZE = 16
_NONCE_SIZE = 12
_KEY_LEN = 32


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=_KEY_LEN, n=2**15, r=8, p=1)
    return kdf.derive(password.encode())


def encrypt_to_file(obj: Any, password: str, path: str | Path) -> None:
    data = json.dumps(obj).encode()
    salt = os.urandom(_SALT_SIZE)
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(_NONCE_SIZE)
    ct = aesgcm.encrypt(nonce, data, None)
    blob = b"|".join([salt, nonce, ct])
    Path(path).write_bytes(b64encode(blob))


def decrypt_from_file(password: str, path: str | Path) -> Any:
    blob = b64decode(Path(path).read_bytes())
    salt, nonce, ct = blob.split(b"|", 2)
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    data = aesgcm.decrypt(nonce, ct, None)
    return json.loads(data.decode())
