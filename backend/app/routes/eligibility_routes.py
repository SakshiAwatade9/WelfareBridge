from flask import Blueprint, jsonify
from ..models import User, Scheme, SavedScheme
from ..decorators import roles_required, current_user_id
from ..eligibility import evaluate_scheme

eligibility_bp = Blueprint("eligibility", __name__, url_prefix="/api/eligibility")


@eligibility_bp.route("/check", methods=["GET"])
@roles_required("USER", "ADMIN")
def check_all():
    user = User.query.get(current_user_id())

    if not user.profile:
        return jsonify({"message": "Complete the eligibility questionnaire first by submitting PUT /api/profile."}), 400

    saved_ids = {s.scheme_id for s in user.saved_schemes}

    results = []
    for scheme in Scheme.query.all():
        r = evaluate_scheme(user.profile, scheme)
        r["saved"] = scheme.id in saved_ids
        results.append(r)

    results.sort(key=lambda r: r["matchPercent"], reverse=True)
    return jsonify(results)


@eligibility_bp.route("/check/<int:scheme_id>", methods=["GET"])
@roles_required("USER", "ADMIN")
def check_one(scheme_id):
    user = User.query.get(current_user_id())

    if not user.profile:
        return jsonify({"message": "Complete the eligibility questionnaire first by submitting PUT /api/profile."}), 400

    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return jsonify({"message": "Scheme not found."}), 404

    saved = SavedScheme.query.filter_by(user_id=user.id, scheme_id=scheme_id).first() is not None
    r = evaluate_scheme(user.profile, scheme)
    r["saved"] = saved
    return jsonify(r)
