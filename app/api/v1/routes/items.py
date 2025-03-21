from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.item import ItemCreate, ItemResponse
from app.services.item_service import create_item, get_items

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ItemResponse)
def create_item_api(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.get("/", response_model=list[ItemResponse])
def get_items_api(db: Session = Depends(get_db)):
    return get_items(db)
