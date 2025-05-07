from backend.database.connection import SessionLocal
from backend.database.models.sessions import Sessions

from flask import Blueprint
from flask import request

token_check_blueprint = Blueprint("token_check", __name__, url_prefix="/token-check")


@token_check_blueprint.get("/")
def token_check():
    request_cookie: dict = request.cookies
    token = request_cookie.get("auth_token")

    db = SessionLocal()
    active_sessions = db.query(Sessions).filter(
        Sessions.auth_token == token
    ).first()
    db.close()


    if active_sessions is None:
        return { "active": False }

    return { "active": True }

