from backend.database.connection import Base
import sqlalchemy as sa

class ToDo(Base):
    __tablename__ = "todo_tasks"

    id = sa.Column(sa.String(), unique=True, primary_key=True)
    course = sa.Column(sa.String())
    task_name = sa.Column(sa.String())
    status = sa.Column(sa.String())
    email = sa.Column(sa.String())      # for determining which user does this course belongs to
    link = sa.Column(sa.String(), nullable=True)
    due_date = sa.Column(sa.Date(), nullable=True)
