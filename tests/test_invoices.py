import json
import os
import sys
from zendfi import ZendFi, from_env


def pretty_print_invoice(inv: dict) -> None:
    print("Invoice summary:")
    print(f"  id: {inv.get('id')}")
    print(f"  amount: {inv.get('amount')} {inv.get('currency')}")
    print(f"  status: {inv.get('status')}")
    print(f"  invoice_url: {inv.get('invoice_url') or inv.get('payment_url')}")
    print(f"  due_date: {inv.get('due_date')}")
    print()
    print("Full payload:")
    print(json.dumps(inv, indent=2, sort_keys=True))


if __name__ == '__main__':
    # NOTE: this script performs a real API call. Use `ZENDFI_RUN_MOCK=1` for mock
    # or set `ZENDFI_API_KEY` in the environment.
    if os.environ.get('ZENDFI_RUN_MOCK') == '1':
        import requests

        def fake_request(method, url, headers=None, data=None, timeout=None):
            # Minimal mock for create and send endpoints
            class R:
                def __init__(self, status_code=200, data=None):
                    self.status_code = status_code
                    self._data = data or {"success": True}

                @property
                def ok(self):
                    return 200 <= self.status_code < 300

                def json(self):
                    return self._data

                @property
                def text(self):
                    import json as _j

                    return _j.dumps(self._data)

            if url.endswith('/api/v1/invoices') and method == 'POST':
                return R(201, {"invoice_id": "inv_mock_1", "invoice_number": "INV-MOCK-0001", "amount": 500.0, "currency": "USD"})
            if url.endswith('/send') and method == 'POST':
                return R(200, {"success": True, "invoice_id": "inv_mock_1", "status": "sent", "sent_to": "client@dee.com"})
            if '/api/v1/invoices/' in url and method == 'GET':
                return R(200, {"invoice_id": "inv_mock_1", "amount": 500.0, "currency": "USD", "status": "pending"})
            return R(404, {"error": "not_found"})

        requests.request = fake_request
        client = ZendFi(api_key='zfi_test_mock', base_url='https://api.zendfi.tech')
    else:
        try:
            client = from_env()
        except Exception as exc:
            print('Set ZENDFI_API_KEY to run integration tests or use ZENDFI_RUN_MOCK=1')
            print('Error:', exc)
            sys.exit(2)

    line_items = [
        {"description": "Frontend Development (React)", "quantity": 40, "unit_price": 50.00},
        {"description": "Backend API Development", "quantity": 30, "unit_price": 50.00},
        {"description": "UI/UX Design", "quantity": 10, "unit_price": 100.00},
        {"description": "Project Manager", "quantity": 1, "unit_price": 0.00},
    ]

    invoice = client.invoices.create(
        amount=500.00,
        currency="USD",
        customer_email="client@dee.com",
        customer_name="Deev Solutions LLC",
        token="SOL",
        description="Web Services",
        line_items=line_items,
        due_date="2025-12-1T23:59:59Z",
        metadata={"project_id": "proj_q4_21029", "po_number": "PO-12235"},
    )

    pretty_print_invoice(invoice)
    # Attempt to send the invoice via the API
    invoice_id = invoice.get('id') or invoice.get('invoice_id') or invoice.get('data', {}).get('invoice_id')
    if invoice_id:
        sent = client.invoices.send(invoice_id=invoice_id)
        print("\nSend result:")
        pretty_print_invoice(sent)
    else:
        print('Could not determine invoice id from create response; skipping send')
