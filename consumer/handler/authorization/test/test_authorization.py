import pytest
from consumer.handler.authorization.authorization import authorization_create, authorization_update, authorization_delete, authorization_main
from database.database import SessionLocal

def test_authorization_create():
    db = SessionLocal()
    try:
        check_authorization_create = authorization_create("test", db)
        assert check_authorization_create.verify
        assert check_authorization_create.message == "Key is correct for create"
    except Exception as e:
        pytest.fail(f"Error: {e}")
    finally:
        db.close()



def test_authorization_update():
    db = SessionLocal()
    try:
        check_authorization_create = authorization_update("test", db)
        assert check_authorization_create.verify
        assert check_authorization_create.message == "Key is correct for update"
    except Exception as e:
        pytest.fail(f"Error: {e}")
    finally:
        db.close()

def test_authorization_delete():
    db = SessionLocal()
    try:
        check_authorization_create = authorization_delete("test", db)
        assert check_authorization_create.verify
        assert check_authorization_create.message == "Key is correct for delete"
    except Exception as e:
        pytest.fail(f"Error: {e}")
    finally:
        db.close()

def test_authorization_main():
    db = SessionLocal()
    try:
        check_authorization_create = authorization_main("test1", db)
        assert check_authorization_create.verify
        assert check_authorization_create.message == "Key is correct for main"
    except Exception as e:
        pytest.fail(f"Error: {e}")
    finally:
        db.close()
def test_authorization_create_main():
    db = SessionLocal()
    try:
        check_authorization_create = authorization_create("test1", db)
        assert check_authorization_create.verify
        assert check_authorization_create.message == "Key is correct for main"
    except Exception as e:
        pytest.fail(f"Error: {e}")
    finally:
        db.close()

