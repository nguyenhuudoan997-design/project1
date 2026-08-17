from flask import Blueprint, render_template

from services.prediction_service import PredictionService

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics")
def analytics():

    prediction_trend = PredictionService.get_prediction_trend()

    trend_labels = []
    trend_values = []

    for item in prediction_trend:
        trend_labels.append(item.id)
        trend_values.append(item.rating)

    rating_distribution = PredictionService.get_rating_distribution()

    rating_labels = []
    rating_values = []

    for item in rating_distribution:
        rating_labels.append(str(item[0]))
        rating_values.append(item[1])

    return render_template(
        "charts.html",
        trend_labels=trend_labels,
        trend_values=trend_values,
        rating_labels=rating_labels,
        rating_values=rating_values
    )