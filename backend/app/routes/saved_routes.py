from flask import Blueprint, jsonify
from ..extensions import db
from ..models import User, Scheme, SavedScheme
from ..decorators import roles_required, current_user_id

saved_bp = Blueprint("saved", __name__, url_prefix="/api/saved")


@saved_bp.route("", methods=["GET"])
@roles_required("USER", "ADMIN")
def list_saved():
    user = User.query.get(current_user_id())
    results = []
    for s in user.saved_schemes:
        d = s.scheme.to_dict()
        d["saved"] = True
        results.append(d)
    return jsonify(results)


@saved_bp.route("/<int:scheme_id>", methods=["POST"])
@roles_required("USER", "ADMIN")
def save_scheme(scheme_id):
    user_id = current_user_id()

    existing = SavedScheme.query.filter_by(user_id=user_id, scheme_id=scheme_id).first()
    if existing:
        return jsonify({"message": "Already saved."})

    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return jsonify({"message": "Scheme not found."}), 404

    db.session.add(SavedScheme(user_id=user_id, scheme_id=scheme_id))
    db.session.commit()
    return jsonify({"message": "Saved to your list."})


@saved_bp.route("/<int:scheme_id>", methods=["DELETE"])
@roles_required("USER", "ADMIN")
def unsave_scheme(scheme_id):
    user_id = current_user_id()
    SavedScheme.query.filter_by(user_id=user_id, scheme_id=scheme_id).delete()
    db.session.commit()
    return jsonify({"message": "Removed from saved schemes."})
