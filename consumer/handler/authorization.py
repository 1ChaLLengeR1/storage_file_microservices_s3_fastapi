from fastapi import Depends
from database.database import get_db
from sqlalchemy.orm import Session
from consumer.helper.authorization import verify_password
from pydantic import BaseModel
from database.modals.Keys.models import Keys

class VerifyResult(BaseModel):
    verify: bool
    message: str
def authorization_create(key: str, db: Session = Depends(get_db)) -> VerifyResult:

    check_main_key = authorization_main(key, db)
    if check_main_key.verify:
        return VerifyResult(
            verify=True,
            message="Key is correct for main"
        )

    check_keys = db.query(Keys).filter(Keys.type == "create").all()

    for item_key in check_keys:
        check_password = verify_password(key, item_key.password)
        if check_password:
            return VerifyResult(
                verify=True,
                message="Key is correct for create"
            )

    return VerifyResult(
        verify=False,
        message="Key is incorrect for create"
    )


def authorization_update(key: str, db: Session = Depends(get_db)) -> VerifyResult:

    check_main_key = authorization_main(key, db)
    if check_main_key.verify:
        return VerifyResult(
            verify=True,
            message="Key is correct for main"
        )

    check_keys = db.query(Keys).filter(Keys.type == "update").all()
    for item_key in check_keys:
        check_password = verify_password(key, item_key.password)
        if check_password:
            return VerifyResult(
                verify=True,
                message="Key is correct for update"
            )

    return VerifyResult(
        verify=False,
        message="Key is incorrect for update"
    )

def authorization_delete(key: str, db: Session = Depends(get_db)) -> VerifyResult:

    check_main_key = authorization_main(key, db)
    if check_main_key.verify:
        return VerifyResult(
            verify=True,
            message="Key is correct for main"
        )

    check_keys = db.query(Keys).filter(Keys.type == "delete").all()

    for item_key in check_keys:
        check_password = verify_password(key, item_key.password)
        if check_password:
            return VerifyResult(
                verify=True,
                message="Key is correct for delete"
            )

    return VerifyResult(
        verify=False,
        message="Key is incorrect for delete"
    )

def authorization_main(key: str, db: Session = Depends(get_db)) -> VerifyResult:

    check_keys = db.query(Keys).filter(Keys.type == "main").all()
    for item_key in check_keys:
        check_password = verify_password(key, item_key.password)
        if check_password:
            return VerifyResult(
                verify=True,
                message="Key is correct for main"
            )

    return VerifyResult(
        verify=False,
        message="Key is incorrect for main"
    )
