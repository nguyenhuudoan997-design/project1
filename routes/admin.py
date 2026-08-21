# ==========================================
# IMPORT
# ==========================================

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from extensions import db
from models.user import User
from models.prediction import Prediction
from services.prediction_service import PredictionService


# ==========================================
# BLUEPRINT
# ==========================================

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ==========================================
# ADMIN AUTHORIZATION
# ==========================================

def admin_required():
    """
    Kiểm tra người dùng hiện tại có phải Admin hay không.
    """

    if "user_id" not in session:
        return False

    if session.get("role") != "Admin":
        return False

    return True


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@admin_bp.route("/")
def admin_dashboard():

    if not admin_required():
        flash(
            "Bạn không có quyền truy cập khu vực quản trị.",
            "danger"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    # --------------------------------------
    # SYSTEM STATISTICS
    # --------------------------------------

    system_stats = PredictionService.get_system_statistics()

    total_users = system_stats["total_users"]

    total_predictions = system_stats["total_predictions"]

    average_rating = system_stats["average_rating"]

    accuracy = system_stats["accuracy"]

    total_admins = system_stats["total_admins"]

    total_developers = system_stats["total_developers"]

    total_normal_users = system_stats["total_normal_users"]
    
    total_admins = User.query.filter_by(
        role="Admin"
    ).count()

    total_developers = User.query.filter_by(
        role="Developer"
    ).count()

    total_normal_users = User.query.filter_by(
        role="User"
    ).count()

    # --------------------------------------
    # RECENT USERS
    # --------------------------------------

    recent_users = (
        User.query
        .order_by(User.created_at.desc())
        .limit(5)
        .all()
    )

    # --------------------------------------
    # RECENT PREDICTIONS
    # --------------------------------------

    recent_predictions = (
        Prediction.query
        .order_by(Prediction.created_at.desc())
        .limit(10)
        .all()
    )

    # --------------------------------------
    # RATING DISTRIBUTION
    # --------------------------------------

    rating_distribution = (
        PredictionService
        .get_rating_distribution()
    )

    rating_labels = [
        str(item[0])
        for item in rating_distribution
    ]

    rating_values = [
        item[1]
        for item in rating_distribution
    ]

    # --------------------------------------
    # RENDER
    # --------------------------------------

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_predictions=total_predictions,
        average_rating=average_rating,
        accuracy=accuracy,
        total_admins=total_admins,
        total_developers=total_developers,
        total_normal_users=total_normal_users,
        recent_users=recent_users,
        recent_predictions=recent_predictions,
        rating_labels=rating_labels,
        rating_values=rating_values
    )


# ==========================================
# MANAGE USERS
# ==========================================

