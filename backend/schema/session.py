from backend.database.connection import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

class Session:
    session_token = Column(String, primary_key=True, unique=True)
    api_token = Column(String, unique=True)

