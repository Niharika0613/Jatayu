from flask import Blueprint, request, jsonify
from .. import db
from ..models import TravelAgency
from ..utils.auth import admin_required

agencies_bp = Blueprint("agencies", __name__)


@agencies_bp.route("/", methods=["GET"])
def list_agencies():
    region = request.args.get("region", "")
    state = request.args.get("state", "")
    service = request.args.get("service", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 9))

    query = TravelAgency.query.filter_by(status="approved")
    if region:
        query = query.filter(TravelAgency.regions_covered.ilike(f"%{region}%"))
    if state:
        query = query.filter(TravelAgency.state.ilike(f"%{state}%"))
    if service:
        query = query.filter(TravelAgency.services.ilike(f"%{service}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "agencies": [a.to_dict() for a in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
    }), 200


@agencies_bp.route("/<int:agency_id>", methods=["GET"])
def get_agency(agency_id):
    a = TravelAgency.query.get_or_404(agency_id)
    return jsonify({"agency": a.to_dict()}), 200


@agencies_bp.route("/", methods=["POST"])
def register_agency():
    data = request.get_json() or {}
    required = ["name", "state", "contact_number", "services"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"{f} is required"}), 400

    a = TravelAgency(
        name=data["name"],
        owner_name=data.get("owner_name"),
        contact_number=data["contact_number"],
        email=data.get("email"),
        website=data.get("website"),
        base_city=data.get("base_city"),
        state=data["state"],
        regions_covered=data.get("regions_covered"),
        services=data["services"],
        certifications=data.get("certifications"),
        year_founded=data.get("year_founded"),
        vehicle_types=data.get("vehicle_types"),
        max_group_size=data.get("max_group_size"),
        offers_insurance=data.get("offers_insurance", False),
        insurance_details=data.get("insurance_details"),
        pricing_tier=data.get("pricing_tier"),
        package_starting_price_inr=data.get("package_starting_price_inr"),
        description=data.get("description"),
        cover_photo=data.get("cover_photo"),
        status="pending",
    )
    db.session.add(a)
    db.session.commit()
    return jsonify({"message": "Agency registered. Pending admin approval.", "id": a.id}), 201


@agencies_bp.route("/<int:agency_id>/approve", methods=["POST"])
@admin_required
def approve(agency_id):
    a = TravelAgency.query.get_or_404(agency_id)
    a.status = "approved"
    a.is_verified = True
    db.session.commit()
    return jsonify({"message": f"{a.name} approved"}), 200


@agencies_bp.route("/<int:agency_id>/reject", methods=["POST"])
@admin_required
def reject(agency_id):
    a = TravelAgency.query.get_or_404(agency_id)
    a.status = "rejected"
    db.session.commit()
    return jsonify({"message": f"{a.name} rejected"}), 200


@agencies_bp.route("/<int:agency_id>", methods=["DELETE"])
@admin_required
def delete_agency(agency_id):
    a = TravelAgency.query.get_or_404(agency_id)
    name = a.name
    db.session.delete(a)
    db.session.commit()
    return jsonify({"message": f"{name} deleted"}), 200
