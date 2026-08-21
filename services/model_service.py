# ==========================================
# IMPORT
# ==========================================

from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# ==========================================
# MODEL PATH
# ==========================================

BASE_DIR = Path(
    __file__
).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "random_forest_model.pkl"
)


# ==========================================
# LOAD MODEL
# ==========================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Không tìm thấy model tại: {MODEL_PATH}"
    )


model = joblib.load(
    MODEL_PATH
)


# ==========================================
# EXPECTED FEATURES
# ==========================================

FEATURE_COLUMNS = [
    "Reviews",
    "Installs",
    "Price",
    "Size"
]


# ==========================================
# CHECK MODEL FEATURES
# ==========================================

if hasattr(
    model,
    "feature_names_in_"
):

    model_features = list(
        model.feature_names_in_
    )

    if model_features != FEATURE_COLUMNS:

        raise ValueError(
            "\nModel không tương thích với website!\n"
            f"Model đang yêu cầu: {model_features}\n"
            f"Website đang sử dụng: {FEATURE_COLUMNS}\n\n"
            "Hãy train lại model."
        )


# ==========================================
# MODEL SERVICE
# ==========================================

class ModelService:

    @staticmethod
    def predict_rating(
        reviews,
        installs,
        price,
        size
    ):
        """
        Dự đoán Rating dựa trên:

        Reviews
        Installs
        Price
        Size
        """

        reviews = float(reviews)
        installs = float(installs)
        price = float(price)
        size = float(size)

        # ----------------------------------
        # INPUT DATA
        # ----------------------------------

        input_data = pd.DataFrame({

            "Reviews": [
                reviews
            ],

            "Installs": [
                installs
            ],

            "Price": [
                price
            ],

            "Size": [
                size
            ]

        })

        # ----------------------------------
        # PREDICT
        # ----------------------------------

        prediction = model.predict(
            input_data
        )

        raw_rating = float(
            prediction[0]
        )

        # ----------------------------------
        # LIMIT RATING
        # ----------------------------------

        predicted_rating = np.clip(
            raw_rating,
            1.0,
            5.0
        )

        # ----------------------------------
        # ROUND
        # ----------------------------------

        predicted_rating = round(
            float(predicted_rating),
            2
        )

        return predicted_rating