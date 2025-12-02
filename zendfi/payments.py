from typing import Optional, Dict, Any, List
from .client import ZendFi
from .utils import make_idempotency_key


class Payments:
    def __init__(self, client: ZendFi):
        self._client = client

    def create(self, amount: float, currency: str, token: str, description: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, split_recipients: Optional[List[Dict[str, Any]]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        payload = {
            "amount": amount,
            "currency": currency,
            "token": token,
        }
        if description:
            payload["description"] = description
        if metadata:
            payload["metadata"] = metadata
        if split_recipients:
            # Expect list of dicts with recipient_wallet, recipient_name, percentage, split_order, etc.
            payload["split_recipients"] = split_recipients

        headers = {}
        headers["Idempotency-Key"] = idempotency_key or make_idempotency_key()

        return self._client._request("POST", "/api/v1/payments", json_data=payload, headers=headers)

    def retrieve(self, payment_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/api/v1/payments/{payment_id}")

    def list(self, limit: int = 20, starting_after: Optional[str] = None) -> Dict[str, Any]:
        qs = f"?limit={limit}"
        if starting_after:
            qs += f"&starting_after={starting_after}"
        return self._client._request("GET", f"/api/v1/payments{qs}")
