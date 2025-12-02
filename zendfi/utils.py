import os
import uuid
import hmac
import hashlib
from typing import Optional, Dict, Any


def make_idempotency_key(provided: Optional[str] = None) -> str:
    return provided or str(uuid.uuid4())


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key, default)


def build_url(base: str, path: str) -> str:
    return base.rstrip("/") + "/" + path.lstrip("/")


def verify_signature(secret: str, payload: bytes, signature: str) -> bool:
    # expected header format: "sha256=hexdigest"
    try:
        if signature.startswith("sha256="):
            sig = signature.split("=", 1)[1]
        else:
            sig = signature
        mac = hmac.new(secret.encode(), payload, hashlib.sha256)
        return hmac.compare_digest(mac.hexdigest(), sig)
    except Exception:
        return False
