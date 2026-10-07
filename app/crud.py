from sqlalchemy.orm import Session
from sqlalchemy import text
from . import schemas
from . import models

def create_user_in_db(db: Session, User: schemas.UserCreate):
    query = text("""
        INSERT INTO users(name, email, date, password,domain)
        VALUES (:name,:email, :date,:password, :domain)
        RETURNING id,name, email, date, password,domain;
    """)

    result = db.execute(query, User.model_dump())

    db.commit()

    return result.fetchone()


def get_all_user_from_db(db: Session):
    query = text("SELECT id, name, email, date, domain FROM users;")
    result = db.execute(query)

    return result.fetchall()
def get_user_by_email(db: Session, email: str):
    query = text("SELECT * FROM users WHERE email = :email")
    result = db.execute(query, {"email": email}).first()
    return result


def get_user_by_id(db: Session, id: int):
    query = text("SELECT * FROM users WHERE id = :user_id;")

    result = db.execute(query, {"user_id": id}).first()

    return result


def update_user_in_db(db: Session, user_id: int, user_update: schemas.UserUpdate):
    # 1. Extract only the fields explicitly provided by the user
    update_data = user_update.model_dump(exclude_unset=True)

    # If no fields were provided to update, just fetch and return the existing user
    if not update_data:
        check_query = text("SELECT * FROM users WHERE id = :user_id;")
        return db.execute(check_query, {"user_id": user_id}).first()

    # 2. Dynamically build the SET clause for the SQL query based on what was passed
    set_clauses = []
    params = {"user_id": user_id}

    for key, value in update_data.items():
        if value is not None:  # Safety check so nulls don't wipe data
            set_clauses.append(f"{key} = :{key}")
            params[key] = value

    if not set_clauses:
        return db.execute(text("SELECT * FROM users WHERE id = :user_id;"), {"user_id": user_id}).first()

    set_string = ", ".join(set_clauses)
    query = text(f"""
        UPDATE users 
        SET {set_string} 
        WHERE id = :user_id 
        RETURNING id, name, email, date, domain;
    """)

    result = db.execute(query, params)
    db.commit()

    updated_user = result.fetchone()
    return updated_user

def delete_user_from_db(db: Session, user_id: int):
    # 1. Fetch the existing user by ID
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None

    # 2. Delete and commit changes
    db.delete(db_user)
    db.commit()
    return db_user