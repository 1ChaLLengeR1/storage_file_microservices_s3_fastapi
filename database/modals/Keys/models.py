from sqlalchemy import Column, String, DateTime
import uuid
from datetime import datetime
from database.database import Base

class Keys(Base):
    __tablename__ = "keys"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String)
    password = Column(String)
    createUp = Column(DateTime, default=datetime.utcnow())

    class Config:
        orm_mode = True