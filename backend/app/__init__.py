from flask import Flask, jsonify
from .config import Config
from .extensions import db, bcrypt, jwt, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})

    from .routes.auth_routes import auth_bp
    from .routes.profile_routes import profile_bp
    from .routes.scheme_routes import scheme_bp
    from .routes.eligibility_routes import eligibility_bp
    from .routes.saved_routes import saved_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(scheme_bp)
    app.register_blueprint(eligibility_bp)
    app.register_blueprint(saved_bp)
    app.register_blueprint(admin_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "WelfareBridge API"})

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Your session has expired. Please log in again."}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"message": "Invalid authentication token."}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return jsonify({"message": "Authentication required."}), 401

    with app.app_context():
        db.create_all()
        from .seed import run_seed
        run_seed()

    return app
