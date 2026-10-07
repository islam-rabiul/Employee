from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import schemas, models,service
from .database import engine, get_db
from . import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API", version="1.0")

@app.post("/user/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.create_user_service(db=db, user=user)

@app.get("/user/", response_model=List[schemas.UserResponse])
def get_all_user_records(db: Session = Depends(get_db)):
    return service.get_all_users_service(db=db)

@app.get("/user/{email}", response_model=schemas.UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = service.get_user_by_email_service(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/user/id/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = service.get_user_by_id_service(db, user_id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/user/id/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = service.update_user_service(db=db, user_id=id, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/user/id/{id}", response_model=schemas.UserResponse)
def delete_user(id: int, db: Session = Depends(get_db)):
    deleted_user = service.delete_user_service(db=db, user_id=id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user