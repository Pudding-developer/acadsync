from flask import Blueprint, redirect
from backend.modules.google import get_browser_auth_url

gsuite_login_blueprint = Blueprint("gsuite_login", __name__, url_prefix="/gsuite-login")


@gsuite_login_blueprint.get("/redirect")
def redirect_auth_url():
    return redirect(get_browser_auth_url())

