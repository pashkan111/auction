from fastapi.exceptions import HTTPException


class AbstractAPIException(HTTPException):
    status_code: int = 500
    detail: str = 'Exception In API'

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)


class StorageAPIException(AbstractAPIException):
    status_code = 500
    detail = 'Exception In Storage'


class NotExistsException(AbstractAPIException):
    status_code = 404
    detail = 'Object does not exists'


class BadRequestException(AbstractAPIException):
    status_code = 400
    detail = 'Bad Request'
