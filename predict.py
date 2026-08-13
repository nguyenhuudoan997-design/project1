# ==========================================
# IMPORT
# ==========================================

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)

from services.model_service import ModelService
from services.prediction_service import PredictionService


# ==========================================
# BLUEPRINT
# ==========================================

predict_bp = Blueprint(
    "predict",
    __name__
)


# ==========================================
# PREDICT
# ==========================================

@predict_bp.route(
    "/predict",
    methods=["GET", "POST"]
)
def predict():

    # --------------------------------------
    # CHECK LOGIN
    # --------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    prediction_text = None
    error = None

    # --------------------------------------
    # POST
    # --------------------------------------

    if request.method == "POST":

        try:

            reviews = float(
                request.form.get(
                    "reviews",
                    0
                )
            )

            installs = float(
                request.form.get(
                    "installs",
                    0
                )
            )

            price = float(
                request.form.get(
                    "price",
                    0
                )
            )

            size = float(
                request.form.get(
                    "size",
                    0
                )
            )

            # ----------------------------------
            # VALIDATE
            # ----------------------------------

            if reviews < 0:

                raise ValueError(
                    "Reviews không được âm."
                )

            if installs < 0:

                raise ValueError(
                    "Installs không được âm."
                )

            if price < 0:

                raise ValueError(
                    "Price không được âm."
                )

            if size < 0:

                raise ValueError(
                    "Size không được âm."
                )

            # ----------------------------------
            # MODEL PREDICTION
            # ----------------------------------

            rating = ModelService.predict_rating(
                reviews=reviews,
                installs=installs,
                price=price,
                size=size
            )

            # ----------------------------------
            # LIMIT RATING
            # ----------------------------------

            rating = max(
                0,
                min(
                    5,
                    float(rating)
                )
            )

            rating = round(
                rating,
                2
            )

            # ----------------------------------
            # SAVE DATABASE
            # ----------------------------------

            PredictionService.save_prediction(
                user_id=session["user_id"],
                reviews=reviews,
                installs=installs,
                price=price,
                size=size,
                rating=rating
            )

            prediction_text = rating

            flash(
                "Dự đoán đã được lưu thành công!",
                "success"
            )

        except ValueError as err:

            error = str(err)

        except Exception as err:

            error = (
                f"Lỗi khi dự đoán: {err}"
            )

    # --------------------------------------
    # RENDER
    # --------------------------------------

    return render_template(
        "user/predict.html",
        prediction_text=prediction_text,
        error=error,
        user=session.get("user"),
        role=session.get("role")
    )