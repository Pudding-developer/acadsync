from backend.modules.google import handle_oauth_callback
from flask import Blueprint
from flask import request
from flask import redirect
from flask import make_response

credential_register_blueprint = Blueprint("credential_register", __name__, url_prefix="/credential-register")

@credential_register_blueprint.get("/")
def register_credential_to_database():
    _, auth_token = handle_oauth_callback(request.url)

    response = make_response(redirect("/homepage"))
    response.set_cookie("auth_token", auth_token)
    return response
