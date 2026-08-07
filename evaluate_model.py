"""
File: evaluate_model.py

Description:
    Đánh giá mô hình Machine Learning Random Forest Regressor
    sau khi huấn luyện. Chương trình tính các chỉ số đánh giá,
    trực quan hóa kết quả dự đoán và xuất báo cáo.

Input:
    data/processed/googleplaystore_features.csv
    models/random_forest_model.pkl

Output:
    reports/model_report.txt
    reports/figures/actual_vs_predicted.png
    reports/figures/residual_plot.png

Authors:
    - Nguyễn Hữu Đoàn -

Project:
    AI Rating Predictor
"""
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import explained_variance_score

# ==================================================
# CẤU HÌNH ĐƯỜNG DẪN
# ==================================================
DATA_DIR = Path("data")
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = Path("models")
REPORT_DIR = Path("reports")
FIGURE_DIR = REPORT_DIR / "figures"
INPUT_FILE = PROCESSED_DIR / "googleplaystore_features.csv"
MODEL_FILE = MODEL_DIR / "random_forest_model.pkl"
REPORT_FILE = REPORT_DIR / "model_report.txt"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# TẢI DỮ LIỆU
# ==================================================
def load_data(file_path: Path) -> pd.DataFrame:
    """
    Đọc dữ liệu Feature.
    Parameters
    ----------
    file_path : Path
        Đường dẫn tới file dữ liệu.
    Returns
    -------
    pd.DataFrame
        DataFrame chứa dữ liệu đánh giá.
    """
    try:
        df = pd.read_csv(file_path)

        print("=" * 60)
        print("TẢI DỮ LIỆU FEATURE")
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
# TẢI MÔ HÌNH
# ==================================================
def load_model(
    model_path: Path
) -> RandomForestRegressor:
    """
    Đọc mô hình Machine Learning đã huấn luyện.
    Parameters
    ----------
    model_path : Path
        Đường dẫn tới file mô hình.
    Returns
    -------
    RandomForestRegressor
        Mô hình đã huấn luyện.
    """
    try:
        model = joblib.load(model_path)
        
        if not hasattr(model, "feature_importances_"):
            raise ValueError(
                "Mô hình chưa được huấn luyện."
            )
        print(type(model))
        print("\n" + "=" * 60)
        print("TẢI MÔ HÌNH")
        print("=" * 60)
        print(f"Đã tải mô hình từ: {model_path}")

        return model
    except FileNotFoundError:
        print(f"Không tìm thấy mô hình: {model_path}")
        raise
    except Exception as error:
        print(f"Lỗi khi tải mô hình: {error}")
        raise

# ==================================================
# KIỂM TRA DỮ LIỆU
# ==================================================
def inspect_data(df: pd.DataFrame) -> None:
    """
    Hiển thị thông tin dữ liệu đánh giá.
    """

    print("\n" + "=" * 60)
    print("KIỂM TRA DỮ LIỆU")
    print("=" * 60)
    print("Hình dạng:", df.shape)
    print("\nKiểu dữ liệu")
    print(df.dtypes)
    print("\nGiá trị bị thiếu")
    print(df.isnull().sum())
    print("\nSao chép")
    print(df.duplicated().sum())
    print("\n5 dòng đầu")
    print(df.head())

def validate_data(df: pd.DataFrame) -> None:
    """
    Kiểm tra dữ liệu đầu vào.
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa dữ liệu.
    """
    print("="*60)
    print("XÁC THỰC DỮ LIỆU")
    print("="*60)
    print("Hình dạng :",df.shape)
    print("Sao chép :",df.duplicated().sum())
    print("Giá trị thiếu :",df.isnull().sum().sum())
    print("Vô cực :",
          np.isinf(df.select_dtypes(include="number")).sum().sum())
    
    if df.isnull().sum().sum() > 0:
            raise ValueError("Dữ liệu chứa giá trị thiếu.")
    
