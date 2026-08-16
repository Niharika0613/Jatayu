from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from .. import db, cache, cache, cache, cache, cache, cache
from ..models import Trek, Booking, User, TravelAgency
from ..utils.auth import trekker_required, get_current_user

user_bp = Blueprint("user", __name__)


@user_bp.route("/dashboard", methods=["GET"])
@trekker_required
def dashboard():
    user = get_current_user()
    bookings = Booking.query.filter_by(user_id=user.id).order_by(
        Booking.created_at.desc()
    ).limit(5).all()
    open_treks = Trek.query.filter_by(status="Open").order_by(
        Trek.start_date.asc()
    ).limit(6).all()

    return jsonify({
        "user": user.to_dict(),
        "recent_bookings": [b.to_dict() for b in bookings],
        "available_treks": [t.to_dict() for t in open_treks],
    }), 200


@user_bp.route("/bookings", methods=["GET"])
@trekker_required
def my_bookings():
    user = get_current_user()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    pagination = Booking.query.filter_by(user_id=user.id).order_by(
        Booking.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "bookings": [b.to_dict() for b in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": page,
    }), 200


@user_bp.route("/bookings", methods=["POST"])
@trekker_required
def book_trek():
    user = get_current_user()
    data = request.get_json() or {}

    trek_id = data.get("trek_id")
    if not trek_id:
        return jsonify({"error": "trek_id is required"}), 400

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    if trek.status != "Open":
        return jsonify({"error": "This trek is not open for booking"}), 400

    if trek.available_slots <= 0:
        return jsonify({"error": "No slots available"}), 400

    # No duplicate bookings
    existing = Booking.query.filter_by(
        user_id=user.id, trek_id=trek_id
    ).filter(Booking.status != "Cancelled").first()
    if existing:
        return jsonify({"error": "You have already booked this trek"}), 409

    # Calculate amount paid and validate agency if provided
    agency_id = data.get("travel_agency_id")
    final_price = trek.price_inr
    
    if agency_id:
        agency = TravelAgency.query.get(agency_id)
        if not agency or agency.status != "approved":
            return jsonify({"error": "Selected travel agency is invalid or not approved"}), 400
        if agency.package_starting_price_inr:
            final_price = agency.package_starting_price_inr

    booking = Booking(
        user_id=user.id,
        trek_id=trek_id,
        travel_agency_id=agency_id,
        status="Booked",
        payment_status="Paid",  # simulated
        amount_paid=final_price,
        payment_method="Simulated",
        confirmed_at=datetime.utcnow(),
    )

    trek.available_slots -= 1
    if trek.available_slots == 0:
        trek.status = "Closed"

    db.session.add(booking)
    db.session.commit()
    cache.clear()
    cache.clear()
    cache.clear()
    cache.clear()
    cache.clear()
    cache.clear()

    return jsonify({
        "message": f"Successfully booked {trek.name}!",
        "booking": booking.to_dict(),
    }), 201


@user_bp.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
@trekker_required
def cancel_booking(booking_id):
    user = get_current_user()
    booking = Booking.query.filter_by(id=booking_id, user_id=user.id).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking.status != "Booked":
        return jsonify({"error": "Only active bookings can be cancelled"}), 400

    data = request.get_json() or {}
    booking.status = "Cancelled"
    booking.cancelled_at = datetime.utcnow()
    booking.cancellation_reason = data.get("reason", "Cancelled by user")
    booking.payment_status = "Refunded"

    # Restore slot
    trek = Trek.query.get(booking.trek_id)
    if trek and trek.status in ["Open", "Closed"]:
        trek.available_slots += 1
        if trek.status == "Closed":
            trek.status = "Open"

    db.session.commit()
    cache.clear()
    return jsonify({"message": "Booking cancelled successfully"}), 200


@user_bp.route("/history", methods=["GET"])
@trekker_required
def history():
    """Completed and cancelled bookings — wireframe screen 12."""
    user = get_current_user()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    pagination = Booking.query.filter_by(user_id=user.id).filter(
        Booking.status.in_(["Completed", "Cancelled"])
    ).order_by(Booking.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        "history": [b.to_dict() for b in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": page,
    }), 200


@user_bp.route("/export-history", methods=["POST"])
@trekker_required
def export_history():
    """Trigger async CSV export via Celery."""
    from ..jobs.tasks import export_booking_history
    user = get_current_user()
    task = export_booking_history.delay(user.id)
    return jsonify({
        "message": "Export started. You will be notified when ready.",
        "task_id": task.id,
    }), 202


@user_bp.route("/profile", methods=["GET"])
@trekker_required
def profile():
    user = get_current_user()
    return jsonify({"user": user.to_dict()}), 200
