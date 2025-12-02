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
            return {
                "id": "550e8400-e29b-41d4-a716-446440000",
                "amount": 100.0,
                "currency": "USD",
                "status": "Pending",
                "qr_code": "solana:ABC123...?amount=100&spl-token=USDC",
                "payment_url": "https://zendfi.tech/pay/550e8400-e29b-41d4-a716-44440000",
                "expires_at": "2024-01-15T10:45:00Z",
                "split_ids": [
                    "660e8400-e29b-41d4-a716-446655440001",
                    "770e8400-e29b-41d4-a716-446655440002",
                    "880e8400-e29b-41d4-a716-446655440003",
                ],
            }

    return R()


if __name__ == '__main__':
    client = get_client()
    if os.getenv('ZENDFI_RUN_MOCK') == '1':
        requests.request = fake_request

    split_recipients = [
        {
            "recipient_wallet": "7xKXtg2CW87d97TXJ5jBkheTqA83TZRuJosgAsU",
            "recipient_name": "Seller - ArtisanPottery",
            "percentage": 85.0,
            "split_order": 1,
        },
        {
            "recipient_wallet": "8yKXtg2CW87d97TXJSDpbD5jBeTqA83TZRuJosgAsV",
            "recipient_name": "Platform Fee",
            "percentage": 10.0,
            "split_order": 2,
        },
        {
            "recipient_wallet": "9zKXtg2CW87d97TXJSDpbD5jBkhqA83TZRuJosgAsW",
            "recipient_name": "Payment Processor",
            "percentage": 5.0,
            "split_order": 3,
        },
    ]

    paymentSplit = client.payments.create(
        amount=100.00,
        currency="USD",
        token="USDC",
        description="Handmade Pottery - Order #12345",
        metadata={"order_id": "12345", "product": "Ceramic Vase", "seller": "ArtisanPottery"},
        split_recipients=split_recipients,
    )

    print('Payment result:')
    print(json.dumps(paymentSplit, indent=2, sort_keys=True))
