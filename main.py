from fastapi import FastAPI, HTTPException, Depends, UploadFile
from typing import Union
from database.database import get_db
from sqlalchemy.orm import Session
from database.modals.Catalog.models import Catalog
from config.s3_deps import s3_auth
from botocore.client import BaseClient



app = FastAPI()

@app.get("/catalogs")
async def create_item(db: Session = Depends(get_db)):

    catalogs = db.query(Catalog).all()
    return catalogs

@app.get("/bukets")
def get_buckets(s3: BaseClient = Depends(s3_auth)):
    response = s3.list_buckets()

    return response['Buckets']
@app.post("/uploadfile/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}