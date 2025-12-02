from typing import Optional, Dict, Any, List
from .client import ZendFi
from .utils import make_idempotency_key


class PaymentLinks:
    def __init__(self, client: ZendFi):
        self._client = client

    def create(self, data: Dict[str, Any], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        payload = data.copy()
        headers = {"Idempotency-Key": idempotency_key or make_idempotency_key()}
        return self._client._request("POST", "/api/v1/payment-links", json_data=payload, headers=headers)

    def retrieve(self, link_code: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/api/v1/payment-links/{link_code}")

    def list(self, limit: int = 20, offset: Optional[int] = None) -> List[Dict[str, Any]]:
        qs = f"?limit={limit}"
        if offset is not None:
            qs += f"&offset={offset}"
        return self._client._request("GET", f"/api/v1/payment-links{qs}")
