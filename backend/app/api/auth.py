from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from werkzeug.security import check_password_hash
from .. import db
from ..models import User
from ..utils.auth import hash_password, get_current_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    if user.status == "blacklisted":
        return jsonify({"error": "Your account has been blacklisted. Contact support."}), 403

    if not user.is_active:
        return jsonify({"error": "Your account is inactive. Contact admin."}), 403

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict(),
    }), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    """Only trekkers can self-register."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["full_name", "email", "password", "confirm_password", "contact_number"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    if data["password"] != data["confirm_password"]:
        return jsonify({"error": "Passwords do not match"}), 400

    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    email = data["email"].strip().lower()
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(
        role="trekker",
        full_name=data["full_name"].strip(),
        email=email,
        password_hash=hash_password(data["password"]),
        contact_number=data.get("contact_number", "").strip(),
        status="active",
        is_active=True,
        # Jatayu extras (optional at registration)
        state=data.get("state"),
        home_city=data.get("home_city"),
        experience_level=data.get("experience_level"),
        blood_group=data.get("blood_group"),
        emergency_contact_name=data.get("emergency_contact_name"),
        emergency_contact_number=data.get("emergency_contact_number"),
    )

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "message": "Registration successful. Welcome to Jatayu!",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict(),
    }), 201


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user.to_dict()}), 200


@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}

    updatable = [
        "full_name", "contact_number", "state", "home_city",
        "experience_level", "blood_group", "emergency_contact_name",
        "emergency_contact_number",
    ]
    for field in updatable:
        if field in data:
            setattr(user, field, data[field])

    # Password change (optional)
    if data.get("new_password"):
        if not data.get("current_password"):
            return jsonify({"error": "Current password required"}), 400
        if not check_password_hash(user.password_hash, data["current_password"]):
            return jsonify({"error": "Current password incorrect"}), 401
        user.password_hash = hash_password(data["new_password"])

    db.session.commit()
    return jsonify({"message": "Profile updated", "user": user.to_dict()}), 200
