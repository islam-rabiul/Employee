from fastapi import FastAPI, Depends, BackgroundTasks,Query
from sqlalchemy.orm import Session
from typing import List

from . import schemas, models,service
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User API", version="1.0")

#
# @app.post("/user/", response_model=schemas.UserResponse)
# def create_user(user: schemas.UserCreate,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
#     new_user = service.create_user_service(db=db, user=user)
#
#     background_tasks.add_task(
#         service.write_audit_log,
#         action="USER_CREATED",
#         email=new_user.email
#     )
#
#     return new_user


from app.queue import task_queue
from app.tasks import generate_user_report


@app.post("/user/", response_model=schemas.UserResponse)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    new_user = service.create_user_service(db=db, user=user)
    try:
        task_queue.enqueue(
            generate_user_report,
            user_email=new_user.email
        )
    except Exception as e:
        print(f"Redis queue warning: {e}")

    return new_user

@app.get("/user/", response_model=List[schemas.UserResponse])
def get_all_user_records(db: Session = Depends(get_db)):
    return service.get_all_users_service(db=db)

@app.get("/user/email/{email}", response_model=schemas.UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return service.get_user_by_email_service(db=db, email=email)


@app.get("/user/id/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return service.get_user_by_id_service(db, user_id=id)

@app.put("/user/id/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    return service.update_user_service(db=db, user_id=id, user_update=user_update)


@app.delete("/user/id/{id}", response_model=schemas.UserResponse)
def delete_user(id: int, db: Session = Depends(get_db)):
    return service.delete_user_service(db=db, user_id=id)
@app.get("/users/filter", response_model=List[schemas.UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    domain: str | None = None,
    db: Session = Depends(get_db)
):
    return service.get_users_service(db=db, skip=skip, limit=limit, search=search, domain=domain)
