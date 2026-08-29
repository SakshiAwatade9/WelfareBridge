from flask import Blueprint, request, jsonify
from sqlalchemy import func
from ..extensions import db
from ..models import User, Scheme, SavedScheme
from ..decorators import roles_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/schemes", methods=["POST"])
@roles_required("ADMIN")
def create_scheme():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    department = (data.get("department") or "").strip()
    benefit = (data.get("benefit") or "").strip()

    if not name or not department or not benefit:
        return jsonify({"message": "Please fill in at least the name, department, and benefit."}), 400

    scheme = Scheme(
        name=name,
        department=department,
        category=data.get("category") or "Education",
        benefit=benefit,
        description=data.get("description") or "",
        min_age=data.get("minAge"),
        max_age=data.get("maxAge"),
        max_income=data.get("maxIncome"),
        state=data.get("state") or "All India",
        occupation=data.get("occupation") or "any",
        gender=data.get("gender") or "any",
        senior_only=bool(data.get("seniorOnly")),
        deadline=data.get("deadline") or "Open year-round",
        apply_link=data.get("applyLink") or "#",
    )
    scheme.set_documents_list(data.get("documents") or [])

    db.session.add(scheme)
    db.session.commit()
    return jsonify(scheme.to_dict())


@admin_bp.route("/schemes/<int:scheme_id>", methods=["PUT"])
@roles_required("ADMIN")
def update_scheme(scheme_id):
    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return jsonify({"message": "Scheme not found."}), 404

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    department = (data.get("department") or "").strip()
    benefit = (data.get("benefit") or "").strip()

    if not name or not department or not benefit:
        return jsonify({"message": "Please fill in at least the name, department, and benefit."}), 400

    scheme.name = name
    scheme.department = department
    scheme.category = data.get("category") or "Education"
    scheme.benefit = benefit
    scheme.description = data.get("description") or ""
    scheme.min_age = data.get("minAge")
    scheme.max_age = data.get("maxAge")
    scheme.max_income = data.get("maxIncome")
    scheme.state = data.get("state") or "All India"
    scheme.occupation = data.get("occupation") or "any"
    scheme.gender = data.get("gender") or "any"
    scheme.senior_only = bool(data.get("seniorOnly"))
    scheme.deadline = data.get("deadline") or "Open year-round"
    scheme.apply_link = data.get("applyLink") or "#"
    scheme.set_documents_list(data.get("documents") or [])

    db.session.commit()
    return jsonify(scheme.to_dict())


@admin_bp.route("/schemes/<int:scheme_id>", methods=["DELETE"])
@roles_required("ADMIN")
def delete_scheme(scheme_id):
    scheme = Scheme.query.get(scheme_id)
    if not scheme:
        return jsonify({"message": "Scheme not found."}), 404
    db.session.delete(scheme)
    db.session.commit()
    return jsonify({"message": "Scheme removed from the catalogue."})


@admin_bp.route("/stats", methods=["GET"])
@roles_required("ADMIN")
def stats():
    total_schemes = Scheme.query.count()
    total_citizens = User.query.filter_by(role="USER").count()
    total_saves = SavedScheme.query.count()

    by_category_rows = (
        db.session.query(Scheme.category, func.count(Scheme.id))
        .group_by(Scheme.category)
        .all()
    )
    by_category = {category: count for category, count in by_category_rows}

    return jsonify({
        "totalSchemes": total_schemes,
        "totalCitizens": total_citizens,
        "totalSaves": total_saves,
        "byCategory": by_category,
    })
