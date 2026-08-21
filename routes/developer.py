# ==========================================
# IMPORT
# ==========================================

import os
import joblib

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    current_app
)

from services.prediction_service import PredictionService


# ==========================================
# BLUEPRINT
# ==========================================

developer_bp = Blueprint(
    "developer",
    __name__,
    url_prefix="/developer"
)


# ==========================================
# CHECK DEVELOPER
# ==========================================

def check_developer():

    if "user" not in session:
        return redirect(
            url_for("auth.login")
        )

    if session.get("role") != "Developer":
        return redirect(
            url_for("dashboard.dashboard")
        )

    return None


# ==========================================
# DEVELOPER DASHBOARD
# ==========================================

@developer_bp.route("/")
def dashboard():

    access_error = check_developer()

    if access_error:
        return access_error

    # --------------------------------------
    # SYSTEM STATISTICS
    # --------------------------------------

    system_stats = (
        PredictionService
        .get_system_statistics()
    )

    return render_template(

        "developer/dashboard.html",

        user=session.get("user"),

        role=session.get("role"),

        total_predictions=(
            system_stats["total_predictions"]
        ),

        average_rating=(
            system_stats["average_rating"]
        ),

        accuracy=(
            system_stats["accuracy"]
        ),

        total_users=(
            system_stats["total_users"]
        ),

        total_admins=(
            system_stats["total_admins"]
        ),

        total_developers=(
            system_stats["total_developers"]
        ),

        total_normal_users=(
            system_stats["total_normal_users"]
        )
    )

# ==========================================
# DEVELOPER MODEL
# ==========================================

@developer_bp.route("/model")
def model():

    access_error = check_developer()

    if access_error:
        return access_error

    model_path = os.path.join(
        current_app.root_path,
        "models",
        "random_forest_model.pkl"
    )

    model_exists = os.path.exists(
        model_path
    )

    model_info = None

    if model_exists:

        try:

            trained_model = joblib.load(
                model_path
            )

            model_info = {
                "type": type(
                    trained_model
                ).__name__,

                "n_estimators": getattr(
                    trained_model,
                    "n_estimators",
                    "N/A"
                ),

                "random_state": getattr(
                    trained_model,
                    "random_state",
                    "N/A"
                )
            }

        except Exception as err:

            print(
                f"Lỗi đọc model: {err}"
            )

            model_exists = False

    return render_template(
        "developer/model.html",

        user=session.get("user"),

        role=session.get("role"),

        model_exists=model_exists,

        model_info=model_info
    )


# ==========================================
# DEVELOPER REPORTS
# ==========================================

@developer_bp.route("/reports")
def reports():

    access_error = check_developer()

    if access_error:
        return access_error

    return render_template(
        "developer/reports.html",

        user=session.get("user"),

        role=session.get("role")
    )