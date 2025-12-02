import json
import time
from typing import Optional, Dict, Any
import requests

from .errors import APIError
from .utils import make_idempotency_key, get_env, build_url

try:
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    _HAS_TENACITY = True
except Exception:
    _HAS_TENACITY = False


class ZendFi:
    def __init__(self, api_key: str, base_url: Optional[str] = None, env: Optional[str] = None, timeout: int = 10):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url or get_env("ZENDFI_BASE_URL", "https://api.zendfi.tech")
        self.env = env or get_env("ZENDFI_ENV", "production")
        self.timeout = timeout

        # components
        from .payments import Payments
        from .customers import Customers
        from .invoices import Invoices
        from .webhooks import Webhooks
        from .subscriptions import Subscriptions
        from .payment_links import PaymentLinks
        from .installment_plans import InstallmentPlans
        from .escrows import Escrows

        self.payments = Payments(self)
        self.customers = Customers(self)
        self.invoices = Invoices(self)
        self.webhooks = Webhooks(self)
        self.subscriptions = Subscriptions(self)
        self.payment_links = PaymentLinks(self)
        self.installment_plans = InstallmentPlans(self)
        self.escrows = Escrows(self)

    def _headers(self, extra: Dict[str, str] = None) -> Dict[str, str]:
        h = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "zendfi-python/0.1.0",
        }
        if extra:
            h.update(extra)
        return h

    def _request(self, method: str, path: str, json_data: Dict[str, Any] = None, headers: Dict[str, str] = None):
        url = build_url(self.base_url, path)
        h = self._headers(headers)
        body = None if json_data is None else json.dumps(json_data)

        # retries
        if _HAS_TENACITY:
            @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8),
                   retry=retry_if_exception_type((requests.exceptions.RequestException,)))
            def _do():
                resp = requests.request(method, url, headers=h, data=body, timeout=self.timeout)
                return resp
            resp = _do()
        else:
            attempts = 3
            resp = None
            for i in range(attempts):
                try:
                    resp = requests.request(method, url, headers=h, data=body, timeout=self.timeout)
                except requests.exceptions.RequestException:
                    # network error -> retry
                    if i == attempts - 1:
                        raise
                    time.sleep(2 ** i)
                    continue

                # If server returned 5xx, consider retrying (transient server error)
                if resp is not None and 500 <= getattr(resp, 'status_code', 0) < 600:
                    # if this was the last attempt, break and let error handling below raise
                    if i == attempts - 1:
                        break
                    # exponential backoff then retry
                    time.sleep(2 ** i)
                    continue
                # success or non-retriable response -> break loop
                break

        if not resp.ok:
            try:
                data = resp.json()
                msg = data.get("message") or data
            except Exception:
                msg = resp.text
            raise APIError(resp.status_code, msg)
        try:
            return resp.json()
        except ValueError:
            return resp.text


def from_env() -> ZendFi:
    api_key = get_env("ZENDFI_API_KEY")
    if not api_key:
        raise ValueError("ZENDFI_API_KEY not set in environment")
    base = get_env("ZENDFI_BASE_URL")
    env = get_env("ZENDFI_ENV")
    return ZendFi(api_key=api_key, base_url=base, env=env)



