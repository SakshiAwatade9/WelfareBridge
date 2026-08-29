from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity


def roles_required(*allowed_roles):
    """
    Decorator that requires a valid JWT AND that the token's role claim is one of allowed_roles.
    Usage: @roles_required("ADMIN")  or  @roles_required("USER", "ADMIN")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            if role not in allowed_roles:
                return jsonify({"message": "You do not have permission to perform this action."}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def current_user_id():
    """Call only inside a route already guarded by roles_required or verify_jwt_in_request."""
    return int(get_jwt_identity())
