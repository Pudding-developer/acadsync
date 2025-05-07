from backend.modules.google import handle_oauth_callback
from backend.modules.background import load_latest_user_announcements
from flask import Blueprint
from flask import request
from flask import redirect
from flask import make_response
from threading import Thread

credential_register_blueprint = Blueprint("credential_register", __name__, url_prefix="/credential-register")

@credential_register_blueprint.get("/")
def register_credential_to_database():
    _, auth_token = handle_oauth_callback(request.url)

    # handle the syncing of data for this newly logged in user
    th = Thread(target=load_latest_user_announcements, args=(auth_token, ))
    th.start()

    response = make_response(redirect("/homepage"))
    response.set_cookie("auth_token", auth_token)
    return response
