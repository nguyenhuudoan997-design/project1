from flask import Blueprint, render_template, session

from services.prediction_service import PredictionService


analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route("/analytics")
def analytics():

    # ==========================================
    # LOGIN
    # ==========================================

    if "user_id" not in session:

        return render_template(
            "login.html",
            error="Vui lòng đăng nhập."
        )

    user_id = session.get("user_id")

    username = session.get(
        "user",
        "Khách"
    )

    # ==========================================
    # RATING DISTRIBUTION
    # ==========================================

    rating_distribution = (
        PredictionService.get_rating_distribution(
            user_id=user_id
        )
    )

    rating_labels = [
        str(item[0])
        for item in rating_distribution
    ]

    rating_values = [
        int(item[1])
        for item in rating_distribution
    ]

    # ==========================================
    # PREDICTION TREND
    # ==========================================

    prediction_trend = (
        PredictionService.get_prediction_trend(
            user_id=user_id
        )
    )

    trend_labels = [
        str(item.id)
        for item in prediction_trend
    ]

    trend_values = [
        float(item.rating)
        for item in prediction_trend
    ]

    # ==========================================
    # DEBUG
    # ==========================================

    print("================================")
    print("ANALYTICS DATA")
    print("================================")

    print(
        "Trend labels:",
        trend_labels
    )

    print(
        "Trend values:",
        trend_values
    )

    print(
        "Rating labels:",
        rating_labels
    )

    print(
        "Rating values:",
        rating_values
    )

    print("================================")

    # ==========================================
    # RENDER
    # ==========================================

    return render_template(
        "analytics.html",

        user=username,

        trend_labels=trend_labels,
        trend_values=trend_values,

        rating_labels=rating_labels,
        rating_values=rating_values
    )