from typing import Optional, Dict, Any
from .client import ZendFi
from .utils import make_idempotency_key


class Subscriptions:
    def __init__(self, client: ZendFi):
        self._client = client

    # Plans
    def create_plan(self, data: Dict[str, Any], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        payload = data.copy()
        headers = {"Idempotency-Key": idempotency_key or make_idempotency_key()}
        return self._client._request("POST", "/api/v1/subscriptions/plans", json_data=payload, headers=headers)

    def get_plan(self, plan_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/api/v1/subscriptions/plans/{plan_id}")

    # Subscriptions
    def create(self, data: Dict[str, Any], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        headers = {"Idempotency-Key": idempotency_key or make_idempotency_key()}
        return self._client._request("POST", "/api/v1/subscriptions", json_data=data, headers=headers)

    def retrieve(self, subscription_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/api/v1/subscriptions/{subscription_id}")

    def cancel(self, subscription_id: str) -> Dict[str, Any]:
        return self._client._request("POST", f"/api/v1/subscriptions/{subscription_id}/cancel")