# ==================================================
# TÁCH TÍNH NĂNG VÀ MỤC TIÊU
# ==================================================
def split_features_target(
    df: pd.DataFrame
) -> tuple[
    pd.DataFrame,
    pd.Series,
    pd.DataFrame,
    pd.Series
]:
    """
    Tách dữ liệu thành Train và Test giống train_model.py.
    Parameters
    ----------
    df : pd.DataFrame
    Returns
    -------
    tuple
        X_test, y_test sau khi chia dữ liệu.
    """
    print("\n" + "=" * 60)
    print("CHUẨN BỊ DỮ LIỆU TEST")
    print("=" * 60)

    target_column = "Rating"

    if target_column not in df.columns:
        raise ValueError(
            f"Không tìm thấy cột '{target_column}'."
        )

    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    if X.isnull().sum().sum() > 0:
        raise ValueError(
            "Tính năng vẫn còn thiếu giá trị."
        )
    if y.isnull().sum() > 0:
        raise ValueError(
            "Mục tiêu vẫn còn thiếu giá trị."
        )
    
    duplicate = X.duplicated().sum()
    print(f"Tính năng nhân bản : {duplicate}")
    
    (X_train,X_test,y_train,y_test) = train_test_split(X,y,test_size=0.2,random_state=42)

    print(f"Train Size : {len(X_train)}")
    print(f"Test Size  : {len(X_test)}")
    
    return X_test, y_test

# ==================================================
# ĐÁNH GIÁ MÔ HÌNH
# ==================================================
def evaluate_model(
    model: RandomForestRegressor,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> tuple[np.ndarray, dict]:
    """
    Đánh giá mô hình Machine Learning.
    Parameters
    ----------
    model : RandomForestRegressor
        Random Forest đã huấn luyện.
    X_test : pd.DataFrame
    y_test : pd.Series
    Returns
    -------
    tuple
        predictions, metrics
    """
    print("\n" + "=" * 60)
    print("ĐÁNH GIÁ MÔ HÌNH")
    print("=" * 60)

    predictions = model.predict(X_test)
    
    print("\nThông tin dự đoán")
    print(f"Dự đoán tối thiểu: {predictions.min():.3f}")
    print(f"Dự đoán tối đa: {predictions.max():.3f}")
    print(f"Dự đoan trung bình: {predictions.mean():.3f}")
    print(f"Hình dạng dự đoán: {predictions.shape}")
    print("\n5 Dự đoán đầu")
    print(predictions[:5])
    print()
    print("Sai số trung bình")
    print(np.mean(np.abs(predictions-y_test)))
    
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    mape = (
        np.mean(
            np.abs((y_test - predictions) / y_test)
        ) * 100
    )
    absolute_errors = np.abs(y_test - predictions)
    max_error = absolute_errors.max()
    min_error = absolute_errors.min()
    mean_error = absolute_errors.mean()
    explained_variance = explained_variance_score(
        y_test,
        predictions
    )
    metrics = {
        "R2 Score": r2,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "Maximum Error": max_error,
        "Minimum Error": min_error,
        "Mean Error": mean_error,
        "Explained Variance": explained_variance,
        "MAPE (%)": mape
    }
    metrics["Explained Variance"] = explained_variance
    
    importance = pd.DataFrame({
        "Feature": X_test.columns,
        "Importance": model.feature_importances_
    })
    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )
    importance.to_csv(
        REPORT_DIR / "feature_importance.csv",
        index=False
    )
    importance.head(20).to_csv(
        REPORT_DIR/"top20_feature_importance.csv",
        index=False
    )
    
    print("\nTOP 20 TÍNH NĂNG")
    print(importance.head(20))
    print("\nKẾT QUẢ ĐÁNH GIÁ")
    
    for key, value in metrics.items():
        print(f"{key:<18}: {value:.4f}")

    return predictions, metrics
  
