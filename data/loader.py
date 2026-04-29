from __future__ import annotations

import hashlib
import hmac
import json
import struct
import zlib
from pathlib import Path

_ALLOWED_LANGS = {"sk", "cz", "en", "es"}
_MAGIC = b"PTE1"

# Built-in offline data key.
# This is practical obfuscation for a local learning app, not bank-grade DRM.
_KEY_TEXT = "PyTrainerEdu|offline-packed-data|v1.1.0|Tibor-Majka-SuPyWomen|no-plain-json"
_KEY = hashlib.sha256(_KEY_TEXT.encode("utf-8")).digest()

_BASE_DIR = Path(__file__).resolve().parent.parent
_PACKED_DIR = _BASE_DIR / "data_packed"
_JSON_DIR = Path(__file__).resolve().parent


def _keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < length:
        out.extend(hashlib.sha256(key + nonce + struct.pack(">Q", counter)).digest())
        counter += 1
    return bytes(out[:length])


def _unpack_pte(path: Path):
    blob = path.read_bytes()
    if len(blob) < 52 or blob[:4] != _MAGIC:
        raise ValueError(f"Invalid PyTrainerEdu packed data file: {path.name}")

    nonce = blob[4:20]
    tag = blob[20:52]
    ciphertext = blob[52:]

    expected = hmac.new(_KEY, _MAGIC + nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        raise ValueError(f"Packed data integrity check failed: {path.name}")

    stream = _keystream(_KEY, nonce, len(ciphertext))
    compressed = bytes(a ^ b for a, b in zip(ciphertext, stream))
    raw = zlib.decompress(compressed)
    return json.loads(raw.decode("utf-8"))


def _load_data(prefix: str, lang: str):
    if lang not in _ALLOWED_LANGS:
        raise ValueError(f"Unsupported language: {lang}")

    packed_path = _PACKED_DIR / f"{prefix}_{lang}.pte"
    if packed_path.exists():
        return _unpack_pte(packed_path)

    # Developer fallback: useful when editing questions before packing.
    json_path = _JSON_DIR / f"{prefix}_{lang}.json"
    if json_path.exists():
        return json.loads(json_path.read_text(encoding="utf-8"))

    raise FileNotFoundError(f"Missing data file for {prefix}_{lang}: {packed_path} or {json_path}")


def load_questions(lang: str):
    return _load_data("questions", lang)


def load_texts(lang: str):
    return _load_data("texts", lang)
