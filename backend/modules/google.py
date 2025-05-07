from backend.config.appconfig import API_TOKEN_ASSIGNMENT_PATH
from backend.database.connection import SessionLocal
from backend.database.models.sessions import Sessions
from backend.database.models.assignments import ToDo
from backend.database.models.classroom import Classroom
from backend.database.models.notification import Notifications
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import date
from datetime import datetime
from uuid import uuid4

from sqlalchemy import and_
import os

# allows http redirection
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

config_path = "backend/config/credentials.json"
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.announcements',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]


def model_to_dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


# opens a browser to allow user from accessing its google data
def get_browser_auth_url():
    flow = Flow.from_client_secrets_file(
        config_path,
        scopes=SCOPES,
        redirect_uri=API_TOKEN_ASSIGNMENT_PATH
    )

    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url


def handle_oauth_callback(authorization_response_url: str):
    flow = Flow.from_client_secrets_file(
        config_path,
        scopes=SCOPES,
        redirect_uri=API_TOKEN_ASSIGNMENT_PATH
    )
    flow.fetch_token(authorization_response=authorization_response_url)
    creds = flow.credentials

    # Get user info
    oauth2_service = build("oauth2", "v2", credentials=creds)
    userinfo = oauth2_service.userinfo().get().execute()
    user_email = userinfo["email"]
    auth_token = str(uuid4())

    # Save to DB
    db = SessionLocal()
    existing = db.query(Sessions).filter_by(user_email=user_email).first()
    if not existing:
        session = Sessions(
            auth_token=auth_token,
            user_email=user_email,
            access_token=creds.token,
            refresh_token=creds.refresh_token,
            token_uri=creds.token_uri,
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            scopes=",".join(creds.scopes)
        )
        db.add(session)
    else:
        existing.auth_token = auth_token
        existing.access_token = creds.token
        existing.refresh_token = creds.refresh_token
        existing.scopes = ",".join(creds.scopes)
    db.commit()
    db.close()

    return user_email, auth_token

# retrieves user credentials with the given api token
def get_user_credentials(auth_token):
    db = SessionLocal()
    session = db.query(Sessions).filter_by(
        auth_token=auth_token
    ).first()
    db.close()

    if not session:
        return {
            "message": "Unauthenticated"
        }

    creds = Credentials(
        token=session.access_token,
        refresh_token=session.refresh_token,
        token_uri=session.token_uri,
        client_id=session.client_id,
        client_secret=session.client_secret,
        scopes=session.scopes.split(",")
    )

    service = build("oauth2", "v2", credentials=creds)
    userinfo = service.userinfo().get().execute()
    return userinfo


def get_user_courses(auth_token: str):
    db = SessionLocal()
    session = db.query(Sessions).filter_by(
        auth_token=auth_token
    ).first()
    db.close()

    if not session:
        return {
            "message": "Unauthenticated"
        }

    courses = db.query(Classroom).filter(
        Classroom.owner == session.user_email
    ).all()

    return [model_to_dict(course) for course in courses]


def get_user_tasks(auth_token: str, include_done: bool):
    db = SessionLocal()
    session = db.query(Sessions).filter_by(
        auth_token=auth_token
    ).first()

    try:
        my_email = session.user_email
        if include_done:
            todo_task = db.query(ToDo).filter(
                and_(
                    ToDo.email == my_email,
                    ToDo.course == "local-acadsync"
                )
            ).all()
        else:
            todo_task = db.query(ToDo).filter(
                and_(
                    ToDo.email == my_email,
                    ToDo.status.in_(["CREATED", "NEW"])
                )
            ).all()

        return [model_to_dict(task) for task in todo_task]

    finally:
        db.close()


