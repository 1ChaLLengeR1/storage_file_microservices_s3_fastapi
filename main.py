from fastapi import FastAPI, HTTPException, Depends
from database.database import get_db
from sqlalchemy.orm import Session
from database.modals.Catalog.models import Catalog

app = FastAPI()

@app.get("/catalogs")
async def create_item(db: Session = Depends(get_db)):

    catalogs = db.query(Catalog).all()
    return catalogs