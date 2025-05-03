from flask import Blueprint, redirect

credential_register_blueprint = Blueprint("credential_register", __name__, url_prefix="/credential-register")

@credential_register_blueprint.get("/")
def register_credential_to_database():
    # session registration here...
    return redirect("/homepage")

