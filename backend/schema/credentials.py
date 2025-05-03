from backend.database.connection import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

class Credentials:
    user_id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    google_token = Column(String)
    messenger_token = Column(String)
