from backend.config.appconfig import SQLITE_PATH
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# important objects that will be used throughout the app
Engine = create_engine(
    SQLITE_PATH,
    connect_args={"check_same_thread": False}
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


# function for committing changes
def commit_change(session_local: Session, model_object):
    session_local.commit()
    session_local.refresh(model_object)
