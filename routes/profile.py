# ==========================================
# IMPORT
# ==========================================

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)


# ==========================================
# BLUEPRINT
# ==========================================

profile_bp = Blueprint(
    "profile",
    __name__
)


# ==========================================
# PROFILE
# ==========================================

@profile_bp.route("/profile")
def profile():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "user/profile.html",
        user=session.get("user"),
        role=session.get("role")
    )