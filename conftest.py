import os
import sys

import pytest

src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.append(src_dir)


# https://docs.pytest.org/en/latest/monkeypatch.html#global-patch-example-preventing-requests-from-remote-operations
@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")
