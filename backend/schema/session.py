from backend.database.connection import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

class Session:
    id = Column(String, primary_key=True, unique=True)
    user_id = Column(Integer)
