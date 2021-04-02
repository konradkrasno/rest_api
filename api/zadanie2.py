from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import List, Dict

import requests
from django.conf import settings


def get_orderbook() -> Dict:
    return requests.get(url=settings.ORDERBOOK_URL).json()


def get_bitcoin_price_one_transaction(bids: List, buy: str) -> str:
    """
    Returns the minimum price of bitcoin that can be bought with a single transaction.
    """
    try:
        buy = Decimal(buy)
    except InvalidOperation:
        raise ValueError

    sorted_bids = sorted(bids, key=lambda x: x[0])
    for item in sorted_bids:
        if Decimal(str(item[1])) >= buy:
            return str(
                Decimal(item[0]).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
            )


def get_bitcoin_price_multiple_transaction(bids: List, buy: str) -> str:
    """
    Returns the minimum price of bitcoin that can be bought by making multiple transactions.
    """
    try:
        to_buy = Decimal(buy)
    except InvalidOperation:
        raise ValueError

    sorted_bids = sorted(bids, key=lambda x: x[0])
    bought = Decimal(0)
    price_weights = []

    for item in sorted_bids:
        if bought < to_buy:
            quantity = Decimal(str(item[1]))
            price = Decimal(str(item[0]))
            transaction = (
                quantity if to_buy - bought >= quantity else to_buy - bought
            )
            bought += transaction
            price_weights.append(price * transaction / to_buy)
        else:
            return str(
                sum(price_weights).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
            )
