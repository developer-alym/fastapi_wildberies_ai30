from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Category
from db.schema import CategoryCreateSchema, CategoryListSchema
from typing import List

category_router = APIRouter(prefix='/category', tags=['Category'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/create', response_model=dict)
async def create_category(category_data:CategoryCreateSchema, db: Session = Depends(get_db)):
    category_db = Category(**category_data.dict())
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return {'status': 'Success created'}

@category_router.get('/list', response_model=List[CategoryListSchema])
async def get_list(db: Session = Depends(get_db)):
    category_db = db.query(Category).all()
    return category_db

@category_router.get('/detail/{category_id}', response_model=CategoryListSchema)
async def get_detail(category_id:int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynda category jok')
    return category_db

@category_router.put('/update/{category_id}', response_model=CategoryCreateSchema)
async def update_category(category_id:int, category_data:CategoryCreateSchema,db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    category_db.category_name = category_data.category_name
    category_db.category_image = category_data.category_image
    db.commit()
    db.refresh(category_db)
    return category_db

@category_router.delete('/delete/{category_id}', response_model=dict)
async def delete_category(category_id:int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    db.delete(category_db)
    db.commit()
    return {'status': 'Success deleted'}









