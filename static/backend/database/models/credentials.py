from backend.database.connection import Base
import sqlalchemy as sa

class Credentials(Base):
    api_token = sa.Column(sa.String(500), unique=True)