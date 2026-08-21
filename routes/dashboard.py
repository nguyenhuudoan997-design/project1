from flask import Blueprint
from flask import render_template
from flask import session

from services.prediction_service import PredictionService


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
def dashboard():

    # ==================================================
    # USER INFORMATION
    # ==================================================

    username = session.get(
        "user",
        "Khách"
    )

    user_id = session.get(
        "user_id"
    )

    role = session.get(
        "role",
        "User"
    )

    # ==================================================
    # DETERMINE DATA SCOPE
    # ==================================================
    #
    # User:
    #     Chỉ xem dữ liệu của chính mình.
    #
    # Admin / Developer:
    #     Xem dữ liệu toàn bộ hệ thống.
    #
    # ==================================================

    if role in ["Admin", "Developer"]:

        dashboard_user_id = None

    else:

        dashboard_user_id = user_id

    # ==================================================
    # STATISTICS
    # ==================================================

    total_prediction = (
        PredictionService.get_total_predictions(
            user_id=dashboard_user_id
        )
    )

    average_rating = (
        PredictionService.get_average_rating(
            user_id=dashboard_user_id
        )
    )

    accuracy = (
        PredictionService.get_prediction_accuracy(
            user_id=dashboard_user_id
        )
    )

    # ==================================================
    # HISTORY
    # ==================================================

    pagination = (
        PredictionService.get_predictions_paginated(
            page=1,
            per_page=10,
            user_id=dashboard_user_id
        )
    )

    history = pagination.items

    # ==================================================
    # TOP USERS
    # ==================================================

    top_users = (
        PredictionService.get_top_users(
            limit=5
        )
    )

    # ==================================================
    # RATING DISTRIBUTION
    # ==================================================

    rating_distribution = (
        PredictionService.get_rating_distribution(
            user_id=dashboard_user_id
        )
    )

    rating_labels = [
        str(item[0])
        for item in rating_distribution
    ]

    rating_values = [
        item[1]
        for item in rating_distribution
    ]

    # ==================================================
    # PREDICTION TREND
    # ==================================================

    prediction_trend = (
        PredictionService.get_prediction_trend(
            user_id=dashboard_user_id
        )
    )

    trend_labels = [
        str(index + 1)
        for index, item in enumerate(
            prediction_trend
        )
    ]

    trend_values = [
        float(item.rating)
        for item in prediction_trend
    ]

    # ==================================================
    # DEBUG
    # ==================================================

    print("================================")
    print("DASHBOARD DATA")
    print("================================")

    print("Username:", username)
    print("Role:", role)
    print("User ID:", user_id)
    print(
        "Dashboard User ID:",
        dashboard_user_id
    )

    print(
        "Total predictions:",
        total_prediction
    )

    print(
        "Average rating:",
        average_rating
    )

    print(
        "Accuracy:",
        accuracy
    )

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

    # ==================================================
    # RENDER DASHBOARD
    # ==================================================

    return render_template(

        "dashboard.html",

        user=username,

        role=role,

        history=history,

        total_prediction=total_prediction,

        average_rating=average_rating,

        accuracy=accuracy,

        top_users=top_users,

        trend_labels=trend_labels,

        trend_values=trend_values,

        rating_labels=rating_labels,

        rating_values=rating_values,

        pagination=pagination,

        keyword="",

        rating=""
    )