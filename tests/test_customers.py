

def test_create_customer(monkeypatch, client):
    def fake_request(method, url, headers=None, data=None, timeout=None):
        class R:
            ok = True

            def json(self):
                return {"id": "cust_123", "email": "a@b.com"}

        return R()

    monkeypatch.setattr('requests.request', fake_request)
    res = client.customers.create(email='a@b.com', name='Alex')
    assert res['email'] == 'a@b.com'
