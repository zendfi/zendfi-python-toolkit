import os
import json
import requests
from zendfi.client import ZendFi, from_env


def get_client():
    if os.getenv('ZENDFI_RUN_MOCK') == '1':
        return ZendFi(api_key='test_key', base_url='http://localhost:5555')
    if os.getenv('ZENDFI_API_KEY'):
        return from_env()
    raise RuntimeError('Set ZENDFI_API_KEY or ZENDFI_RUN_MOCK=1')


def fake_request(method, url, headers=None, data=None, timeout=None):
    print('MOCK REQUEST:', method, url)
    print('HEADERS:', headers)
    print('DATA:', data)

    class R:
        ok = True

        def json(self):
            return {"id": "inv_123", "amount": 3500.0}

    return R()


if __name__ == '__main__':
    client = get_client()
    if os.getenv('ZENDFI_RUN_MOCK') == '1':
        requests.request = fake_request

    line_items = [
        {"description": "A", "quantity": 1, "unit_price": 100.0},
    ]

    res = client.invoices.create(
        amount=100.0,
        currency='USD',
        customer_email='client@example.com',
        customer_name='Acme',
        token='USDC',
        description='Test',
        line_items=line_items,
        due_date='2025-11-15T23:59:59Z',
        metadata={'k': 'v'},
    )

    print(json.dumps(res, indent=2))
