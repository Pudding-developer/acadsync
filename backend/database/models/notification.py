from backend.database.connection import Base
import sqlalchemy as sa


class Notifications(Base):
    __tablename__ = "notifications"

    id = sa.Column(sa.Integer(), unique=True, primary_key=True)
    owner = sa.Column(sa.String())
    notification_id = sa.Column(sa.String())
    course_id = sa.Column(sa.String())
    is_latest = sa.Column(sa.Boolean())