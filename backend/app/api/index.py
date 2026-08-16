from flask import Blueprint, render_template_string, send_from_directory, current_app
import os

index_bp = Blueprint("index", __name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Jatayu — India's Trekking Soul</title>
  <link rel="icon" href="/static/favicon.ico"/>
  <link rel="stylesheet" href="/static/css/app.css"/>
</head>
<body>
  <div id="app"></div>
  <script src="/static/js/app.js"></script>
</body>
</html>"""


@index_bp.route("/", defaults={"path": ""})
@index_bp.route("/<path:path>")
def catch_all(path):
    is_prod = os.environ.get("FLASK_ENV") == "production" or current_app.config.get("ENV") == "production"
    if is_prod and current_app.static_folder and os.path.exists(os.path.join(current_app.static_folder, "index.html")):
        return send_from_directory(current_app.static_folder, "index.html")
    return render_template_string(HTML)
