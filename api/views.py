from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from . import zadanie1
from . import zadanie2


@api_view(["POST"])
@parser_classes([JSONParser])
def process_names(request, format=None):
    """
    An endpoint that sorts the given data by 'second_name' and 'first_name'
    and appends the hash value to each item of provided list.
    """
    data_list = request.data.get("data_list")
    try:
        processed_data = zadanie1.process_data(data_list)
    except Exception:
        return Response({"error": "Cannot process provided data"})
    return Response({"result": processed_data})


@api_view(["POST"])
@parser_classes([JSONParser])
def calculate_price(request, format=None):
    """
    An endpoint giving the minimum price at which a given amount of bitcoin can be bought
    """
    orderbook = zadanie2.get_orderbook()
    buy = request.data.get("buy")

    try:
        price = zadanie2.get_bitcoin_price_multiple_transaction(
            bids=orderbook["bids"], buy=buy
        )
    except ValueError:
        return Response({"error": "Wrong input value type"})

    if price is None:
        return Response({"error": "Cannot buy this amount of bitcoins"})
    return Response({"price": price})
