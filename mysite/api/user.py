from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import UserProfile
from db.schema import UserProfileUpdateSchema, UserProfileListSchema, UserProfileDetailSchema
from typing import List

user_router = APIRouter(prefix='/user', tags=['UserProfile'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @user_router.post('/create', response_model=UserProfileCreateSchema)
# async def create_user(user_data: UserProfileCreateSchema, db: Session = Depends(get_db)):
#     user_db = UserProfile(**user_data.dict())
#     db.add(user_db)
#     db.commit()
#     db.refresh(user_db)
#     return user_db

@user_router.get('/list', response_model=List[UserProfileListSchema])
async def list_user(db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).all()
    return user_db

@user_router.get('/detail/{user_id}', response_model=UserProfileDetailSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Munday adam jok')
    return user_db


@user_router.put('/update/{user_id}', response_model=dict)
async def update_user(user_id:int, user_data: UserProfileUpdateSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday adam jok')
    for key, value in user_data.dict().items():
        setattr(user_db, key, value)
    db.commit()
    db.refresh(user_db)
    return {'status': 'success updated'}

@user_router.delete('/delete/{user_id}', response_model=dict)
async def delete_user(user_id:int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday adam jok')
    db.delete(user_db)
    db.commit()
    return {'status': 'success deleted'}













