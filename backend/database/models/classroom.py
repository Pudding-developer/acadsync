from backend.database.connection import Base
import sqlalchemy as sa

class Classroom(Base):
    __tablename__ = "classroom"

    id = sa.Column(sa.Integer(), primary_key=True, unique=True)
    classid = sa.Column(sa.String())
    name = sa.Column(sa.String())
    room = sa.Column(sa.String())
    section = sa.Column(sa.String())
    courseState = sa.Column(sa.String())
    alternateLink = sa.Column(sa.String())
    messengerLink = sa.Column(sa.String(), nullable=True)
    owner = sa.Column(sa.String())
