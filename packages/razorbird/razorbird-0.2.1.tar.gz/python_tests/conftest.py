import subprocess
import time

import pytest
import requests


razorbird = None


def pytest_sessionstart(session):
    global razorbird

    razorbird = subprocess.Popen(('razorbird', 'example'))

    # NOTE(vytas): give the server some time to start.
    for attempt in range(3):
        try:
            requests.get('http://127.0.0.1:8000/', timeout=3)
            break
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.2)


def pytest_sessionfinish(session, exitstatus):
    razorbird.kill()
    razorbird.communicate()


@pytest.fixture
def api():
    return 'http://127.0.0.1:8000'
