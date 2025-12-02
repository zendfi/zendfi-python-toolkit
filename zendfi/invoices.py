from typing import Optional, Dict, Any, List
from .client import ZendFi
from .utils import make_idempotency_key


class Invoices:
    def __init__(self, client: ZendFi):
        self._client = client

    def create(
        self,
        amount: float,
        currency: str = "USD",
        *,
        # Customer identification: either `customer_id` or provide email/name
        customer_id: Optional[str] = None,
        customer_email: Optional[str] = None,
        customer_name: Optional[str] = None,
        token: Optional[str] = None,
        description: Optional[str] = None,
        line_items: Optional[List[Dict[str, Any]]] = None,
        due_date: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an invoice.

        Accepts either `customer_id` or `customer_email` (+ optional `customer_name`).
        Pass `line_items` as a list of {description, quantity, unit_price} dicts.
        """
        payload: Dict[str, Any] = {
            "amount": amount,
            "currency": currency,
        }

        if customer_id:
            payload["customer_id"] = customer_id
        else:
            # allow creating invoices by providing customer email/name
            if customer_email:
                payload["customer_email"] = customer_email
            if customer_name:
                payload["customer_name"] = customer_name

        if token:
            payload["token"] = token
        if description:
            payload["description"] = description
        if line_items:
            payload["line_items"] = line_items
        if due_date:
            payload["due_date"] = due_date
        if metadata:
            payload["metadata"] = metadata

        headers = {"Idempotency-Key": idempotency_key or make_idempotency_key()}
        return self._client._request("POST", "/api/v1/invoices", json_data=payload, headers=headers)

    def retrieve(self, invoice_id: str) -> Dict[str, Any]:
        return self._client._request("GET", f"/api/v1/invoices/{invoice_id}")

    def list(self, limit: int = 20, starting_after: Optional[str] = None) -> Dict[str, Any]:
        qs = f"?limit={limit}"
        if starting_after:
            qs += f"&starting_after={starting_after}"
        return self._client._request("GET", f"/api/v1/invoices{qs}")

    def send(self, invoice_id: str) -> Dict[str, Any]:
        """Send an invoice to the customer via email (POST /api/v1/invoices/:id/send).

        Returns the API response which typically includes success, invoice_id,
        invoice_number, sent_to, payment_url, and updated status.
        """
        return self._client._request("POST", f"/api/v1/invoices/{invoice_id}/send")
