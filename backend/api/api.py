from flask import Blueprint
from backend.api.gsuite_login import gsuite_login_blueprint
from backend.api.credential_register import credential_register_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(gsuite_login_blueprint)
api_blueprint.register_blueprint(credential_register_blueprint)

@api_blueprint.get("/")
def hello_api():
    return {
        "message": "Hello API!"
    }

