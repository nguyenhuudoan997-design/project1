# ==========================================
# IMPORT
# ==========================================

import os
import joblib
import pandas as pd

from flask import (
    Blueprint,
    render_template,
    request,
    current_app
)

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


# ==========================================
# BLUEPRINT
# ==========================================

admin_bp = Blueprint(
    "admin",
    __name__
)


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@admin_bp.route("/admin")
def admin_dashboard():

    return render_template(
        "admin/dashboard.html",
        user="Admin",
        total_users=0,
        total_predictions=0,
        average_rating=0,
        accuracy=0,
        message=None
    )


# ==========================================
# ADMIN - MANAGE USERS
# ==========================================

@admin_bp.route("/admin/users")
def users():

    return render_template(
        "admin/users.html",
        user="Admin"
    )


# ==========================================
# ADMIN - RETRAIN MODEL
# ==========================================

@admin_bp.route(
    "/admin_retrain",
    methods=["POST"]
)
def admin_retrain():

    template = "admin/dashboard.html"

    # --------------------------------------
    # Kiểm tra file
    # --------------------------------------

    if "file" not in request.files:

        return render_template(
            template,
            user="Admin",
            message="❌ Không tìm thấy file tải lên!"
        )

    file = request.files["file"]

    # --------------------------------------
    # Kiểm tra tên file
    # --------------------------------------

    if file.filename == "":

        return render_template(
            template,
            user="Admin",
            message="❌ Bạn chưa chọn file CSV!"
        )

    # --------------------------------------
    # Kiểm tra định dạng
    # --------------------------------------

    if not file.filename.lower().endswith(".csv"):

        return render_template(
            template,
            user="Admin",
            message="❌ Chỉ chấp nhận file .csv"
        )

    # --------------------------------------
    # Upload folder
    # --------------------------------------

    upload_folder = current_app.config.get(
        "UPLOAD_FOLDER",
        "uploads"
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    # --------------------------------------
    # Đường dẫn file CSV
    # --------------------------------------

    file_path = os.path.join(
        upload_folder,
        "googleplaystore.csv"
    )

    file.save(file_path)

    # ======================================
    # TRAIN MODEL
    # ======================================

    try:

        # ----------------------------------
        # Đọc dữ liệu
        # ----------------------------------

        df = pd.read_csv(file_path)

        # ----------------------------------
        # Kiểm tra Rating
        # ----------------------------------

        if "Rating" not in df.columns:

            return render_template(
                template,
                user="Admin",
                message=(
                    "❌ File CSV không có "
                    "cột Rating!"
                )
            )

        # ----------------------------------
        # Làm sạch Rating
        # ----------------------------------

        df["Rating"] = pd.to_numeric(
            df["Rating"],
            errors="coerce"
        )

        df = df.dropna(
            subset=["Rating"]
        )

        # ----------------------------------
        # Kiểm tra Features
        # ----------------------------------

        features = [
            "Reviews",
            "Installs",
            "Price",
            "Size"
        ]

        missing_features = [
            column
            for column in features
            if column not in df.columns
        ]

        if missing_features:

            return render_template(
                template,
                user="Admin",
                message=(
                    "❌ File CSV thiếu các cột: "
                    + ", ".join(missing_features)
                )
            )

        # ----------------------------------
        # Làm sạch Reviews
        # ----------------------------------

        df["Reviews"] = pd.to_numeric(
            df["Reviews"],
            errors="coerce"
        )

        # ----------------------------------
        # Làm sạch Installs
        # ----------------------------------

        df["Installs"] = (
            df["Installs"]
            .astype(str)
            .str.replace(
                "+",
                "",
                regex=False
            )
            .str.replace(
                ",",
                "",
                regex=False
            )
        )

        df["Installs"] = pd.to_numeric(
            df["Installs"],
            errors="coerce"
        )

        # ----------------------------------
        # Làm sạch Price
        # ----------------------------------

        df["Price"] = (
            df["Price"]
            .astype(str)
            .str.replace(
                "$",
                "",
                regex=False
            )
        )

        df["Price"] = pd.to_numeric(
            df["Price"],
            errors="coerce"
        )

        # ----------------------------------
        # Làm sạch Size
        # ----------------------------------

        df["Size"] = (
            df["Size"]
            .astype(str)
            .str.replace(
                "M",
                "",
                regex=False
            )
            .str.replace(
                "k",
                "",
                regex=False
            )
        )

        df["Size"] = pd.to_numeric(
            df["Size"],
            errors="coerce"
        )

        # ----------------------------------
        # X và y
        # ----------------------------------

        X = df[features].fillna(0)

        y = df["Rating"]

        # ----------------------------------
        # Kiểm tra dữ liệu
        # ----------------------------------

        if len(X) < 10:

            return render_template(
                template,
                user="Admin",
                message=(
                    "❌ Dữ liệu quá ít để "
                    "huấn luyện Model!"
                )
            )

        # ----------------------------------
        # Train / Test Split
        # ----------------------------------

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )
        )

        # ----------------------------------
        # Random Forest
        # ----------------------------------

        new_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )

        new_model.fit(
            X_train,
            y_train
        )

        # ----------------------------------
        # Models folder
        # ----------------------------------

        model_folder = os.path.join(
            current_app.root_path,
            "models"
        )

        os.makedirs(
            model_folder,
            exist_ok=True
        )

        # ----------------------------------
        # Model path
        # ----------------------------------

        model_path = os.path.join(
            model_folder,
            "random_forest_model.pkl"
        )

        # ----------------------------------
        # Save model
        # ----------------------------------

        joblib.dump(
            new_model,
            model_path
        )

        message = (
            "✅ Retrain Model thành công! "
            "Model đã được cập nhật."
        )

    except Exception as err:

        message = (
            f"❌ Lỗi khi Retrain Model: {err}"
        )

    # --------------------------------------
    # Trả kết quả
    # --------------------------------------

    return render_template(
        template,
        user="Admin",
        total_users=0,
        total_predictions=0,
        average_rating=0,
        accuracy=0,
        message=message
    )