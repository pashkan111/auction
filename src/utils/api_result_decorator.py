from functools import wraps

from src.exceptions.api_exceptions import (BadRequestException,
                                           NotExistsException,
                                           StorageAPIException)
from src.exceptions.exceptions import (DoesNotExistsException,
                                       InvalidDataException, StorageException)


def result_decorator(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        try:
            result = await handler(*args, **kwargs)
        except DoesNotExistsException as e:
            raise NotExistsException(str(e))
        except InvalidDataException as e:
            raise BadRequestException(str(e))
        except StorageException as e:
            raise StorageAPIException(str(e))
        return result
    return wrapper
