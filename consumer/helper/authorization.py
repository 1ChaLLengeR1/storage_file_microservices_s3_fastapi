from fastapi import Depends
from database.database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authorization_create(key: str, db: Session = Depends(get_db)):
    pass

async def authorization_update(key: str, db: Session = Depends(get_db)):
    pass

async def authorization_delete(key: str, db: Session = Depends(get_db)):
    pass

async def authorization_main(key: str, db: Session = Depends(get_db)):
    pass
