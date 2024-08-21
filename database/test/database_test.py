import pytest
from sqlalchemy import text
from database.database import engine, SessionLocal
def test_database_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
    finally:
        connection.close()

def test_db_session():
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Database connection failed while using ORM session: {e}")
    finally:
        db.close()
