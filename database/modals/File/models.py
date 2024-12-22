from sqlalchemy import Column, String, DateTime, ForeignKey
import uuid
from datetime import datetime
from database.database import Base


class File(Base):
    __tablename__ = "file"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    catalog_id = Column(String, ForeignKey('catalog.id'))
    mime_type = Column(String)
    file_name = Column(String)
    original_name = Column(String)
    file_size = Column(String)
    s3_url = Column(String)
    s3_path = Column(String)
    createUp = Column(DateTime, default=datetime.utcnow)
    updateUp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        orm_mode = True
