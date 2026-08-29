from flask import Blueprint, jsonify
from ..models import Scheme

scheme_bp = Blueprint("schemes", __name__, url_prefix="/api/schemes")


@scheme_bp.route("", methods=["GET"])
def list_schemes():
    schemes = Scheme.query.all()
    return jsonify([s.to_dict() for s in schemes])


@scheme_bp.route("/<int:scheme_id>", methods=["GET"])
def get_scheme(scheme_id):
    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return jsonify({"message": "Scheme not found."}), 404
    return jsonify(scheme.to_dict())
