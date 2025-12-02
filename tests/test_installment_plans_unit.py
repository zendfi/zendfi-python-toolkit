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
            if method == 'POST':
                return {'plan_id': 'iplan_1', 'status': 'created'}
            return [{'plan_id': 'iplan_1', 'status': 'created'}]
    return R()


if __name__ == '__main__':
    client = get_client()
    if os.getenv('ZENDFI_RUN_MOCK') == '1':
        requests.request = fake_request

    res = client.installment_plans.create({'customer_id': 'cust_1', 'amount': 1000})
    print('Create response:', json.dumps(res, indent=2))
    lst = client.installment_plans.list()
    print('List response:', json.dumps(lst, indent=2))
