class AbstractException(Exception):
    message: str

    def __init__(self, message: str | None = None, detail: str | None = None):
        if message is None:
            message = self.message
        self.args = (message, detail)
        super().__init__(message)


class StorageException(AbstractException):
    message = "Exception In Storage"


class DoesNotExistsException(AbstractException):
    message = "Object does not exists"


class InvalidDataException(AbstractException):
    message = "Invalid data"
