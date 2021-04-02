import json

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """
    Provides client for test views
    """
    return APIClient()


@pytest.fixture
def orderbook():
    """
    Provides orderbook for tests
    """
    with open("fixtures/test_orderbook.json", "r") as file:
        data = json.load(file)
    return data
