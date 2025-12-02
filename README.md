# zendfi-python-sdk

This is a Python SDK port of zendfi-toolkit. It provides simple sync clients for Payments, Customers, Invoices and Webhooks verification.

## Quickstart

```py
from zendfi import from_env
client = from_env()

payment = client.payments.create(amount=50.0, currency="USD", description="Test")
print(payment.get("checkout_url"))
```

## Tests

Run:

```
pip install -r requirements-dev.txt
pytest -q
```

Integration tests

To run tests against the real ZendFi API (BE CAREFUL — these perform real requests):

1. Set your API key and enable integration runs:

```powershell
$env:ZENDFI_API_KEY = "sk_live_..."
$env:ZENDFI_RUN_INTEGRATION = "1"
# Optional: override base URL (e.g. staging)
$env:ZENDFI_BASE_URL = "https://api.zendfi.tech/"
pytest -q -k integration
```

The integration test is guarded so it only runs when `ZENDFI_RUN_INTEGRATION` and
`ZENDFI_API_KEY` are present in the environment.

## Publishing

This repository provides a `pyproject.toml` and `MANIFEST.in` ready for building source and wheel distributions. Quick steps to publish:

- Build distributions locally: `python -m build`
- Upload to PyPI (use a PyPI API token): `python -m twine upload dist/*`

A GitHub Actions workflow (`.github/workflows/publish.yml`) is included to publish on tagged releases. Configure the `PYPI_API_TOKEN` secret in the repository settings before pushing a `vX.Y.Z` tag.

Security note: Never commit real API keys or PyPI tokens to the repository. Use environment variables or CI secrets.
