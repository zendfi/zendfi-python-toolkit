from typing import Optional, Dict, Any, List
from .client import ZendFi
from .utils import make_idempotency_key


class Escrows:
    def __init__(self, client: ZendFi):
        self._client = client

    def create(self, data: Dict[str, Any], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        headers = {"Idempotency-Key": idempotency_key or make_idempotency_key()}
        return self._client._request("POST", "/api/v1/escrows", json_data=data, headers=headers)

    def get(self, escrow_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/api/v1/escrows/{escrow_id}")

    def list(self, limit: int = 20, offset: Optional[int] = None) -> List[Dict[str, Any]]:
        qs = f"?limit={limit}"
        if offset is not None:
            qs += f"&offset={offset}"
        return self._client._request("GET", f"/api/v1/escrows{qs}")

    def approve(self, escrow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", f"/api/v1/escrows/{escrow_id}/approve", json_data=data)

    def refund(self, escrow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", f"/api/v1/escrows/{escrow_id}/refund", json_data=data)

    def dispute(self, escrow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("POST", f"/api/v1/escrows/{escrow_id}/dispute", json_data=data)
