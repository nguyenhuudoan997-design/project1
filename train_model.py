"""
File: train_model.py

Description:
    Huấn luyện mô hình Machine Learning sử dụng thuật toán
    Random Forest Regressor để dự đoán điểm Rating của
    ứng dụng trên Google Play Store.

Input:
    data/processed/googleplaystore_features.csv

Output:
    models/random_forest_model.pkl

Authors:
    - Đỗ Huy Hoàng -

Project:
    AI Rating Predictor
"""

from pathlib import Path
from xml.parsers.expat import model

import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split

# ==================================================
# CẤU HÌNH ĐƯỜNG DẪN
# ==================================================

DATA_DIR = Path("data")

PROCESSED_DIR = DATA_DIR / "processed"

MODEL_DIR = Path("models")

REPORT_DIR = Path("reports")

FIGURE_DIR = REPORT_DIR / "figures"

FEATURE_FILE = REPORT_DIR / "feature_importance.csv"

FIGURE_FILE = FIGURE_DIR / "feature_importance.png"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR.mkdir(parents=True, exist_ok=True)

FIGURE_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = PROCESSED_DIR / "googleplaystore_features.csv"

MODEL_FILE = MODEL_DIR / "random_forest_model.pkl"

FEATURE_COLUMNS = [
    "Reviews",
    "Installs",
    "Price",
    "Size"
]

# ==================================================
# TẢI DỮ LIỆU
# ==================================================
def load_data(file_path: Path) -> pd.DataFrame:
    """
    Đọc dữ liệu đặc trưng từ file CSV.

    Parameters
    ----------
    file_path : Path
        Đường dẫn tới file dữ liệu.

    Returns
    -------
    pd.DataFrame
        DataFrame chứa dữ liệu huấn luyện.
    """

    try:

        df = pd.read_csv(file_path)

        print("=" * 60)
        print("TẢI DỮ LIỆU TÍNH NĂNG")
        print("=" * 60)

        print(f"Số dòng : {df.shape[0]}")
        print(f"Số cột  : {df.shape[1]}")

        return df

    except FileNotFoundError:

        print(f"Không tìm thấy file: {file_path}")

        raise

    except Exception as error:

        print(f"Lỗi khi đọc dữ liệu: {error}")

        raise

# ==================================================
# KIỂM TRA DỮ LIỆU
# ==================================================
def inspect_data(df: pd.DataFrame) -> None:
    """
    Kiểm tra tổng quan dữ liệu trước khi huấn luyện.
    """

    print("\n" + "=" * 60)
    print("TỔNG QUAN DỮ LIỆU")
    print("=" * 60)

    print("\nKích thước dữ liệu:")
    print(df.shape)

    print("\nDanh sách cột:")
    print(df.columns.tolist())

    print("\nKiểu dữ liệu:")
    print(df.dtypes)

    print("\nGiá trị thiếu:")
    print(df.isnull().sum())

    print("\n5 dòng đầu:")
    print(df.head())

    print("\nThông tin dữ liệu:")
    df.info()

