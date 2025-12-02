import os
import hmac
import hashlib
from zendfi.client import ZendFi, from_env
from zendfi.errors import WebhookVerificationError


def get_client():
    if os.getenv('ZENDFI_API_KEY'):
        return from_env()
    return ZendFi(api_key='test_key', base_url='http://localhost:5555')


if __name__ == '__main__':
    client = get_client()

    payload = b'{"event":"payment.created","merchant_id":"m_1","timestamp":1234}'
    secret = os.getenv('ZENDFI_WEBHOOK_SECRET', 'whsec_test')
    sig = 'sha256=' + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

    try:
        res = client.webhooks.verify(payload, sig, secret=secret)
        print('Verified webhook payload:', res)
    except WebhookVerificationError:
        print('Webhook verification failed (as expected if signature mismatch)')
