import pytest
from consumer.handler.authorization import authorization_create, authorization_update, authorization_delete, authorization_main
from database.database import SessionLocal
@pytest.mark.asyncio
async def test_authorization_create():
    db = SessionLocal()
    try:
        check_authorization_create = await authorization_create("test", db)
        assert check_authorization_create.verify
        assert check_authorization_create.message == "Key is correct for create"
    except Exception as e:
        pytest.fail(f"Error: {e}")
    finally:
        db.close()


@pytest.mark.asyncio
async def test_authorization_update():
    db = SessionLocal()
    try:
        check_authorization_create = await authorization_update("test", db)
        assert check_authorization_create.verify
        assert check_authorization_create.message == "Key is correct for update"
    except Exception as e:
        pytest.fail(f"Error: {e}")
    finally:
        db.close()
@pytest.mark.asyncio
async def test_authorization_delete():
    db = SessionLocal()
    try:
        check_authorization_create = await authorization_delete("test", db)
        assert check_authorization_create.verify
        assert check_authorization_create.message == "Key is correct for delete"
    except Exception as e:
        pytest.fail(f"Error: {e}")
    finally:
        db.close()
@pytest.mark.asyncio
async def test_authorization_main():
    db = SessionLocal()
    try:
        check_authorization_create = await authorization_main("test1", db)
        assert check_authorization_create.verify
        assert check_authorization_create.message == "Key is correct for main"
    except Exception as e:
        pytest.fail(f"Error: {e}")
    finally:
        db.close()

