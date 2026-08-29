from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import User, UserProfile
from ..decorators import roles_required, current_user_id

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.route("", methods=["GET"])
@roles_required("USER", "ADMIN")
def get_profile():
    user = User.query.get(current_user_id())
    if not user.profile:
        return jsonify({"message": "No profile found for this account yet."}), 404

    result = user.profile.to_dict()
    result["name"] = user.name
    return jsonify(result)


@profile_bp.route("", methods=["PUT"])
@roles_required("USER", "ADMIN")
def save_profile():
    data = request.get_json(silent=True) or {}

    age = data.get("age")
    gender = data.get("gender")
    state = data.get("state")
    income = data.get("income")
    occupation = data.get("occupation")

    if age is None or not gender or not state or income is None or not occupation:
        return jsonify({"message": "Please complete all fields before continuing."}), 400

    user = User.query.get(current_user_id())
    profile = user.profile or UserProfile(user_id=user.id)

    profile.age = int(age)
    profile.gender = gender
    profile.state = state
    profile.income = int(income)
    profile.occupation = occupation

    db.session.add(profile)
    db.session.commit()

    result = profile.to_dict()
    result["name"] = user.name
    return jsonify(result)
