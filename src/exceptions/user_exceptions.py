from .exceptions import DoesNotExistsException, InvalidDataException


class UserDoesNotExists(DoesNotExistsException):
    message = "User does not exists"


class WrongPasswordException(InvalidDataException):
    message = "Wrong password"
