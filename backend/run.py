import os
from app import create_app, celery

env = os.environ.get("FLASK_ENV", "development")
app = create_app(env)

if __name__ == "__main__":
    app.run(debug=(env == "development"), port=5000)
