from flask import Flask, send_from_directory
from backend.api.api import api_blueprint
from backend.database.connection import Engine
from backend.database.connection import Base
from backend.modules.background import start_background_tasks
from backend.config.appconfig import SQLITE_PATH
import os

app = Flask(__name__)


app.register_blueprint(api_blueprint)

@app.get("/")
def render_landing_page():
    return send_from_directory("templates", "index.html")

@app.get("/static/<path:path>")
def static_files_rendering(path):
    return send_from_directory("static", path)

@app.get("/<path:path>")
def render_html_templates(path):
    if not path.endswith(".html"):
        return send_from_directory("templates", path + ".html")
    return send_from_directory("templates", path)


if __name__ == '__main__':
    # checks first if the database is already created (load the database if not yet)
    if not os.path.isfile(SQLITE_PATH.replace("sqlite:///", "")):
        print("[*] Database does not exist yet... Creating...")
        from backend.database.models.sessions import Sessions
        from backend.database.models.assignments import ToDo
        from backend.database.models.classroom import Classroom
        Base.metadata.create_all(Engine)
        print("[+] Database created!")

    start_background_tasks()
    app.run(port=8000)
