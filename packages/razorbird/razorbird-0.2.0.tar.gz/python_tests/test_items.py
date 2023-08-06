import pytest
import requests

_TIMEOUT = 3.05


@pytest.fixture()
def sample_items(api):
    # Clear all items on the running server first.
    resp = requests.delete(api + '/items', timeout=_TIMEOUT)
    resp.raise_for_status()

    resources = []

    for data in ({'color': 'green'}, [1, 2, 3, 5], {'x': 3.0, 'y': 4.0}):
        resp = requests.post(api + '/items', json=data, timeout=_TIMEOUT)
        resp.raise_for_status()

        resources.append(resp.headers.get('Location'))

    return resources


def test_get_empty_collection(api):
    resp = requests.get(api + '/items', timeout=_TIMEOUT)
    resp.raise_for_status()
    assert resp.json() == []


def test_delete_collection(api, sample_items):
    resp = requests.delete(api + '/items', timeout=_TIMEOUT)
    resp.raise_for_status()

    resp = requests.get(api + '/items', timeout=_TIMEOUT)
    resp.raise_for_status()
    assert resp.json() == []


def test_delete_item(api, sample_items):
    while sample_items:
        resp = requests.get(api + '/items', timeout=_TIMEOUT)
        resp.raise_for_status()
        assert len(resp.json()) == len(sample_items)

        resp_delete = requests.delete(
            api + sample_items.pop(), timeout=_TIMEOUT)
        assert resp_delete.status_code == 204


def test_get_item(api, sample_items):
    for resource in sample_items:
        resp = requests.get(api + resource, timeout=_TIMEOUT)
        resp.raise_for_status()
        assert resp.json()['id'] == resource.split('/')[-1]


def test_get_item_not_found(api, sample_items):
    for resource in sample_items:
        resp = requests.get(api + resource[:-1], timeout=_TIMEOUT)
        assert resp.status_code == 404
