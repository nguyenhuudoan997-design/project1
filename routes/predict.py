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

    # --------------------------------------
    # DEFAULT VALUES
    # --------------------------------------

    prediction_text = None
    error = None

    # Dữ liệu giữ lại trên form
    form_data = {
        "reviews": "",
        "installs": "",
        "price": "0",
        "size": ""
    }

    # --------------------------------------
    # POST
    # --------------------------------------

    if request.method == "POST":

        try:

            # ----------------------------------
            # GET FORM DATA
            # ----------------------------------

            reviews_input = request.form.get(
                "reviews",
                ""
            ).strip()

            installs_input = request.form.get(
                "installs",
                ""
            ).strip()

            price_input = request.form.get(
                "price",
                "0"
            ).strip()

            size_input = request.form.get(
                "size",
                ""
            ).strip()

            # ----------------------------------
            # SAVE FORM DATA
            # ----------------------------------

            form_data = {
                "reviews": reviews_input,
                "installs": installs_input,
                "price": price_input,
                "size": size_input
            }

            # ----------------------------------
            # CHECK EMPTY
            # ----------------------------------

            if not reviews_input:

                raise ValueError(
                    "Vui lòng nhập số Reviews."
                )

            if not installs_input:

                raise ValueError(
                    "Vui lòng nhập số Installs."
                )

            if not size_input:

                raise ValueError(
                    "Vui lòng nhập kích thước ứng dụng."
                )

            # ----------------------------------
            # CONVERT NUMBER
            # ----------------------------------

            reviews = float(
                reviews_input
            )

            installs = float(
                installs_input
            )

            price = float(
                price_input or 0
            )

            size = float(
                size_input
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

            # ----------------------------------
            # RESULT
            # ----------------------------------

            prediction_text = rating

            flash(
                "Dự đoán đã được thực hiện và lưu thành công!",
                "success"
            )

        # --------------------------------------
        # VALUE ERROR
        # --------------------------------------

        except ValueError as err:

            error = str(err)

        # --------------------------------------
        # OTHER ERROR
        # --------------------------------------

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

        form_data=form_data,

        user=session.get(
            "user",
            "Khách"
        ),

        role=session.get(
            "role",
            "User"
        )
    )