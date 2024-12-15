from fastapi import Depends
from database.database import get_db
from sqlalchemy.orm import Session
from consumer.helper.authorization import verify_password
from database.modals.Keys.models import Keys
from consumer.data.response import ResponseData


def authorization_create(key: str, db: Session = Depends(get_db)) -> ResponseData:
    check_main_key = authorization_main(key, db)
    if check_main_key['is_valid']:
        return ResponseData(
            is_valid=True,
            status_code=200,
            data="Key is correct for create"
        )

    check_keys = db.query(Keys).filter(Keys.type == "create").all()

    for item_key in check_keys:
        check_password = verify_password(key, item_key.password)
        if check_password:
            return ResponseData(
                is_valid=True,
                status_code=200,
                data="Key is correct for create"
            )

    return ResponseData(
        is_valid=False,
        status_code=403,
        data={"error": "Key is incorrect for create"}
    )


def authorization_update(key: str, db: Session = Depends(get_db)) -> ResponseData:
    check_main_key = authorization_main(key, db)
    if check_main_key['is_valid']:
        return ResponseData(
            is_valid=True,
            status_code=200,
            data="Key is correct for main"
        )

    check_keys = db.query(Keys).filter(Keys.type == "update").all()
    for item_key in check_keys:
        check_password = verify_password(key, item_key.password)
        if check_password:
            return ResponseData(
                is_valid=True,
                status_code=200,
                data="Key is correct for update"
            )

    return ResponseData(
        is_valid=False,
        status_code=403,
        data={"error": "Key is incorrect for update"}
    )


def authorization_delete(key: str, db: Session = Depends(get_db)) -> ResponseData:
    check_main_key = authorization_main(key, db)
    if check_main_key['is_valid']:
        return ResponseData(
            is_valid=True,
            status_code=200,
            data="Key is correct for main"
        )

    check_keys = db.query(Keys).filter(Keys.type == "delete").all()

    for item_key in check_keys:
        check_password = verify_password(key, item_key.password)
        if check_password:
            return ResponseData(
                is_valid=True,
                status_code=200,
                data="Key is correct for delete"
            )

    return ResponseData(
        is_valid=False,
        status_code=403,
        data={"error": "Key is incorrect for delete"}
    )


def authorization_main(key: str, db: Session = Depends(get_db)) -> ResponseData:
    check_keys = db.query(Keys).filter(Keys.type == "main").all()
    for item_key in check_keys:
        check_password = verify_password(key, item_key.password)
        if check_password:
            return ResponseData(
                is_valid=True,
                status_code=200,
                data="Key is correct for main"
            )

    return ResponseData(
        is_valid=False,
        status_code=403,
        data={"error": "Key is incorrect for main"}
    )
