from backend.modules.google import get_user_courses
from backend.modules.google import get_user_credentials
from backend.modules.google import get_user_tasks
from backend.modules.google import create_user_task
from backend.modules.google import finish_user_task
from backend.modules.google import set_course_link
from backend.modules.google import get_unread_notifs
from backend.modules.google import mark_course_as_viewed

from flask import Blueprint
from flask import request

gsuite_features_blueprint = Blueprint("gsuite_features", __name__, url_prefix="/gsuite-features")

@gsuite_features_blueprint.get("/classroom/courses")
def get_classroom_courses():
    auth_token = request.cookies.get("auth_token")
    if auth_token is None:
        return { "messsage": "Not authenticated" }

    return get_user_courses(auth_token)

@gsuite_features_blueprint.get("/profile/")
def get_user_profile():
    auth_token = request.cookies.get("auth_token")
    if auth_token is None:
        return { "messsage": "Not authenticated" }

    return get_user_credentials(auth_token)

############################
#  Tasks operation routes  #
############################
@gsuite_features_blueprint.get("/classroom/task")
def get_classroom_tasks():
    auth_token = request.cookies.get("auth_token")
    if auth_token is None:
        return { "messsage": "Not authenticated" }

    include_query = request.args.get("include_done", None)
    return get_user_tasks(auth_token, include_query is not None)

@gsuite_features_blueprint.post("/classroom/task")
def create_task():
    auth_token = request.cookies.get("auth_token")
    if auth_token is None:
        return { "messsage": "Not authenticated" }

    request_body = request.get_json(force=True)
    task_name = request_body.get("task_name")
    task_due = request_body.get("task_due")

    if task_due == "":
        task_due = None

    return create_user_task(auth_token, task_name, task_due)

@gsuite_features_blueprint.delete("/classroom/finish-task/<id>")
def finish_task(id):
    return finish_user_task(id)


#######################
#  Class Chat routes  #
#######################
@gsuite_features_blueprint.post("/classroom/set-link/<id>")
def add_messenger_link(id: str):
    auth_token = request.cookies.get("auth_token")
    if auth_token is None:
        return { "messsage": "Not authenticated" }

    request_body = request.get_json(force=True)
    messenger_link = request_body.get("messenger_link")

    if messenger_link is None:
        return { "message": "Messenger link is not set" }

    return set_course_link(auth_token, id, messenger_link)


#########################
#  Notification routes  #
#########################
@gsuite_features_blueprint.get("/notification/unread")
def get_unread_notifs_route():
    auth_token = request.cookies.get("auth_token")
    if auth_token is None:
        return { "messsage": "Not authenticated" }

    return get_unread_notifs(auth_token)


@gsuite_features_blueprint.get("/notification/read/<id>")
def read_notif(id):
    auth_token = request.cookies.get("auth_token")
    if auth_token is None:
        return { "messsage": "Not authenticated" }

    return mark_course_as_viewed(id)


