from .exceptions import DoesNotExistsException, InvalidDataException


class AuctionDoesNotExists(DoesNotExistsException):
    message = "Auction does not exists"


class InvalidBidAmount(InvalidDataException):
    message = "Invalid bid amount. Must be greater than current price"


class BidDoesNotExists(DoesNotExistsException):
    message = "Bid does not exists"
