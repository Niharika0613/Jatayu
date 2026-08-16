from flask import Blueprint, request, jsonify
from .. import cache
from ..models import LocalFood

food_bp = Blueprint("food", __name__)


@food_bp.route("/", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def list_food():
    region = request.args.get("region", "")
    state = request.args.get("state", "")
    category = request.args.get("category", "")
    veg_only = request.args.get("veg_only", "false").lower() == "true"

    query = LocalFood.query
    if region:
        query = query.filter(LocalFood.region.ilike(f"%{region}%"))
    if state:
        query = query.filter(LocalFood.state.ilike(f"%{state}%"))
    if category:
        query = query.filter(LocalFood.category == category)
    if veg_only:
        query = query.filter(LocalFood.is_vegetarian == True)

    food = query.all()
    return jsonify({"food": [f.to_dict() for f in food], "total": len(food)}), 200


@food_bp.route("/region/<string:region>", methods=["GET"])
@cache.cached(timeout=300)
def food_by_region(region):
    food = LocalFood.query.filter(LocalFood.region.ilike(f"%{region}%")).all()
    return jsonify({"food": [f.to_dict() for f in food], "region": region}), 200