# ==================================================
# THỰC TẾ SO VỚI DỰ ĐOÁN
# ==================================================
def plot_actual_vs_predicted(
    y_test: pd.Series,
    predictions: np.ndarray
) -> None:
    """
    Vẽ biểu đồ Actual vs Predicted.
    """
    print("\nĐang tạo Actual vs Predicted...")

    plt.figure(figsize=(7, 6))
    plt.scatter(
        y_test,
        predictions,
        alpha=0.5,
        color="red",
        edgecolors="black"
    )

    min_value = min(y_test.min(), predictions.min())
    max_value = max(y_test.max(), predictions.max())

    plt.plot(
        [min_value, max_value],
        [min_value, max_value],
        linestyle="--",
        linewidth=2
    )
    plt.grid(True)
    plt.title("Đánh giá Thực tế vs Dự đoán")
    plt.xlabel("Đánh giá thực tế")
    plt.ylabel("Đánh giá dự đoán")
    plt.tight_layout()
    plt.savefig(
        FIGURE_DIR / "actual_vs_predicted.png",
        dpi=300
    )
    plt.close()

    print("Đã lưu actual_vs_predicted.png")

# ==================================================
# BIỂU ĐỒ DƯ
# ==================================================
def plot_residuals(
    y_test: pd.Series,
    predictions: np.ndarray
) -> None:
    """
    Vẽ biểu đồ Residual Plot.
    """
    print("Đang tạo Residual Plot...")

    residuals = y_test - predictions

    plt.figure(figsize=(7, 6))
    plt.scatter(
        predictions,
        residuals,
        alpha=0.6
    )
    plt.axhline(
        y=0,
        linestyle="--",
        linewidth=2
    )
    plt.grid(True)
    plt.title("Biểu đồ phần dư")
    plt.xlabel("Đánh giá dự đoán")
    plt.ylabel("Dư")
    plt.tight_layout()
    plt.savefig(
        FIGURE_DIR / "residual_plot.png",
        dpi=300
    )
    plt.close()

    print("Đã lưu residual_plot.png")
    
def plot_feature_importance(
    model: RandomForestRegressor,
    feature_names: list
):
    """
    Vẽ biểu đồ Feature Importance.
    """

    importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_
    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    ).head(20)

    plt.figure(figsize=(9,7))
    plt.barh(
        importance["Feature"],
        importance["Importance"]
    )
    plt.grid(axis="x",linestyle="--",alpha=0.5)
    plt.title("20 tính năng quan trọng nhất")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(
        FIGURE_DIR / "feature_importance.png",
        dpi=300
    )
    plt.close()

    print("Đã lưu feature_importance.png")    

def plot_residual_distribution(
    y_test,
    predictions
):
    """
    Histogram của Residual.
    """
    residuals = y_test - predictions

    plt.figure(figsize=(8,6))
    plt.hist(
        residuals,
        bins=30
    )
    plt.grid(True)
    plt.title("Phân phối dư")
    plt.xlabel("Dư")
    plt.ylabel("Tần suất")
    plt.tight_layout()
    plt.savefig(
        FIGURE_DIR / "residual_distribution.png",
        dpi=300
    )
    plt.close()

    print("Đã lưu residual_distribution.png")
    
def plot_prediction_error(
    y_test,
    predictions
):
    """
    Vẽ biểu đồ lỗi dự đoán.
    """
    print("Đang tạo Prediction Error...")
    
    errors = np.abs(y_test - predictions)
    
    plt.figure(figsize=(7, 6))
    plt.hist(errors, bins=30, edgecolor="black", alpha=0.7)
    plt.grid(True)
    plt.title("Phân phối lỗi dự đoán")
    plt.xlabel("Sai số tuyệt đối")
    plt.ylabel("Tần suất")
    plt.tight_layout()
    plt.savefig(
        FIGURE_DIR / "prediction_error.png",
        dpi=300
    )
    plt.close()
    
    print("Đã lưu prediction_error.png")

