from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for


# ==========================================
# BLUEPRINT
# ==========================================

auth_bp = Blueprint(
    "auth",
    __name__
)


# ==========================================
# USERS DATABASE
# ==========================================

users_db = {

    "user": {
        "password": "123",
        "role": "User"
    },

    "dev": {
        "password": "dev123",
        "role": "Developer"
    },

    "admin": {
        "password": "admin123",
        "role": "Admin"
    }

}


# ==========================================
# LOGIN
# ==========================================

@auth_bp.route("/", methods=["GET", "POST"])
def login():

    print(">>> LOGIN ROUTE ĐƯỢC GỌI")
    print(">>> METHOD:", request.method)

    error = None

    if request.method == "POST":

        print(">>> ĐÃ NHẬN POST LOGIN")

        username = request.form.get("username")
        password = request.form.get("password")

        print(">>> USERNAME:", username)
        print(">>> PASSWORD:", password)

        if username in users_db:

            print(">>> USERNAME TỒN TẠI")

            if users_db[username]["password"] == password:

                print(">>> PASSWORD ĐÚNG")

                session["user"] = username
                session["role"] = users_db[username]["role"]

                role = users_db[username]["role"]

                print(">>> ROLE:", role)

                if role == "User":

                    print(">>> REDIRECT USER")

                    return redirect(
                        url_for("dashboard.dashboard")
                    )

                elif role == "Developer":

                    print(">>> REDIRECT DEVELOPER")

                    return redirect(
                        url_for("developer.dashboard")
                    )

                elif role == "Admin":

                    print(">>> REDIRECT ADMIN")

                    return redirect(
                        url_for("admin.admin_dashboard")
                    )

            else:

                print(">>> PASSWORD SAI")

                error = "Sai mật khẩu!"

        else:

            print(">>> USERNAME KHÔNG TỒN TẠI")

            error = "Tài khoản không tồn tại!"

    return render_template(
        "login.html",
        error=error
    )

# ==========================================
# REGISTER
# ==========================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    error = None
    success = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:

            error = "Vui lòng nhập đầy đủ thông tin."

        elif username in users_db:

            error = "Tên đăng nhập đã tồn tại."

        else:

            users_db[username] = {
                "password": password,
                "role": "User"
            }

            success = "Đăng ký thành công."

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