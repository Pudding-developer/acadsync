from backend.database.connection import Base
import sqlalchemy as sa


class Notifications(Base):
    __tablename__ = "notifications"

    