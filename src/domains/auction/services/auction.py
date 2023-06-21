from src.domains.auction.models import Auction
from src.exceptions.auction_exceptions import InvalidBidAmount
from src.utils.custom_data_types import PriceType


def validate_bid(auction: Auction, bid_amount: PriceType) -> bool:
    if bid_amount < auction.current_price:
        raise InvalidBidAmount
    return True
