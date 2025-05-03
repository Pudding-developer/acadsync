from flask import Flask, send_from_directory
from backend.api.api import api_blueprint

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
    app.run(debug=True, port=8000)
