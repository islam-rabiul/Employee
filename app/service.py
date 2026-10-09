
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException, status
from . import crud, schemas

def create_user_service(db: Session, user: schemas.UserCreate):
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email address already exists."
        )
    if len(user.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters long"
        )
    new_user = crud.create_user_in_db(db=db, User=user)

    return new_user
def get_user_by_id_service(db: Session, user_id: int):
    user = crud.get_user_by_id(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} was not found."
        )
    return user
def get_all_users_service(db: Session=Depends(get_db)):
    return crud.get_all_user_from_db(db=db)

def get_user_by_email_service(db: Session, email: str):
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
def update_user_service(db: Session, user_id: int, user_update: schemas.UserUpdate):
    updated_user=crud.update_user_in_db(db, user_id=user_id, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

def delete_user_service(db: Session, user_id: int):

    deleted_user= crud.delete_user_from_db(db=db, user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
import time
import logging

# Set up logging to watch background output in the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def write_audit_log(action: str, email: str):
    """Simulates a lightweight background job (e.g., logging or sending notifications)."""
    time.sleep(2)
    logger.info(f"--- BACKGROUND AUDIT LOG --- Action: {action} | User Email: {email}")