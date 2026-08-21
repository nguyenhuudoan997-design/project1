# ============================================================
# IMPORT
# ============================================================

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from services.prediction_service import PredictionService


# ============================================================
# BLUEPRINT
# ============================================================

history_bp = Blueprint(
    "history",
    __name__
)


# ============================================================
# HELPER - LOGIN
# ============================================================

def login_required():
    """
    Kiểm tra người dùng đã đăng nhập hay chưa.
    """

    return "user_id" in session


# ============================================================
# HISTORY
# ============================================================

@history_bp.route("/history")
def history():

    # --------------------------------------------------------
    # CHECK LOGIN
    # --------------------------------------------------------

    if not login_required():

        flash(
            "Vui lòng đăng nhập để xem lịch sử dự đoán.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    # --------------------------------------------------------
    # CURRENT USER
    # --------------------------------------------------------

    user_id = session.get("user_id")
    role = session.get("role")

    # --------------------------------------------------------
    # PAGINATION
    # --------------------------------------------------------

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:
        page = 1

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    keyword = request.args.get(
        "keyword",
        ""
    ).strip()

    # --------------------------------------------------------
    # RATING FILTER
    # --------------------------------------------------------

    rating = request.args.get(
        "rating",
        ""
    ).strip()

    # --------------------------------------------------------
    # DETERMINE HISTORY MODE
    # --------------------------------------------------------
    #
    # User:
    #   chỉ xem prediction của chính mình
    #
    # Admin:
    #   xem toàn bộ prediction
    #
    # --------------------------------------------------------

    if role == "Admin":

        history_user_id = None
        admin_mode = True

    else:

        history_user_id = user_id
        admin_mode = False

    # --------------------------------------------------------
    # GET PAGINATED HISTORY
    # --------------------------------------------------------

    pagination = (
        PredictionService.get_predictions_paginated(
            page=page,
            per_page=10,
            keyword=keyword,
            rating=rating,
            user_id=history_user_id
        )
    )

    history_data = pagination.items

    # --------------------------------------------------------
    # RENDER
    # --------------------------------------------------------

    return render_template(
        "user/history.html",

        history=history_data,

        pagination=pagination,

        keyword=keyword,

        rating=rating,

        admin_mode=admin_mode,

        user=session.get(
            "user",
            "Khách"
        ),

        role=role
    )


# ============================================================
# DELETE ONE PREDICTION
# ============================================================

@history_bp.route(
    "/history/delete/<int:prediction_id>",
    methods=["POST"]
)
def delete_prediction(prediction_id):

    # --------------------------------------------------------
    # CHECK LOGIN
    # --------------------------------------------------------

    if not login_required():

        flash(
            "Vui lòng đăng nhập.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    # --------------------------------------------------------
    # CURRENT USER
    # --------------------------------------------------------

    user_id = session.get("user_id")
    role = session.get("role")

    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------
    #
    # Admin có thể xóa prediction của bất kỳ user nào.
    #
    # --------------------------------------------------------

    if role == "Admin":

        deleted = (
            PredictionService.delete_prediction(
                prediction_id=prediction_id
            )
        )

    # --------------------------------------------------------
    # NORMAL USER
    # --------------------------------------------------------
    #
    # User chỉ được xóa prediction của chính mình.
    #
    # --------------------------------------------------------

    else:

        deleted = (
            PredictionService.delete_prediction(
                prediction_id=prediction_id,
                user_id=user_id
            )
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    if deleted:

        flash(
            "Đã xóa dự đoán thành công.",
            "success"
        )

    else:

        flash(
            "Không tìm thấy dự đoán hoặc bạn không có quyền xóa.",
            "danger"
        )

    # --------------------------------------------------------
    # REDIRECT
    # --------------------------------------------------------

    if role == "Admin":

        return redirect(
            url_for(
                "history.history",
                page=request.args.get(
                    "page",
                    1,
                    type=int
                ),
                keyword=request.args.get(
                    "keyword",
                    ""
                ),
                rating=request.args.get(
                    "rating",
                    ""
                )
            )
        )

    return redirect(
        url_for(
            "history.history",
            page=request.args.get(
                "page",
                1,
                type=int
            ),
            keyword=request.args.get(
                "keyword",
                ""
            ),
            rating=request.args.get(
                "rating",
                ""
            )
        )
    )


# ============================================================
# CLEAR HISTORY
# ============================================================

@history_bp.route(
    "/history/clear",
    methods=["POST"]
)
def clear_history():

    # --------------------------------------------------------
    # CHECK LOGIN
    # --------------------------------------------------------

    if not login_required():

        flash(
            "Vui lòng đăng nhập.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    # --------------------------------------------------------
    # CURRENT USER
    # --------------------------------------------------------

    user_id = session.get("user_id")
    role = session.get("role")

    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------
    #
    # Admin xóa toàn bộ lịch sử.
    #
    # --------------------------------------------------------

    if role == "Admin":

        deleted_count = (
            PredictionService.clear_history()
        )

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------
    #
    # User chỉ xóa lịch sử của chính mình.
    #
    # --------------------------------------------------------

    else:

        deleted_count = (
            PredictionService.clear_history(
                user_id=user_id
            )
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    if deleted_count > 0:

        flash(
            f"Đã xóa {deleted_count} bản ghi lịch sử.",
            "success"
        )

    else:

        flash(
            "Không có dữ liệu để xóa.",
            "info"
        )

    # --------------------------------------------------------
    # REDIRECT
    # --------------------------------------------------------

    return redirect(
        url_for("history.history")
    )