@admin_bp.route("/users")
def users():

    if not admin_required():
        flash(
            "Bạn không có quyền truy cập.",
            "danger"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    keyword = request.args.get(
        "keyword",
        ""
    ).strip()

    role = request.args.get(
        "role",
        ""
    ).strip()

    query = User.query

    # --------------------------------------
    # SEARCH
    # --------------------------------------

    if keyword:

        query = query.filter(
            User.username.ilike(
                f"%{keyword}%"
            )
        )

    # --------------------------------------
    # ROLE FILTER
    # --------------------------------------

    if role:

        query = query.filter(
            User.role == role
        )

    # --------------------------------------
    # ORDER
    # --------------------------------------

    users_list = (
        query
        .order_by(User.created_at.desc())
        .all()
    )

    return render_template(
        "admin/users.html",
        users=users_list,
        keyword=keyword,
        role=role
    )


# ==========================================
# USER DETAIL
# ==========================================

@admin_bp.route("/users/<int:user_id>")
def user_detail(user_id):

    if not admin_required():
        flash(
            "Bạn không có quyền truy cập.",
            "danger"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    user = User.query.get_or_404(
        user_id
    )

    predictions = (
        Prediction.query
        .filter_by(user_id=user.id)
        .order_by(
            Prediction.created_at.desc()
        )
        .all()
    )

    return render_template(
        "admin/user_detail.html",
        user=user,
        predictions=predictions
    )


# ==========================================
# CHANGE USER ROLE
# ==========================================

@admin_bp.route(
    "/users/<int:user_id>/role",
    methods=["POST"]
)
def change_role(user_id):

    if not admin_required():
        flash(
            "Bạn không có quyền thực hiện thao tác này.",
            "danger"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    user = User.query.get_or_404(
        user_id
    )

    # Không cho Admin tự đổi quyền của chính mình

    if user.id == session.get("user_id"):

        flash(
            "Bạn không thể thay đổi quyền của chính mình.",
            "warning"
        )

        return redirect(
            url_for("admin.users")
        )

    new_role = request.form.get(
        "role"
    )

    allowed_roles = [
        "User",
        "Developer",
        "Admin"
    ]

    if new_role not in allowed_roles:

        flash(
            "Quyền người dùng không hợp lệ.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.user_detail",
                user_id=user.id
            )
        )

    user.role = new_role

    db.session.commit()

    flash(
        "Đã cập nhật quyền người dùng.",
        "success"
    )

    return redirect(
        url_for(
            "admin.user_detail",
            user_id=user.id
        )
    )


# ==========================================
# DELETE USER
# ==========================================

@admin_bp.route(
    "/users/<int:user_id>/delete",
    methods=["POST"]
)
def delete_user(user_id):

    if not admin_required():
        flash(
            "Bạn không có quyền thực hiện thao tác này.",
            "danger"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    user = User.query.get_or_404(
        user_id
    )

    # Không cho Admin tự xóa chính mình

    if user.id == session.get("user_id"):

        flash(
            "Bạn không thể xóa tài khoản của chính mình.",
            "warning"
        )

        return redirect(
            url_for("admin.users")
        )

    username = user.username

    db.session.delete(user)
    db.session.commit()

    flash(
        f"Đã xóa người dùng {username}.",
        "success"
    )

    return redirect(
        url_for("admin.users")
    )


# ==========================================
# ALL PREDICTION HISTORY
# ==========================================

@admin_bp.route("/predictions")
def predictions():

    if not admin_required():
        flash(
            "Bạn không có quyền truy cập.",
            "danger"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    keyword = request.args.get(
        "keyword",
        ""
    ).strip()

    rating = request.args.get(
        "rating",
        ""
    ).strip()

    pagination = (
        PredictionService
        .get_predictions_paginated(
            page=page,
            per_page=10,
            keyword=keyword,
            rating=rating,
            user_id=None
        )
    )

    history = pagination.items

    return render_template(
        "user/history.html",
        history=history,
        pagination=pagination,
        keyword=keyword,
        rating=rating,
        admin_mode=True
    )


# ==========================================
# RETRAIN PAGE
# ==========================================

@admin_bp.route(
    "/retrain",
    methods=["GET", "POST"]
)
def admin_retrain():

    if not admin_required():
        flash(
            "Bạn không có quyền truy cập.",
            "danger"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    if request.method == "POST":

        file = request.files.get(
            "dataset"
        )

        if not file:

            flash(
                "Vui lòng chọn file CSV.",
                "warning"
            )

            return redirect(
                url_for("admin.admin_retrain")
            )

        # ------------------------------------------------
        # PHẦN TRAIN MODEL
        # ------------------------------------------------
        #
        # Tạm thời chưa gọi train_model.py tại đây.
        #
        # Sau khi phần Admin ổn định, chúng ta sẽ
        # nối chức năng training vào đây.
        #

        flash(
            "File đã được nhận. Chức năng huấn luyện mô hình sẽ được xử lý ở bước tiếp theo.",
            "info"
        )

        return redirect(
            url_for("admin.admin_retrain")
        )

    return render_template(
        "admin/retrain.html"
    )