from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return check_password_hash(hashed, plain)


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))


# ── Role decorators ────────────────────────────────────────────────

def role_required(*roles):
    """Generic role guard. Usage: @role_required('admin') or @role_required('admin','staff')"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user = get_current_user()
            if not user:
                return jsonify({"error": "User not found"}), 404
            if user.status == "blacklisted":
                return jsonify({"error": "Your account has been blacklisted"}), 403
            if not user.is_active:
                return jsonify({"error": "Your account is inactive"}), 403
            if user.role not in roles:
                return jsonify({"error": "Access denied. Insufficient permissions."}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(fn):
    return role_required("admin")(fn)


def staff_required(fn):
    return role_required("staff")(fn)


def trekker_required(fn):
    return role_required("trekker")(fn)


def staff_or_admin_required(fn):
    return role_required("admin", "staff")(fn)


def any_role_required(fn):
    return role_required("admin", "staff", "trekker")(fn)
