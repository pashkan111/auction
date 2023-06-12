from .exceptions import DoesNotExistsException


class UserDoesNotExists(DoesNotExistsException):
    message = "User does not exists"
