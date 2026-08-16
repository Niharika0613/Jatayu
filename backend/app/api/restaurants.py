from flask import Blueprint, request, jsonify
from .. import db
from ..models import Restaurant
from ..utils.auth import admin_required

restaurants_bp = Blueprint("restaurants", __name__)


@restaurants_bp.route("/", methods=["GET"])
def list_restaurants():
    region = request.args.get("region", "")
    state = request.args.get("state", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 12))

    query = Restaurant.query.filter_by(status="approved")
    if region:
        query = query.filter(Restaurant.region.ilike(f"%{region}%"))
    if state:
        query = query.filter(Restaurant.state.ilike(f"%{state}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "restaurants": [r.to_dict() for r in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
    }), 200


@restaurants_bp.route("/<int:restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id):
    r = Restaurant.query.get_or_404(restaurant_id)
    return jsonify({"restaurant": r.to_dict()}), 200


@restaurants_bp.route("/", methods=["POST"])
def register_restaurant():
    """Public registration — goes into pending for admin approval."""
    data = request.get_json() or {}
    required = ["name", "region", "state", "contact_number"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"{f} is required"}), 400

    r = Restaurant(
        name=data["name"],
        owner_name=data.get("owner_name"),
        contact_number=data["contact_number"],
        email=data.get("email"),
        address=data.get("address"),
        village=data.get("village"),
        region=data["region"],
        state=data["state"],
        distance_from_trailhead_km=data.get("distance_from_trailhead_km"),
        type=data.get("type", "dhaba"),
        open_season=data.get("open_season"),
        accepts_upi=data.get("accepts_upi", True),
        accepts_cash=data.get("accepts_cash", True),
        cover_photo=data.get("cover_photo"),
        description=data.get("description"),
        speciality=data.get("speciality"),
        status="pending",
    )
    db.session.add(r)
    db.session.commit()
    return jsonify({"message": "Restaurant registered. Pending admin approval.", "id": r.id}), 201


@restaurants_bp.route("/<int:restaurant_id>/approve", methods=["POST"])
@admin_required
def approve(restaurant_id):
    r = Restaurant.query.get_or_404(restaurant_id)
    r.status = "approved"
    r.is_verified = True
    db.session.commit()
    return jsonify({"message": f"{r.name} approved"}), 200


@restaurants_bp.route("/<int:restaurant_id>/reject", methods=["POST"])
@admin_required
def reject(restaurant_id):
    r = Restaurant.query.get_or_404(restaurant_id)
    r.status = "rejected"
    db.session.commit()
    return jsonify({"message": f"{r.name} rejected"}), 200


@restaurants_bp.route("/<int:restaurant_id>", methods=["DELETE"])
@admin_required
def delete_restaurant(restaurant_id):
    r = Restaurant.query.get_or_404(restaurant_id)
    name = r.name
    db.session.delete(r)
    db.session.commit()
    return jsonify({"message": f"{name} deleted"}), 200
