from sqlalchemy import Column, String, DateTime
import uuid
from datetime import datetime
from database.database import Base
from sqlalchemy.dialects import postgresql as psql

class Keys(Base):
    __tablename__ = "keys"

    id = Column(psql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String)
    password = Column(String)
    createUp = Column(DateTime, default=datetime.utcnow())

    class Config:
        orm_mode = True