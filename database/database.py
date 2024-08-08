from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

host = config("DB_HOST")
port = config("DB_PORT", cast=int)
user = config("DB_USER")
password = config("DB_PASSWORD")
dbName = config("DB_DBNAME")

if not all([host, port, user, password, dbName]):
    raise ValueError("One or more database environment variables are missing.")

data_base_url = f"postgresql://{user}:{password}@{host}:{port}/{dbName}"
engine = create_engine(data_base_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
