import pytest
from sqlalchemy import text

# Import funkcji i zmiennych z Twojego kodu
from database.database import engine, SessionLocal
def test_database_connection():
    try:
        # Otwarcie połączenia bez użycia sesji ORM
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_db_session():
    try:
        # Otwarcie sesji ORM
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Database connection failed while using ORM session: {e}")
    finally:
        db.close()
