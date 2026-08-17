from flask import Blueprint, render_template, session


profile_bp = Blueprint(
    "profile",
    __name__
)


@profile_bp.route("/profile")
def profile():

    username = session.get(
        "user",
        "Khách"
    )

    return render_template(
        "user/profile.html",
        user=username
    )