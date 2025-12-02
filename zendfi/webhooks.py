from typing import Optional, Dict, Any
from .client import ZendFi
from .utils import verify_signature
from .errors import WebhookVerificationError


class Webhooks:
    def __init__(self, client: ZendFi):
        self._client = client

    def verify(self, payload: bytes, signature_header: str, secret: Optional[str] = None) -> Dict[str, Any]:
        secret = secret or self._client.api_key  # default to api key if user stores secret there (document clearly)
        ok = verify_signature(secret, payload, signature_header)
        if not ok:
            raise WebhookVerificationError("invalid webhook signature")
        # return parsed payload
        import json
        return json.loads(payload.decode())
