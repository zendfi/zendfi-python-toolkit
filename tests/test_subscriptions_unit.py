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
            if '/plans' in url:
                return {'id': 'plan_1', 'name': 'Basic'}
            return {'id': 'sub_1', 'status': 'active'}
    return R()


if __name__ == '__main__':
    client = get_client()
    if os.getenv('ZENDFI_RUN_MOCK') == '1':
        requests.request = fake_request

    plan = client.subscriptions.create_plan({'name': 'Basic', 'amount': 1000})
    print('Plan:', json.dumps(plan, indent=2))
    sub = client.subscriptions.create({'plan_id': 'plan_1', 'customer_id': 'cust_1'})
    print('Subscription:', json.dumps(sub, indent=2))
