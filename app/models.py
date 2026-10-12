
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)  # Indexed for fast lookups
    date = Column(DateTime)
    password = Column(String)
    domain = Column(String, index=True)  # Indexed for fast filtering by department/domain
