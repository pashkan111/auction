from decimal import Decimal

from src.exceptions.auction_exceptions import InvalidBidAmount
from src.utils.custom_data_types import PriceType


def validate_bid(auction_current_price: Decimal, bid_amount: PriceType) -> bool:
    if bid_amount < auction_current_price:
        raise InvalidBidAmount
    return True
