from typing import TypedDict, Union, Dict, Any, List
from fastapi.responses import JSONResponse


class ResponseData(TypedDict, total=False):
    is_valid: bool
    data: Union[str, Dict[str, Any], List[Any]]
    status_code: int
    status: str


class ResponseApiData:
    def __init__(self, status: str, status_code: int, data=None):
        self.status = status
        self.status_code = status_code
        self.data = data

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            content={
                'status': self.status,
                'status_code': self.status_code,
                'data': self.data,
            },
            status_code=self.status_code
        )
