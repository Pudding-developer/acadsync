from flask import Blueprint
from backend.api.auth import auth_blueprint
from backend.api.gsuite_login import gsuite_login_blueprint
from backend.api.credential_register import credential_register_blueprint
from backend.api.gsuite_features import gsuite_features_blueprint
from backend.api.token_check import token_check_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(auth_blueprint)
api_blueprint.register_blueprint(credential_register_blueprint)
api_blueprint.register_blueprint(gsuite_features_blueprint)
api_blueprint.register_blueprint(gsuite_login_blueprint)
api_blueprint.register_blueprint(token_check_blueprint)

@api_blueprint.get("/")
def hello_api():
    return {
        "message": "Hello API!"
    }

