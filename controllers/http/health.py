from flask import Blueprint, current_app, jsonify

health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/healthz", methods=["GET"])
def liveness():
    """Liveness probe returning 200 if the HTTP worker process is alive."""
    return jsonify({"status": "ok"}), 200


@health_blueprint.route("/readyz", methods=["GET"])
def readiness():
    """Readiness probe checking database and Keycloak dependencies."""
    db_status = "up"
    auth_status = "up"
    status_code = 200

    try:
        db_manager = current_app.extensions.get("db_manager")
        if db_manager:
            db_manager.check_connection()
    except Exception:
        db_status = "down"
        status_code = 503

    try:
        auth_controller = getattr(current_app, "_authController", None)
        if auth_controller:
            auth_controller.check_connection()
    except Exception:
        auth_status = "down"
        status_code = 503

    return (
        jsonify(
            {
                "status": "ready" if status_code == 200 else "unhealthy",
                "database": db_status,
                "auth": auth_status,
            }
        ),
        status_code,
    )
