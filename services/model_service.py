from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# ============================================================
# MODEL PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "random_forest_model.pkl"


# ============================================================
# LOAD MODEL
# ============================================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Không tìm thấy model tại: {MODEL_PATH}"
    )


model = joblib.load(MODEL_PATH)


# ============================================================
# EXPECTED FEATURES
# ============================================================

FEATURE_COLUMNS = [
    "Reviews",
    "Installs",
    "Price",
    "Size"
]


# ============================================================
# CHECK MODEL FEATURES
# ============================================================

if hasattr(model, "feature_names_in_"):

    model_features = list(model.feature_names_in_)

    if model_features != FEATURE_COLUMNS:

        raise ValueError(
            "\nModel không tương thích với website!\n"
            f"Model đang yêu cầu: {model_features}\n"
            f"Website đang sử dụng: {FEATURE_COLUMNS}\n\n"
            "Hãy chạy lại train_model.py để tạo model mới "
            "với đúng 4 feature."
        )


# ============================================================
# MODEL SERVICE
# ============================================================

class ModelService:

    @staticmethod
    def predict_rating(
        reviews,
        installs,
        price,
        size
    ):
        """
        Dự đoán Rating dựa trên 4 feature:

        - Reviews
        - Installs
        - Price
        - Size
        """

        # ----------------------------------------------------
        # Convert dữ liệu sang số
        # ----------------------------------------------------

        reviews = float(reviews)
        installs = float(installs)
        price = float(price)
        size = float(size)

        # ----------------------------------------------------
        # Tạo DataFrame
        # ----------------------------------------------------

        input_data = pd.DataFrame({

            "Reviews": [reviews],

            "Installs": [installs],

            "Price": [price],

            "Size": [size]

        })

        # ----------------------------------------------------
        # Predict
        # ----------------------------------------------------

        prediction = model.predict(input_data)

        raw_rating = float(prediction[0])

        # ----------------------------------------------------
        # Giới hạn Rating
        # ----------------------------------------------------

        predicted_rating = np.clip(
            raw_rating,
            1.0,
            5.0
        )

        # ----------------------------------------------------
        # Làm tròn
        # ----------------------------------------------------

        predicted_rating = round(
            float(predicted_rating),
            2
        )

        return predicted_rating