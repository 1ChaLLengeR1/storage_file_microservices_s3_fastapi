from sqlalchemy import Column, String, DateTime
import uuid
from datetime import datetime
from database.database import Base

class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    bucketName = Column(String)
    name = Column(String)
    originalName = Column(String)
    path = Column(String)
    url = Column(String)
    createUp = Column(DateTime, default=datetime.utcnow)
    updateUp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        orm_mode = True
