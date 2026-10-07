# app/services.py
from . import crud, schemas
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.exceptions import HTTPException

def create_user_service(db: Session, user: schemas.UserCreate):
    # Step 1: Business rule validation (Check if password is strong enough)
    if len(user.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters long"
        )


    new_user = crud.create_user_in_db(db=db, User=user)

    return new_user

def get_all_users_service(db: Session=Depends(get_db)):
    return crud.get_all_user_from_db(db=db)

def get_user_by_id_service(db: Session, user_id: int):
    return crud.get_user_by_id(db, id=user_id)

def get_user_by_email_service(db: Session, email: str):
    return crud.get_user_by_email(db, email=email)

def update_user_service(db: Session, user_id: int, user_update: schemas.UserUpdate):
    return crud.update_user_in_db(db=db, user_id=user_id, user_update=user_update)

def delete_user_service(db: Session, user_id: int):
    return crud.delete_user_from_db(db=db, user_id=user_id)