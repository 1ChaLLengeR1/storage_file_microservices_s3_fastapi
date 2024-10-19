from pydantic import BaseModel
from typing import Optional


class ResponseError(BaseModel):
    error: Optional[str] = None