# ==================================================
# LƯU BÁO CÁO
# ==================================================
def save_report(
    metrics: dict,
    output_file: Path,
    runtime
) -> None:
    """
    Lưu báo cáo đánh giá mô hình.
    Parameters
    ----------
    metrics : dict
        Dictionary chứa các chỉ số đánh giá.
    output_file : Path
        Đường dẫn lưu báo cáo.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as file:

            file.write("=" * 60 + "\n")
            file.write("BÁO CÁO ĐÁNH GIÁ MÔ HÌNH\n")
            file.write("=" * 60 + "\n\n")
            file.write("Mô hình\n")
            file.write("-" * 40 + "\n")
            file.write("Bộ hồi quy rừng ngẫu nhiên\n\n")
            file.write("Các chỉ số đánh giá\n")
            file.write("-" * 40 + "\n")
            
            for key,value in metrics.items():
               file.write(
                   f"{key:<20}: {value:.4f}\n"
                )
            file.write("\n")
            file.write("="*60+"\n")
            file.write("TÍNH QUAN TRỌNG HÀNG ĐẦU CỦA TÍNH NĂNG\n")
            file.write("="*60+"\n")

            importance=pd.read_csv(
                REPORT_DIR/"feature_importance.csv"
            )
            for _,row in importance.head(10).iterrows():
                file.write(
                    f"{row['Feature']:<45}"
                    f"{row['Importance']:.6f}\n"
                )
            if metrics["R2 Score"] >= 0.90:
                conclusion = (
                    "Mô hình đạt được hiệu suất dự đoán xuất sắc."
                )
            elif metrics["R2 Score"] >= 0.80:
                conclusion = (
                    "Mô hình đạt được hiệu suất dự đoán tốt."
                )
            elif metrics["R2 Score"] >= 0.70:
                conclusion = (
                    "Mô hình đạt được hiệu suất dự đoán chấp nhận được."
                )
            else:
                conclusion = (
                    "Mô hình cần được cải thiện thêm."
                )

            file.write("Kết luận\n")
            file.write("-" * 40 + "\n")
            file.write(conclusion)
            file.write("\n")
            file.write(
                "Biểu đồ được lưu tại thư mục reports/figures.\n"
            )
            file.write(
                "Tầm quan trọng của tính năng được lưu tại reports/feature_importance.csv\n"
            )
            file.write("\n")
            file.write("-" * 40 + "\n")
            file.write(f"Thời gian chạy: {runtime:.2f} giây\n")
            
        print("\n" + "=" * 60)
        print("LƯU BÁO CÁO")
        print("=" * 60)
        print(f"Đã lưu báo cáo tại: {output_file}")
        
    except Exception as error:
        print(f"Lỗi khi lưu báo cáo: {error}")
        raise

# ==================================================
# HÀM CHÍNH
# ==================================================
def main() -> None:
    """
    Điều khiển toàn bộ quá trình đánh giá mô hình.
    """
    print("=" * 60)
    print("ĐÁNH GIÁ MÔ HÌNH")
    print("=" * 60)
    
    start_time = time.perf_counter()
    # Đọc dữ liệu
    df = load_data(INPUT_FILE)
    # Kiểm tra dữ liệu
    inspect_data(df)
    validate_data(df)
    # Đọc mô hình
    model = load_model(MODEL_FILE)
    # Chuẩn bị dữ liệu test
    X_test, y_test = split_features_target(df)
    # Đánh giá mô hình
    predictions, metrics = evaluate_model(
        model,
        X_test,
        y_test
    )
    # Vẽ biểu đồ
    plot_actual_vs_predicted(
        y_test,
        predictions
    )
    plot_residuals(
        y_test,
        predictions
    )
    plot_feature_importance(
        model,
        X_test.columns
    )
    plot_residual_distribution(
        y_test,
        predictions
    )
    plot_prediction_error(
        y_test,
        predictions
    )
    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    
    # Lưu báo cáo
    save_report(
        metrics,
        REPORT_FILE,
        elapsed_time
    )

    print("\n" + "=" * 60)
    print("ĐÁNH GIÁ MÔ HÌNH HOÀN TẤT")
    print()
    print("Sinh viên  :", "Nguyễn Hữu Đoàn")
    print("Dự án      :", "AI Rating Predictor")
    print("Mẫu        :", "Random Forest Regressor")
    print("Trạng thái : THÀNH CÔNG")
    print("=" * 60)
    print(f"Report : {REPORT_FILE}")
    print(f"Figures: {FIGURE_DIR}")
    print("=" * 60)
    print(f"Thời gian chạy: {elapsed_time:.2f} giây")
    print("=" * 60)
    
# ==================================================
# CHẠY HÀM CHÍNH
# ==================================================
if __name__ == "__main__":
    main()