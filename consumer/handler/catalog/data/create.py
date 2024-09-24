from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HandlerCatalogResponse(BaseModel):
    id: Optional[str] = None
    bucketName: Optional[str] = None
    name: Optional[str] = None
    originalName: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None
    createUp: Optional[datetime] = None
    updateUp: Optional[datetime] = None