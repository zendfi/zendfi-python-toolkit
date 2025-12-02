import os
from zendfi.client import from_env


if __name__ == '__main__':
    os.environ['ZENDFI_API_KEY'] = os.getenv('ZENDFI_API_KEY', 'env_key_123')
    os.environ['ZENDFI_BASE_URL'] = os.getenv('ZENDFI_BASE_URL', 'http://localhost:5555')
    client = from_env()
    print('client ready, api_key=', client.api_key)
