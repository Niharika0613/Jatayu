from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS
from celery import Celery
import os

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
celery = Celery()


def create_app(config_name="development"):
    is_prod = os.environ.get("FLASK_ENV") == "production" or config_name == "production"
    if is_prod:
        app = Flask(__name__,
                    static_folder="../../frontend/dist",
                    static_url_path="/")
    else:
        app = Flask(__name__, template_folder="../../templates")
        
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        imports=("app.jobs.tasks",),
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    from .api.auth import auth_bp
    from .api.admin import admin_bp
    from .api.staff import staff_bp
    from .api.user import user_bp
    from .api.treks import treks_bp
    from .api.restaurants import restaurants_bp
    from .api.agencies import agencies_bp
    from .api.food import food_bp
    from .api.reviews import reviews_bp
    from .api.index import index_bp

    app.register_blueprint(auth_bp,        url_prefix="/api/auth")
    app.register_blueprint(admin_bp,       url_prefix="/api/admin")
    app.register_blueprint(staff_bp,       url_prefix="/api/staff")
    app.register_blueprint(user_bp,        url_prefix="/api/user")
    app.register_blueprint(treks_bp,       url_prefix="/api/treks")
    app.register_blueprint(restaurants_bp, url_prefix="/api/restaurants")
    app.register_blueprint(agencies_bp,    url_prefix="/api/agencies")
    app.register_blueprint(food_bp,        url_prefix="/api/food")
    app.register_blueprint(reviews_bp,     url_prefix="/api")
    app.register_blueprint(index_bp)

    with app.app_context():
        from .models import User, Trek, Booking, Restaurant, LocalFood, TravelAgency
        db.create_all()

    return app
