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
    class R:
        ok = True
        def json(self):
            if method == 'POST' and url.endswith('/approve'):
                return {'status': 'approved'}
            if method == 'POST' and url.endswith('/refund'):
                return {'status': 'refunded'}
            if method == 'POST' and url.endswith('/dispute'):
                return {'status': 'disputed'}
            if method == 'POST':
                return {'id': 'esc_1', 'status': 'created'}
            return [{'id': 'esc_1', 'status': 'created'}]
    return R()


if __name__ == '__main__':
    client = get_client()
    if os.getenv('ZENDFI_RUN_MOCK') == '1':
        requests.request = fake_request

    esc = client.escrows.create({'amount': 1000, 'buyer': 'b1'})
    print('Escrow create:', json.dumps(esc, indent=2))
    apr = client.escrows.approve('esc_1', {'tx': 'sig'})
    print('Approve response:', json.dumps(apr, indent=2))
    ref = client.escrows.refund('esc_1', {'reason': 'test'})
    print('Refund response:', json.dumps(ref, indent=2))
    dis = client.escrows.dispute('esc_1', {'reason': 'fraud'})
    print('Dispute response:', json.dumps(dis, indent=2))
