# ==========================================
# IMPORT
# ==========================================

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from services.prediction_service import (
    PredictionService
)


# ==========================================
# BLUEPRINT
# ==========================================

history_bp = Blueprint(
    "history",
    __name__
)


# ==========================================
# HISTORY
# ==========================================

@history_bp.route("/history")
def history():

    # --------------------------------------
    # CHECK LOGIN
    # --------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    keyword = request.args.get(
        "keyword",
        ""
    ).strip()

    rating = request.args.get(
        "rating",
        ""
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:

        page = 1

    # --------------------------------------
    # PAGINATION
    # --------------------------------------

    pagination = (
        PredictionService
        .get_predictions_paginated(
            page=page,
            per_page=10,
            keyword=keyword,
            rating=rating,
            user_id=session["user_id"]
        )
    )

    return render_template(
        "user/history.html",
        history=pagination.items,
        pagination=pagination,
        keyword=keyword,
        rating=rating,
        user=session.get("user"),
        role=session.get("role")
    )


# ==========================================
# DELETE ONE
# ==========================================

@history_bp.route(
    "/history/delete/<int:prediction_id>",
    methods=["POST"]
)
def delete_prediction(
    prediction_id
):

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    try:

        deleted = (
            PredictionService
            .delete_prediction(
                prediction_id,
                user_id=session["user_id"]
            )
        )

        if deleted:

            flash(
                "Dự đoán đã được xóa thành công!",
                "success"
            )

        else:

            flash(
                "Không tìm thấy dự đoán.",
                "warning"
            )

    except Exception as err:

        flash(
            f"Không thể xóa dự đoán: {err}",
            "danger"
        )

    return redirect(
        url_for("history.history")
    )


# ==========================================
# CLEAR ALL
# ==========================================

@history_bp.route(
    "/history/clear",
    methods=["POST"]
)
def clear_history():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    try:

        deleted_count = (
            PredictionService
            .clear_history(
                user_id=session["user_id"]
            )
        )

        flash(
            f"Đã xóa {deleted_count} "
            "bản ghi lịch sử.",
            "success"
        )

    except Exception as err:

        flash(
            f"Không thể xóa lịch sử: {err}",
            "danger"
        )

    return redirect(
        url_for("history.history")
    )