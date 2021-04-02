import pytest
from api.zadanie1 import hash_data, sort_data_by_names, process_data
from api.zadanie2 import (
    get_bitcoin_price_one_transaction,
    get_bitcoin_price_multiple_transaction,
)
from fixtures.test_data import input_data, sorted_data, result


def test_hash_data():
    assert (
        hash_data("Jan", "Kowalski", "1977-11-10")
        == f"d371d82da0bcb79c71d8a9d56a5272732f01ed3496887620c6f10ef9fa823e3a"
    )


def test_sort_data():
    assert sort_data_by_names(input_data["data_list"]) == sorted_data["data_list"]


def test_process_data():
    assert process_data(input_data["data_list"]) == result["result"]


def test_process_names_when_valid(client):
    response = client.post("/zadanie1/", data=input_data, format="json")
    assert response.status_code == 200
    assert response.data == result


def test_process_names_when_invalid(client):
    response = client.post("/zadanie1/", data={}, format="json")
    assert response.status_code == 200
    assert response.data == {"error": "Cannot process provided data"}


def test_get_bitcoin_price_one_transaction(orderbook):
    price = get_bitcoin_price_one_transaction(bids=orderbook["bids"], buy="0.1234")
    assert price == "227402.01"


def test_get_bitcoin_price_one_transaction_when_invalid_input(orderbook):
    with pytest.raises(ValueError):
        get_bitcoin_price_one_transaction(bids=orderbook["bids"], buy="invalid")


def test_get_bitcoin_price_one_transaction_when_buy_over_all_bids(orderbook):
    price = get_bitcoin_price_one_transaction(bids=orderbook["bids"], buy="10")
    assert not price


def test_get_bitcoin_price_multiple_transaction(orderbook):
    price = get_bitcoin_price_multiple_transaction(bids=orderbook["bids"], buy="0.1234")
    assert price == "227400.58"


def test_get_bitcoin_price_multiple_transaction_when_buy_over_all_bitcoins(orderbook):
    price = get_bitcoin_price_multiple_transaction(bids=orderbook["bids"], buy="10")
    assert not price


def test_get_bitcoin_price_multiple_transaction_when_invalid_input(orderbook):
    with pytest.raises(ValueError):
        get_bitcoin_price_multiple_transaction(bids=orderbook["bids"], buy="invalid")


def test_calculate_price(client, mocker, orderbook):
    mocker.patch("api.zadanie2.get_orderbook", return_value=orderbook)
    response = client.post("/zadanie2/", data={"buy": "0.1234"}, format="json")
    assert response.status_code == 200
    assert response.data == {"price": "227400.58"}


def test_calculate_price_when_invalid(client, mocker, orderbook):
    mocker.patch("api.zadanie2.get_orderbook", return_value=orderbook)
    response = client.post("/zadanie2/", data={"buy": "invalid"}, format="json")
    assert response.status_code == 200
    assert response.data == {"error": "Wrong input value"}


def test_calculate_price_when_wrong_data(client, mocker, orderbook):
    mocker.patch("api.zadanie2.get_orderbook", return_value=orderbook)
    response = client.post("/zadanie2/", data={"buy": ["0.1234"]}, format="json")
    assert response.status_code == 200
    assert response.data == {"error": "Wrong input value type"}


def test_calculate_price_buy_over_all_bitcoins(client, mocker, orderbook):
    mocker.patch("api.zadanie2.get_orderbook", return_value=orderbook)
    response = client.post("/zadanie2/", data={"buy": "10"}, format="json")
    assert response.status_code == 200
    assert response.data == {"error": "Cannot buy this amount of bitcoins"}
