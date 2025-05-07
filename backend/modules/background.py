from backend.modules.google import load_users_tasks
from backend.modules.google import load_user_courses
from backend.modules.google import load_latest_user_announcements
from backend.modules.google import watch_user_announcements
from backend.database.connection import SessionLocal
from backend.database.models.sessions import Sessions
from backend.database.models.assignments import ToDo
from threading import Thread
import time

# first time pull latest notification
def initial_user_notification():
    db = SessionLocal()
    sessions = db.query(Sessions).all()
    print("[*] Syncing notifications locally...")
    for sess in sessions:
        load_latest_user_announcements(sess.auth_token)
    print("[+] Done Syncing notifications locally")

    # start looping through for latest announcements
    db.close()

    while True:
        print("[*] Watching and syncing user unread announcements")
        for sess in sessions:
            print("[+] Watching announcements for user:", sess.user_email)
            watch_user_announcements(sess.access_token)
            time.sleep(4)

# this syncs the task status for the user
def sync_user_courses():
    while True:
        db = SessionLocal()
        try:
            sessions = db.query(Sessions).all()
            print("[*] Re-Syncing user tasks locally...")

            for sess in sessions:
                print("[+] Reloaded tasks for user:", sess.user_email)
                load_users_tasks(sess.auth_token)
            print("[*] Done resyncing batch")
            time.sleep(5)
        finally:
            db.close()

# syncs the current classrooms of the user
def sync_user_classrooms():
    while True:
        db = SessionLocal()
        try:
            sessions = db.query(Sessions).all()
            print("[*] Re-Syncing user classrooms locally...")

            for sess in sessions:
                print("[+] Reloaded classes for user:", sess.user_email)
                load_user_courses(sess.auth_token)
            print("[*] Done resyncing batch")
            time.sleep(3)
        finally:
            db.close()

def start_background_tasks():
    print("[*] Starting background tasks...")
    th1 = Thread(target=sync_user_courses)
    th2 = Thread(target=sync_user_classrooms)
    th3 = Thread(target=initial_user_notification)

    th3.start()
    th1.start()
    th2.start()