def create_user_task(auth_token: str, task_name: str, task_duedate: date):
    db = SessionLocal()
    try:
        session = db.query(Sessions).filter_by(
            auth_token=auth_token
        ).first()

        dt = None
        if task_duedate is not None:
            dt = datetime.strptime(task_duedate, "%Y-%m-%dT%H:%M")

        new_task = ToDo(
            id=str(uuid4()),
            course="local-acadsync",
            task_name=task_name,
            status="CREATED",
            email=session.user_email,
            link=None,
            due_date=dt
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return model_to_dict(new_task)

    finally:
        db.close()

def set_course_link(auth_token: str, id: int, messenger_link: str):
    db = SessionLocal()
    try:
        session = db.query(Sessions).filter_by(
            auth_token=auth_token
        ).first()

        if session is None:
            return { "messenger": "Unauthenticated" }

        matched_course = db.query(Classroom).filter(Classroom.id == id).first()
        if matched_course is not None:
            matched_course.messengerLink = messenger_link
            db.commit()
            db.refresh(matched_course)
            return { "messenger": "Successfuly set messenger link for course" }
        return { "messenger": "Link not set for nonexistent course" }
    finally:
        db.close()

def finish_user_task(task_id: str):
    db = SessionLocal()
    try:
        matched_task = db.query(ToDo).filter_by(
            id=task_id
        ).first()

        if matched_task is not None:
            matched_task.status = "TURNED_IN"
            db.commit()
            db.refresh(matched_task)

        return {
            "data": model_to_dict(matched_task),
            "message": "Successfully marked task as finished"
        }
    finally:
        db.close()


def load_users_tasks(auth_token: str):
    db = SessionLocal()

    try:
        session = db.query(Sessions).filter_by(
            auth_token=auth_token
        ).first()

        if not session:
            return {
                "message": "Unauthenticated"
            }

        creds = Credentials(
            token=session.access_token,
            refresh_token=session.refresh_token,
            token_uri=session.token_uri,
            client_id=session.client_id,
            client_secret=session.client_secret,
            scopes=session.scopes.split(",")
        )

        service = build("classroom", "v1", credentials=creds)

        # Get enrolled courses
        tasks = []
        courses = service.courses().list().execute().get("courses", [])
        for course in courses:
            if course["courseState"] != "ACTIVE":
                continue

            # Get specific course's coursework
            course_id = course["id"]
            course_name = course["name"]

            coursework_items = service.courses().courseWork().list(
                courseId=course_id
            ).execute().get("courseWork", [])

            for item in coursework_items:
                coursework_id = item["id"]
                title = item.get("title", "Untitled")

                # Get the student's submission
                submission_list = service.courses().courseWork().studentSubmissions().list(
                    courseId=course_id,
                    courseWorkId=coursework_id
                ).execute().get("studentSubmissions", [])

                # load all the tasks
                for submission in submission_list:
                    if submission["state"] in ["CREATED", "NEW"]:
                        tasks.append({
                            "id": submission["id"],
                            "course": course_name,
                            "state": submission["state"],
                            "assignment": title,
                            "dueDate": item.get("dueDate", "No due date"),
                            "link": submission["alternateLink"]
                        })

        # check which if the tasks are already loaded to the database
        # update database real-time in parallel to local tasks
        for task in tasks:
            matched_task = db.query(ToDo).filter(
                ToDo.id == task["id"]
            ).first()

            # create new to-do list
            if matched_task is None:
                current_duedate = None
                if isinstance(task["dueDate"], dict):
                    current_duedate = date(
                        task["dueDate"]["year"],
                        task["dueDate"]["month"],
                        task["dueDate"]["day"]
                    )

                newly_created = ToDo(
                    id=task["id"],
                    course=task["course"],
                    task_name=task["assignment"],
                    status=task["state"],
                    due_date=current_duedate,
                    email=session.user_email,
                    link=task["link"]
                )

                db.add(newly_created)
                db.commit()
                db.refresh(newly_created)

            # refresh the status and dueDate if there's any changes
            else:
                current_duedate = None
                if isinstance(task["dueDate"], dict):
                    current_duedate = date(
                        task["dueDate"]["year"],
                        task["dueDate"]["month"],
                        task["dueDate"]["day"]
                    )

                matched_task.status = task["state"]
                matched_task.due_date = current_duedate
                matched_task.link = task["link"]

                db.commit()
                db.refresh(matched_task)

    finally:
        db.close()

def load_user_courses(auth_token: str):
    db = SessionLocal()
    session = db.query(Sessions).filter_by(
        auth_token=auth_token
    ).first()
    db.close()

    if not session:
        return {
            "message": "Unauthenticated"
        }

    creds = Credentials(
        token=session.access_token,
        refresh_token=session.refresh_token,
        token_uri=session.token_uri,
        client_id=session.client_id,
        client_secret=session.client_secret,
        scopes=session.scopes.split(",")
    )

    service = build("classroom", "v1", credentials=creds)
    courses = service.courses().list().execute()
    courses = courses.get("courses", [])

    for course in courses:
        if course.get("courseState") != "ACTIVE":
            continue

        matched_class = db.query(Classroom).filter(
            and_(
                Classroom.classid == course["id"],
                Classroom.owner == session.user_email
            )
        ).first()

        if matched_class is None:
            matched_class = Classroom(
                classid=course["id"],
                name=course.get("name"),
                room=course.get("room"),
                section=course.get("section"),
                courseState=course.get("courseState"),
                alternateLink=course.get("alternateLink"),
                messengerLink=None,
                owner=session.user_email,
            )

            db.add(matched_class)
            db.commit()
            db.refresh(matched_class)
        else:
            if course["courseState"] != "ACTIVE":
                db.query(Classroom).filter(
                    and_(
                        Classroom.classid == course["id"],
                        Classroom.owner == session.user_email
                    )
                ).delete()
                db.commit()


def get_latest_user_announcements(auth_token: str):
    db = SessionLocal()
    try:
        session = db.query(Sessions).filter(
            Sessions.auth_token == auth_token
        ).first()

        if session is None:
            return

        creds = Credentials(
            token=session.access_token,
            refresh_token=session.refresh_token,
            token_uri=session.token_uri,
            client_id=session.client_id,
            client_secret=session.client_secret,
            scopes=session.scopes.split(",")
        )

        current_user_courses = get_user_courses(auth_token)
        current_user_courses_ids = [course["classid"] for course in current_user_courses]

        service = build('classroom', 'v1', credentials=creds)
        course_announcement_latest = []
        for course_id in current_user_courses_ids:
            response = service.courses().announcements().list(
                courseId=course_id,
                orderBy='updateTime desc',
                pageSize=1
            ).execute()

            announcements = response.get('announcements', [])
            if announcements:
                course_announcement_latest.append({
                    "classid": course_id,
                    "latest_announcement": announcements[0]["id"]
                })

        return course_announcement_latest
    finally:
        db.close()


def get_latest_course_announcement(auth_token: str, course_id: str):
    db = SessionLocal()
    try:
        session = db.query(Sessions).filter(
            Sessions.auth_token == auth_token
        ).first()

        if session is None:
            return

        creds = Credentials(
            token=session.access_token,
            refresh_token=session.refresh_token,
            token_uri=session.token_uri,
            client_id=session.client_id,
            client_secret=session.client_secret,
            scopes=session.scopes.split(",")
        )

        service = build('classroom', 'v1', credentials=creds)
        response = service.courses().announcements().list(
            courseId=course_id,
            orderBy='updateTime desc',
            pageSize=1
        ).execute()

        announcements = response.get('announcements', [])
        if announcements:
            return { "classid": course_id, "latest_announcement": announcements[0]["id"] }
        return None

    finally:
        db.close()


def load_latest_user_announcements(auth_token: str):
    db = SessionLocal()
    try:
        session = db.query(Sessions).filter(
            Sessions.auth_token == auth_token
        ).first()

        if session is None:
            return

        course_latest_announcement = get_latest_user_announcements(
            auth_token
        )

        # match and load the current user's notifications
        for announce in course_latest_announcement:
            course = db.query(Notifications).filter(
                and_(
                    Notifications.owner == session.user_email,
                    Notifications.course_id == announce["classid"]
                )
            ).first()

            if course is not None:
                course.notification_id = announce["latest_announcement"]
                course.is_latest = True
                db.commit()
            else:
                course = Notifications(
                    owner=session.user_email,
                    course_id=announce["classid"],
                    notification_id=announce["latest_announcement"],
                    is_latest=True
                )

                db.add(course)

            db.commit()
            db.refresh(course)

    finally:
        db.close()

def watch_user_announcements(auth_token: str):
    db = SessionLocal()
    try:
        session = db.query(Sessions).filter(
            Sessions.auth_token == auth_token
        ).first()

        if session is None:
            return

        course_latest_announcement = get_latest_user_announcements(
            auth_token
        )

        # match and load the current user's notifications
        for announce in course_latest_announcement:
            course = db.query(Notifications).filter(
                and_(
                    Notifications.owner == session.user_email,
                    Notifications.course_id == announce["classid"]
                )
            ).first()

            if course is not None:
                if course.notification_id != announce["latest_announcement"]:
                    course.is_latest = False
                db.commit()
            else:
                course = Notifications(
                    owner=session.user_email,
                    course_id=announce["classid"],
                    notification_id=announce["latest_announcement"],
                    is_latest=False
                )

                db.add(course)

            db.commit()
            db.refresh(course)

    finally:
        db.close()


def get_unread_notifs(auth_token: str):
    db = SessionLocal()
    try:
        session = db.query(Sessions).filter(
            Sessions.auth_token == auth_token
        ).first()

        if session is None:
            return { "message": "Unauthenticated" }

        unsynced = db.query(Notifications).filter(
            and_(
                Notifications.owner == session.user_email,
                Notifications.is_latest == False,
            )
        ).all()
        return [model_to_dict(model) for model in unsynced]

    finally:
        db.close()


def mark_course_as_viewed(auth_token: str, course_id: str):
    db = SessionLocal()
    try:
        session = db.query(Sessions).filter(
            Sessions.auth_token == auth_token
        ).first()

        if session is None:
            return

        latest_course_announcement = get_latest_course_announcement(
            auth_token, course_id
        )

        notification = db.query(Notifications).filter(
            and_(
                Notifications.owner == session.user_email,
                Notifications.course_id == course_id
            )
        ).first()

        if latest_course_announcement is None or \
            notification is None:
            return

        notification.is_latest = True
        notification.notification_id = latest_course_announcement["latest_announcement"]
        return { "message": "Marked notification as viewed" }

    finally:
        db.close()

