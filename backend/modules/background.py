from backend.modules.google import load_users_tasks
from backend.modules.google import load_user_courses
from backend.database.connection import SessionLocal
from backend.database.models.sessions import Sessions
from backend.database.models.assignments import ToDo
from threading import Thread
import time

# this syncs the task status for the user
def sync_user_courses():
    db = SessionLocal()
    try:

        while True:
            sessions = db.query(Sessions).all()
            print("[*] Re-Syncing user tasks locally...")

            for sess in sessions:
                print("[+] Reloaded tasks for user:", sess.user_email)
                load_users_tasks(sess.auth_token)
            print("[*] Done resyncing batch")
            time.sleep(10)
    finally:
        db.close()

# syncs the current classrooms of the user
def sync_user_classrooms():
    db = SessionLocal()
    try:

        while True:
            sessions = db.query(Sessions).all()
            print("[*] Re-Syncing user classrooms locally...")

            for sess in sessions:
                print("[+] Reloaded classes for user:", sess.user_email)
                load_user_courses(sess.auth_token)
            print("[*] Done resyncing batch")
            time.sleep(23)
    finally:
        db.close()

def start_background_tasks():
    print("[*] Starting background tasks...")
    th1 = Thread(target=sync_user_courses)
    th2 = Thread(target=sync_user_classrooms)

    th1.start()
    th2.start()
