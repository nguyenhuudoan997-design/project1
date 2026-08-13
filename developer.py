from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for


# ==========================================
# BLUEPRINT
# ==========================================

developer_bp = Blueprint(
    "developer",
    __name__,
    url_prefix="/developer"
)


# ==========================================
# DEVELOPER DASHBOARD
# ==========================================

@developer_bp.route("/")
def dashboard():

    # ------------------------------
    # Kiểm tra đăng nhập
    # ------------------------------

    if "user" not in session:

        return redirect(
            url_for("auth.login")
        )

    # ------------------------------
    # Kiểm tra Developer
    # ------------------------------

    if session.get("role") != "Developer":

        return redirect(
            url_for("auth.login")
        )

    # ------------------------------
    # Dashboard
    # ------------------------------

    return render_template(
        "developer/dashboard.html",
        user=session.get("user"),
        role=session.get("role")
    )