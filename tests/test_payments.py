
import json
from zendfi import ZendFi


def pretty_print_payment(p: dict) -> None:
    """Print a compact summary followed by the full JSON payload."""
    print("Payment summary:")
    print(f"  id: {p.get('id')}")
    print(f"  amount: {p.get('amount')} {p.get('currency')}")
    print(f"  status: {p.get('status')}")
    print(f"  payment_url: {p.get('payment_url')}")
    print(f"  expires_at: {p.get('expires_at')}")
    print()
    print("Full payload:")
    print(json.dumps(p, indent=2, sort_keys=True))


if __name__ == '__main__':
    # NOTE: this script performs a real API call. Keep credentials and amount minimal.
    client = ZendFi(api_key="YOUR_API_KEY")

    payment = client.payments.create(
        amount=1.00,
        currency="USD",
        token="USDC",
        description="Premium Course",
    )

    pretty_print_payment(payment)