# ==================================================
# PHÂN CHIA CÁC TÍNH NĂNG VÀ MỤC TIÊU
# ==================================================
def split_features_target(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Tách 4 Feature và Target.

    Features:
        Reviews
        Installs
        Price
        Size

    Target:
        Rating
    """

    print("\n" + "=" * 60)
    print("PHÂN CHIA CÁC TÍNH NĂNG VÀ MỤC TIÊU")
    print("=" * 60)

    target_column = "Rating"

    # Kiểm tra Target
    if target_column not in df.columns:
        raise ValueError(
            f"Không tìm thấy cột '{target_column}'."
        )

    # Kiểm tra 4 Feature
    missing_features = [
        column
        for column in FEATURE_COLUMNS
        if column not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Thiếu Feature: {missing_features}"
        )

    # Chỉ lấy đúng 4 Feature
    X = df[FEATURE_COLUMNS].copy()

    # Target
    y = df[target_column].copy()

    # Kiểm tra missing
    if X.isnull().sum().sum() > 0:

        print("\nPhát hiện giá trị thiếu:")

        print(X.isnull().sum())

        # Điền giá trị thiếu bằng median
        X = X.fillna(X.median())

    if y.isnull().sum() > 0:

        print(
            f"\nPhát hiện {y.isnull().sum()} "
            "giá trị Rating bị thiếu."
        )

        valid_index = y.notna()

        X = X.loc[valid_index]

        y = y.loc[valid_index]

    print(f"Số Feature : {X.shape[1]}")

    print(
        f"Tên Feature : {list(X.columns)}"
    )

    print(
        f"Số Sample  : {len(X)}"
    )

    print("\nFeature sử dụng để train:")

    for feature in X.columns:
        print(f"  - {feature}")

    print("\nTarget:")

    print(f"  - {target_column}")

    return X, y


# ==================================================
# PHÂN CHIA BÀI KIỂM TRA VÀ HUẤN LUYỆN
# ==================================================
def split_train_test(
    X: pd.DataFrame,
    y: pd.Series
) -> tuple:
    """
    Chia dữ liệu thành Train và Test.

    Parameters
    ----------
    X : pd.DataFrame
        Feature.

    y : pd.Series
        Target.

    Returns
    -------
    tuple
        X_train, X_test, y_train, y_test
    """

    print("\n" + "=" * 60)
    print("PHÂN CHIA BÀI KIỂM TRA VÀ HUẤN LUYỆN")
    print("=" * 60)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print(f"Train : {X_train.shape}")
    print(f"Test  : {X_test.shape}")
    print(f"Training Samples : {len(X_train)}")
    print(f"Testing Samples  : {len(X_test)}")
    return X_train, X_test, y_train, y_test

# ==================================================
# HUẤN LUYỆN MÔ HÌNH
# ==================================================
def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> tuple[RandomForestRegressor, np.ndarray, float, float, float, float]:
    """
    Huấn luyện mô hình Random Forest Regressor.

    Parameters
    ----------
    X_train : pd.DataFrame

    y_train : pd.Series

    X_test : pd.DataFrame

    y_test : pd.Series

    Returns
    -------
    tuple
        Mô hình đã được huấn luyện cùng với các kết quả dự đoán và chỉ số.
    """

    print("\n" + "=" * 60)
    print("HUẤN LUYỆN MÔ HÌNH NGẪU NHIÊN")
    print("=" * 60)

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        oob_score=True,
        bootstrap=True
    )

    start_time = time.time()
    model.fit(X_train, y_train)
    end_time = time.time()
    training_time = end_time - start_time

    print("Huấn luyện hoàn thành.")
    print(f"Number of Trees : {model.n_estimators}")
    print(f"Thời gian huấn luyện: {training_time:.2f} giây")

    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(
        y_test,
        predictions
    )
    rmse = mse ** 0.5

    print("\nĐÁNH GIÁ NHANH MÔ HÌNH")
    print(f"R² Score : {r2:.4f}")
    print(f"MAE      : {mae:.4f}")
    print(f"MSE       : {mse:.4f}")
    print(f"RMSE      : {rmse:.4f}")
    print(f"Điểm OOB : {model.oob_score_:.4f}")
    return (
        model,
        predictions,
        r2,
        mae,
        rmse,
        training_time
     )

# ==================================================
# LƯU MÔ HÌNH
# ==================================================
def save_model(
    model: RandomForestRegressor,
    model_path: Path
) -> None:
    """
    Lưu mô hình Machine Learning.

    Parameters
    ----------
    model : RandomForestRegressor
        Mô hình đã huấn luyện.

    model_path : Path
        Đường dẫn lưu mô hình.
    """

    try:

        joblib.dump(model, model_path)

        print("\n" + "=" * 60)
        print("LƯU MÔ HÌNH")
        print("=" * 60)

        print(f"Đã lưu mô hình tại: {model_path}")

    except Exception as error:

        print(f"Lỗi khi lưu mô hình: {error}")

        raise

def save_training_summary():
    """
    Lưu tóm tắt quá trình huấn luyện mô hình.
    """
    pass
# ==================================================
# TÍNH IMPORTANCE TÍNH NĂNG
# ==================================================
def feature_importance(
    model: RandomForestRegressor,
    feature_names: list[str]
) -> pd.DataFrame:
    """
    Tính độ quan trọng của các tính năng.
    """

    importance_values = getattr(model, "feature_importances_", None)

    if importance_values is None:
        raise AttributeError("Mô hình không có thuộc tính feature_importances_.")

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importance_values
    }).sort_values(by="Importance", ascending=False).reset_index(drop=True)

    print("\n" + "=" * 60)
    print("TÍNH IMPORTANCE CỦA FEATURE")
    print("=" * 60)
    print(importance_df.head(10))

    return importance_df

def save_feature_importance(
    importance_df: pd.DataFrame
) -> None:
    """
    Lưu DataFrame mức quan trọng của các tính năng.
    """

    try:
        importance_df.to_csv(FEATURE_FILE, index=False)

        print("\n" + "=" * 60)
        print("TÍNH NĂNG QUAN TRỌNG ĐÃ LƯU")
        print("=" * 60)
        print(f"Đã lưu feature importance tại: {FEATURE_FILE}")

    except Exception as error:
        print(f"Lỗi khi lưu feature importance: {error}")
        raise

def plot_feature_importance(
    importance_df: pd.DataFrame,
    max_features: int = 20
) -> None:
    """
    Vẽ biểu đồ mức quan trọng của các tính năng.
    """
    top_features = importance_df.head(max_features).sort_values(by="Importance", ascending=False)

    plt.figure(figsize=(10, 8))
    plt.barh(top_features["Feature"], top_features["Importance"], color="skyblue")
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Feature Importance")
    plt.tight_layout()
    plt.savefig(
        FIGURE_FILE,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    print("\n" + "=" * 60)
    print("VẼ VÀ LƯU BIỂU ĐỒ IMPORTANCE")
    print("=" * 60)
    print(f"Đã lưu biểu đồ tại: {FIGURE_FILE}")

# ==================================================
# HÀM CHÍNH
# ==================================================
def main() -> None:
    """
    Điều khiển toàn bộ quá trình huấn luyện mô hình.
    """
    print("=" * 60)
    print("HUẤN LUYỆN MÔ HÌNH RANDOM FOREST")
    print("=" * 60)

    # Đọc dữ liệu
    df = load_data(INPUT_FILE)

    # Kiểm tra dữ liệu
    inspect_data(df)

    # Tách Feature và Target
    X, y = split_features_target(df)

    # Chia Train/Test
    X_train, X_test, y_train, y_test = split_train_test(
        X,
        y
    )

    # Huấn luyện mô hình
    (model, predictions, r2, mae, rmse, training_time) = train_model(
        X_train,
        y_train,
        X_test,
        y_test
    )
    importance_df = feature_importance(
        model,
        X.columns.tolist()
    )
    print("\nTOP 10 FEATURE")

    print(importance_df.head(10))
    
    save_feature_importance(
        importance_df
    )
   
    plot_feature_importance(
       importance_df
    )
    
    # Lưu mô hình
    save_model(
        model,
        MODEL_FILE
    )

    save_training_summary()
    
    print("\nTÓM TẮT MÔ HÌNH")
    print("-" * 40)
    print(f"Algorithm      : Random Forest")
    print(f"Trees          : {model.n_estimators}")
    print(f"Model Saved    : {MODEL_FILE}")
    print(f"Feature Report : reports/feature_importance.csv")
    
    print("\n" + "=" * 60)
    print("MÔ HÌNH ĐÃ HOÀN THÀNH")
    print("=" * 60)

    print(f"Model               : {MODEL_FILE}")
    print(f"Feature Importance  : {FEATURE_FILE}")
    print(f"Figure              : {FIGURE_FILE}")
    print(f"Training Time       : {training_time:.2f} seconds")

# ==================================================
# CHẠY HÀM CHÍNH
# ==================================================

if __name__ == "__main__":
    main()