from backend.database.connection import Base
import sqlalchemy as sa

class Sessions(Base):
    __tablename__ = "session"

    auth_token = sa.Column(sa.String(500), unique=True, primary_key=True)
    user_email = sa.Column(sa.String(500))
    access_token = sa.Column(sa.String())
    refresh_token = sa.Column(sa.String())
    token_uri = sa.Column(sa.String())
    client_id = sa.Column(sa.String())
    client_secret = sa.Column(sa.String())
    scopes = sa.Column(sa.String())
