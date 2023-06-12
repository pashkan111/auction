from decimal import Decimal

from src.domains.auction.models import Auction
from src.exceptions.auction_exceptions import InvalidBidAmount


def validate_bid(auction: Auction, bid_amount: Decimal) -> bool:
    if bid_amount < auction.current_price:
        raise InvalidBidAmount
    return True
