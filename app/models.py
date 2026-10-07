from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    email = Column(String)
    date=Column(DateTime)
    password = Column(String)
    domain= Column(String)
