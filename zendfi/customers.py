from typing import Optional, Dict, Any
from .client import ZendFi
from .utils import make_idempotency_key


class Customers:
    def __init__(self, client: ZendFi):
        self._client = client

    def create(self, email: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        payload = {"email": email}
        if name:
            payload["name"] = name
        if metadata:
            payload["metadata"] = metadata

        headers = {"Idempotency-Key": idempotency_key or make_idempotency_key()}
        return self._client._request("POST", "/api/v1/customers", json_data=payload, headers=headers)

    def retrieve(self, customer_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/api/v1/customers/{customer_id}")

    def update(self, customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("PATCH", f"/api/v1/customers/{customer_id}", json_data=data)

    def delete(self, customer_id: str) -> Dict[str, Any]:
        return self._client._request("DELETE", f"/api/v1/customers/{customer_id}")

    def list(self, limit: int = 20, starting_after: Optional[str] = None) -> Dict[str, Any]:
        qs = f"?limit={limit}"
        if starting_after:
            qs += f"&starting_after={starting_after}"
        return self._client._request("GET", f"/api/v1/customers{qs}")
from typing import Optional, Dict, Any
from .client import ZendFi
from .utils import make_idempotency_key

class Customers:
    def __init__(self, client: ZendFi):
        self._client = client

    def create(self, email: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        payload = {"email": email}
        if name:
            payload["name"] = name
        if metadata:
            payload["metadata"] = metadata

        headers = {"Idempotency-Key": idempotency_key or make_idempotency_key()}
        return self._client._request("POST", "/customers", json_data=payload, headers=headers)

    def retrieve(self, customer_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/customers/{customer_id}")

    def update(self, customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("PATCH", f"/customers/{customer_id}", json_data=data)

    def delete(self, customer_id: str) -> Dict[str, Any]:
        return self._client._request("DELETE", f"/customers/{customer_id}")

    def list(self, limit: int = 20, starting_after: Optional[str] = None) -> Dict[str, Any]:
        qs = f"?limit={limit}"
        if starting_after:
            qs += f"&starting_after={starting_after}"
        return self._client._request("GET", f"/customers{qs}")
from typing import Optional, Dict, Any
from .client import ZendFi
from .utils import make_idempotency_key


class Customers:
    def __init__(self, client: ZendFi):
        self._client = client

    def create(self, email: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        payload = {"email": email}
        if name:
            payload["name"] = name
        if metadata:
            payload["metadata"] = metadata

        headers = {"Idempotency-Key": idempotency_key or make_idempotency_key()}
        return self._client._request("POST", "/customers", json_data=payload, headers=headers)

    def retrieve(self, customer_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/customers/{customer_id}")

    def update(self, customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._client._request("PATCH", f"/customers/{customer_id}", json_data=data)

    def delete(self, customer_id: str) -> Dict[str, Any]:
        return self._client._request("DELETE", f"/customers/{customer_id}")

    def list(self, limit: int = 20, starting_after: Optional[str] = None) -> Dict[str, Any]:
        qs = f"?limit={limit}"
        if starting_after:
            qs += f"&starting_after={starting_after}"
        return self._client._request("GET", f"/customers{qs}")
