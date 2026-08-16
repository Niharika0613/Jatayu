from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .. import db, cache, cache, cache, cache, cache, cache
from ..models import Trek, Booking, User
from ..utils.auth import staff_required, get_current_user

staff_bp = Blueprint("staff", __name__)


@staff_bp.route("/dashboard", methods=["GET"])
@staff_required
def dashboard():
    staff = get_current_user()
    assigned = Trek.query.filter_by(staff_id=staff.id).all()
    ongoing = [t for t in assigned if t.status == "Open"]

    total_participants = 0
    for trek in assigned:
        total_participants += Booking.query.filter_by(
            trek_id=trek.id, status="Booked"
        ).count()

    return jsonify({
        "stats": {
            "assigned_treks": len(assigned),
            "total_participants": total_participants,
            "ongoing_treks": len(ongoing),
        },
        "assigned_treks": [t.to_dict() for t in assigned],
    }), 200


@staff_bp.route("/treks", methods=["GET"])
@staff_required
def my_treks():
    staff = get_current_user()
    treks = Trek.query.filter_by(staff_id=staff.id).all()
    return jsonify({"treks": [t.to_dict() for t in treks]}), 200


@staff_bp.route("/treks/<int:trek_id>", methods=["GET"])
@staff_required
def get_trek(trek_id):
    staff = get_current_user()
    trek = Trek.query.filter_by(id=trek_id, staff_id=staff.id).first()
    if not trek:
        return jsonify({"error": "Trek not found or not assigned to you"}), 404

    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    return jsonify({
        "trek": trek.to_dict(),
        "participants": [b.to_dict() for b in bookings],
        "participant_count": len(bookings),
    }), 200


@staff_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@staff_required
def update_trek(trek_id):
    """Staff can only update available_slots and status."""
    staff = get_current_user()
    trek = Trek.query.filter_by(id=trek_id, staff_id=staff.id).first()
    if not trek:
        return jsonify({"error": "Trek not found or not assigned to you"}), 404

    data = request.get_json() or {}

    if "available_slots" in data:
        slots = int(data["available_slots"])
        if slots < 0 or slots > trek.total_slots:
            return jsonify({"error": "Invalid slot count"}), 400
        trek.available_slots = slots

    if "status" in data:
        allowed = ["Open", "Closed", "Completed"]
        if data["status"] not in allowed:
            return jsonify({"error": f"Status must be one of {allowed}"}), 400
        trek.status = data["status"]

        # When completing — mark all active bookings as completed
        if data["status"] == "Completed":
            Booking.query.filter_by(
                trek_id=trek_id, status="Booked"
            ).update({"status": "Completed"})

    db.session.commit()
    cache.clear()
    return jsonify({"message": "Trek updated", "trek": trek.to_dict()}), 200


@staff_bp.route("/treks/<int:trek_id>/complete", methods=["POST"])
@staff_required
def mark_completed(trek_id):
    staff = get_current_user()
    trek = Trek.query.filter_by(id=trek_id, staff_id=staff.id).first()
    if not trek:
        return jsonify({"error": "Trek not found or not assigned to you"}), 404

    trek.status = "Completed"
    Booking.query.filter_by(trek_id=trek_id, status="Booked").update({"status": "Completed"})
    db.session.commit()
    cache.clear()
    return jsonify({"message": f"{trek.name} marked as completed"}), 200


@staff_bp.route("/treks/<int:trek_id>/participants", methods=["GET"])
@staff_required
def participants(trek_id):
    staff = get_current_user()
    trek = Trek.query.filter_by(id=trek_id, staff_id=staff.id).first()
    if not trek:
        return jsonify({"error": "Trek not found or not assigned to you"}), 404

    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    return jsonify({
        "trek_name": trek.name,
        "participants": [b.to_dict() for b in bookings],
        "total": len(bookings),
    }), 200


@staff_bp.route("/participants", methods=["GET"])
@staff_required
def all_participants():
    staff = get_current_user()
    assigned_treks = Trek.query.filter_by(staff_id=staff.id).all()
    trek_ids = [t.id for t in assigned_treks]

    bookings = Booking.query.filter(Booking.trek_id.in_(trek_ids)).all() if trek_ids else []
    return jsonify({
        "participants": [b.to_dict() for b in bookings],
        "total": len(bookings),
    }), 200


@staff_bp.route("/profile", methods=["GET"])
@staff_required
def profile():
    staff = get_current_user()
    return jsonify({"staff": staff.to_dict()}), 200
