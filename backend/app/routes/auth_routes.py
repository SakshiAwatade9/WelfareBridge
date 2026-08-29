from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..extensions import db, bcrypt
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = (data.get("role") or "USER").upper()

    if not name or not email or not password:
        return jsonify({"message": "Please fill in all fields."}), 400
    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters."}), 400
    if role not in ("USER", "ADMIN"):
        role = "USER"

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "An account already exists with this email."}), 400

    user = User(
        name=name,
        email=email,
        password_hash=bcrypt.generate_password_hash(password).decode("utf-8"),
        role=role,
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role, "email": user.email})
    return jsonify({
        "token": token,
        "userId": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    })


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "No matching account found."}), 401

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role, "email": user.email})
    return jsonify({
        "token": token,
        "userId": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    })
