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
                return {'id': 'link_1', 'hosted_page_url': 'https://pay.example/abc'}
            return [{'id': 'link_1', 'hosted_page_url': 'https://pay.example/abc'}]
    return R()


if __name__ == '__main__':
    client = get_client()
    if os.getenv('ZENDFI_RUN_MOCK') == '1':
        requests.request = fake_request

    link = client.payment_links.create({'amount': 1000, 'currency': 'USD'})
    print('Link:', json.dumps(link, indent=2))
    links = client.payment_links.list()
    print('Links list:', json.dumps(links, indent=2))
