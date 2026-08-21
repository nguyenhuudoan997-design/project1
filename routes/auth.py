# ==========================================
# IMPORT
# ==========================================

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)

from extensions import db
from models.user import User


# ==========================================
# BLUEPRINT
# ==========================================

auth_bp = Blueprint(
    "auth",
    __name__
)


# ==========================================
# LOGIN
# ==========================================

@auth_bp.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # --------------------------------------
        # VALIDATE
        # --------------------------------------

        if not username or not password:

            error = (
                "Vui lòng nhập đầy đủ "
                "tên đăng nhập và mật khẩu."
            )

            return render_template(
                "login.html",
                error=error
            )

        # --------------------------------------
        # FIND USER
        # --------------------------------------

        user = User.query.filter_by(
            username=username
        ).first()

        if user is None:

            error = "Tài khoản không tồn tại."

            return render_template(
                "login.html",
                error=error
            )

        # --------------------------------------
        # CHECK PASSWORD
        # --------------------------------------

        if not user.check_password(password):

            error = "Sai mật khẩu."

            return render_template(
                "login.html",
                error=error
            )

        # --------------------------------------
        # CREATE SESSION
        # --------------------------------------

        session.clear()

        session["user_id"] = user.id
        session["user"] = user.username
        session["role"] = user.role

        # --------------------------------------
        # REDIRECT BY ROLE
        # --------------------------------------

        if user.role == "User":

            return redirect(
                url_for("dashboard.dashboard")
            )

        if user.role == "Developer":

            return redirect(
                url_for("developer.dashboard")
            )

        if user.role == "Admin":

            return redirect(
                url_for("admin.admin_dashboard")
            )

        # --------------------------------------
        # INVALID ROLE
        # --------------------------------------

        session.clear()

        error = (
            "Tài khoản có quyền truy cập "
            "không hợp lệ."
        )

        return render_template(
            "login.html",
            error=error
        )

    return render_template(
        "login.html",
        error=error
    )


# ==========================================
# REGISTER
# ==========================================

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    error = None
    success = None

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # --------------------------------------
        # VALIDATE
        # --------------------------------------

        if not username or not password:

            error = (
                "Vui lòng nhập đầy đủ "
                "thông tin."
            )

        # --------------------------------------
        # CHECK USERNAME
        # --------------------------------------

        elif User.query.filter_by(
            username=username
        ).first():

            error = (
                "Tên đăng nhập đã tồn tại."
            )

        # --------------------------------------
        # CREATE USER
        # --------------------------------------

        else:

            user = User(
                username=username,
                role="User"
            )

            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            success = (
                "Đăng ký thành công. "
                "Bạn có thể đăng nhập."
            )

    return render_template(
        "auth/register.html",
        error=error,
        success=success
    )


# ==========================================
# LOGOUT
# ==========================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )