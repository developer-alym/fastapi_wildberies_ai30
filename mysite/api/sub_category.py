from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import SubCategory, Category
from db.schema import SubCategorySchema
from typing import List


sub_category_router = APIRouter(prefix='/sub_category', tags=['SubCategory'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@sub_category_router.post('/create', response_model=SubCategorySchema)
async def create_sub(sub_data:SubCategorySchema, db: Session = Depends(get_db)):
    sub_category_id = db.query(Category).filter(Category.id == sub_data.category_id).first()
    if not sub_category_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday category_id jok')
    sub_db = SubCategory(**sub_data.dict())
    db.add(sub_db)
    db.commit()
    db.refresh(sub_db)
    return sub_db










