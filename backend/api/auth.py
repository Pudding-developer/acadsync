from backend.database.connection import SessionLocal
from backend.database.models.sessions import Sessions

from flask import Blueprint
from flask import request
from flask import redirect

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.get("/logout")
def logout_route():
    request_cookies = request.cookies
    auth_token = request_cookies.get("auth_token")

    db = SessionLocal()
    try:
        db.query(Sessions).filter(
            Sessions.auth_token == auth_token
        ).delete()
        db.commit()

        return redirect("/")
    finally:
        db.close()

