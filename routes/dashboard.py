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

    username = session.get("user", "Khách")

    total_prediction = PredictionService.get_total_predictions()

    average_rating = PredictionService.get_average_rating()

    accuracy = PredictionService.get_prediction_accuracy()

    pagination = PredictionService.get_predictions_paginated(
        page=1,
        per_page=10
    )

    history = pagination.items

    top_users = PredictionService.get_top_users()

    rating_distribution = PredictionService.get_rating_distribution()

    prediction_trend = PredictionService.get_prediction_trend()

    trend_labels = [item.id for item in prediction_trend]

    trend_values = [item.rating for item in prediction_trend]

    rating_labels = [str(item[0]) for item in rating_distribution]

    rating_values = [item[1] for item in rating_distribution]

    return render_template(

        "dashboard.html",

        user=username,

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