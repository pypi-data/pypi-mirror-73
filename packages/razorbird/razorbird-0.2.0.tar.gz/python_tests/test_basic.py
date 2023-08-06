import requests

_TIMEOUT = 3.05


def test_get(api):
    resp = requests.get(api, timeout=_TIMEOUT)
    resp.raise_for_status()

    assert resp.text == 'Hello, World!'
    assert 'text/plain' in resp.headers.get('Content-Type')
