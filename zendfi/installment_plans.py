from typing import Optional, Dict, Any, List
from .client import ZendFi
from .utils import make_idempotency_key


class InstallmentPlans:
    def __init__(self, client: ZendFi):
        self._client = client

    def create(self, data: Dict[str, Any], idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        headers = {"Idempotency-Key": idempotency_key or make_idempotency_key()}
        return self._client._request("POST", "/api/v1/installment-plans", json_data=data, headers=headers)

    def get(self, plan_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/api/v1/installment-plans/{plan_id}")

    def list(self, limit: int = 20, offset: Optional[int] = None) -> List[Dict[str, Any]]:
        qs = f"?limit={limit}"
        if offset is not None:
            qs += f"&offset={offset}"
        return self._client._request("GET", f"/api/v1/installment-plans{qs}")

    def list_customer_plans(self, customer_wallet: str) -> List[Dict[str, Any]]:
        return self._client._request("GET", f"/api/v1/customers/{customer_wallet}/installment-plans")

    def cancel(self, plan_id: str) -> Dict[str, Any]:
        return self._client._request("POST", f"/api/v1/installment-plans/{plan_id}/cancel")
