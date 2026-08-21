"""
File: feature_engineering.py

Description:
    Thực hiện Feature Engineering cho bộ dữ liệu Google Play Store
    sau khi hoàn thành tiền xử lý, phân tích cảm xúc và gộp dữ liệu.

    Module này chuẩn bị dữ liệu đầu vào cho mô hình
    Random Forest Regressor bằng cách lựa chọn đặc trưng,
    mã hóa biến phân loại và tạo bộ dữ liệu phục vụ huấn luyện.

Input:
    data/processed/googleplaystore_merged.csv

Output:
    data/processed/googleplaystore_features.csv

Authors:
    - Đỗ Huy Hoàng -

Project:
    AI Rating Predictor
"""

from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

import pandas as pd
import numpy as np

# ==================================================
# CẤU HÌNH ĐƯỜNG DẪN
# ==================================================
DATA_DIR = Path("data")

PROCESSED_DIR = DATA_DIR / "processed"

INPUT_FILE = PROCESSED_DIR / "googleplaystore_merged.csv"

OUTPUT_FILE = PROCESSED_DIR / "googleplaystore_features.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# TẢI DỮ LIỆU
# ==================================================
def load_data(file_path: Path) -> pd.DataFrame:
    """
    Đọc dữ liệu từ file CSV.

    Parameters
    ----------
    file_path : Path
        Đường dẫn tới file dữ liệu.

    Returns
    -------
    pd.DataFrame
        DataFrame chứa dữ liệu sau khi Hợp nhất.
    """

    try:

        df = pd.read_csv(file_path)

        print("=" * 60)
        print("KỸ THUẬT TÍNH NĂNG - TẢI DỮ LIỆU")
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
    Hiển thị thông tin tổng quan của dữ liệu.
    """

    print("\n" + "=" * 60)
    print("TỔNG QUAN DỮ LIỆU")
    print("=" * 60)

    print("\nHình dạng dữ liệu (số dòng, số cột)")
    print(df.shape)

    print("\nCác cột")
    print(df.columns.tolist())

    print("\nLoại dữ liệu")
    print(df.dtypes)

    print("\nGiá trị bị thiếu")
    print(df.isnull().sum())

    print("\n5 hàng đầu tiên")
    print(df.head())

    print("\n5 hàng cuối cùng")
    print(df.tail())

    print("\nThông tin dữ liệu")
    df.info()
    
# ==================================================
# CHỌN TÍNH NĂNG
# ==================================================
def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lựa chọn các đặc trưng phục vụ huấn luyện mô hình.

    Returns
    -------
    pd.DataFrame
        DataFrame chỉ chứa các đặc trưng cần thiết.
    """

    print("\n" + "=" * 60)
    print("CHỌN TÍNH NĂNG")
    print("=" * 60)

    selected_columns = [
        "Reviews",
        "Installs",
        "Price",
        "Size",
        "Category",
        "Type",
        "Content Rating",
        "Genres",
        "Avg_Compound",
        "Sentiment",
        "Rating"
    ]

    missing_columns = [
        column
        for column in selected_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Thiếu các cột: {missing_columns}"
        )

    feature_df = df[selected_columns].copy()
    
    print("\nThống kê Xếp hạng")
    print(feature_df["Rating"].describe())
    
    print("Các đặc trưng được sử dụng:")
    print("\nPhân bố Cảm xúc")
    print(feature_df["Sentiment"].value_counts(dropna=False))
    for column in feature_df.columns:
        print(f"- {column}")

    return feature_df


# ==================================================
# MÃ HÓA CÁC TÍNH NĂNG
# ==================================================
def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mã hóa các biến phân loại bằng One-Hot Encoding.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        DataFrame sau khi mã hóa.
    """

    print("\n" + "=" * 60)
    print("MÃ HÓA CÁC TÍNH NĂNG")
    print("=" * 60)

    categorical_columns = [
        "Category",
        "Type",
        "Content Rating",
        "Genres",
        "Sentiment"
    ]

    numeric_columns = [
        "Reviews",
        "Installs",
        "Price",
        "Size",
        "Avg_Compound"
    ]

    encoder = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                ),
                categorical_columns
            )
        ],
        remainder="passthrough"
    )
    
    encoded_array = encoder.fit_transform(
        df.drop(columns=["Rating"])
    )

    encoded_columns = encoder.named_transformers_[
        "categorical"
    ].get_feature_names_out(categorical_columns)

    feature_names = list(encoded_columns) + numeric_columns

    encoded_df = pd.DataFrame(
        encoded_array,
        columns=feature_names
    )
    
    encoded_df.reset_index(drop=True, inplace=True)
    
    encoded_df["Rating"] = (
        df["Rating"]
        .reset_index(drop=True)
    )
    
    print("\nSau Mã hóa")
    print(encoded_df.head())
    print(encoded_df.shape)
    
    print("\nDữ liệu thiếu sau Mã hóa")
    print(encoded_df.isnull().sum())
    
    print(f"Số lượng đặc trưng sau Mã hóa: {encoded_df.shape[1]-1}")
    print("\nCác tính năng sau mã hóa:")

    for column in encoded_df.columns:
        print(column)
    return encoded_df

# ==================================================
# KỸ THUẬT TÍNH NĂNG
# ==================================================
def feature_engineering(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Thực hiện toàn bộ quá trình Feature Engineering.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        Bộ dữ liệu sau Feature Engineering.
    """

    print("\n" + "=" * 60)
    print("KỸ THUẬT TÍNH NĂNG")
    print("=" * 60)

    df = select_features(df)
    df = encode_features(df)

    print("\nDữ liệu thiếu trước xử lý")
    print(df.isnull().sum())
    
    df.replace([np.inf, -np.inf],0,inplace=True)
    df.fillna(0, inplace=True)
    
    print("\nDữ liệu thiếu sau xử lý")
    print(df.isnull().sum())
    print(df.shape)
    
    if df.isnull().sum().sum() == 0:

        print("\n✓ Dữ liệu sẵn sàng cho Học máy")

    else:

        print("\n✗ Dữ liệu vẫn còn dữ liệu thiếu")
    
    return df

def validate_data(df: pd.DataFrame) -> None:

    print("="*60)
    print("XÁC THỰC DỮ LIỆU")
    print("="*60)

    print("Shape :",df.shape)
    print("Missing :",df.isnull().sum().sum())
    print("Duplicate :",df.duplicated().sum())
    print("Infinity :",
          np.isinf(df.select_dtypes(include="number")).sum().sum())
    
    print("\nCác kiểu dữ liệu")
    print(df.dtypes)
    
    print("\nMức sử dụng bộ nhớ")
    print(df.memory_usage(deep=True).sum()/1024**2,"MB")
    
# ==================================================
# LƯU DỮ LIỆU
# ==================================================
def save_data(
    df: pd.DataFrame,
    output_file: Path
) -> None:
    """
    Lưu bộ dữ liệu sau Feature Engineering.

    Parameters
    ----------
    df : pd.DataFrame

    output_file : Path
    """

    try:
        validate_data(df)
        
        print("\nKiểm tra Missing trước khi lưu")
        print(df.isnull().sum().sum())

        df.to_csv(output_file, index=False)

        print("\n" + "=" * 60)
        print("LƯU BỘ DỮ LIỆU TÍNH NĂNG")
        print("=" * 60)

        print(f"Đã lưu dữ liệu tại: {output_file}")

    except Exception as error:

        print(f"Lỗi khi lưu dữ liệu: {error}")

        raise

# ==================================================
# HÀM CHÍNH
# ==================================================
def main() -> None:
    """
    Điều khiển toàn bộ quá trình Feature Engineering.
    """

    print("=" * 60)
    print("KỸ THUẬT TÍNH NĂNG")
    print("=" * 60)

    # Đọc dữ liệu
    df = load_data(INPUT_FILE)

    print(df.columns.tolist())
    
    # Kiểm tra dữ liệu
    inspect_data(df)

    # Thực hiện Feature Engineering
    feature_df = feature_engineering(df)
    validate_data(feature_df)
    
    print("\n" + "=" * 60)
    print("BỘ DỮ LIỆU TÍNH NĂNG")
    print("=" * 60)

    print(f"Kích thước dữ liệu : {feature_df.shape}")

    print("\nKiểu dữ liệu:")

    print(feature_df.dtypes)

    print("\nSố lượng giá trị thiếu:")

    print(feature_df.isnull().sum())

    print("\n5 dòng đầu:")

    print(feature_df.head())

    save_data(feature_df, OUTPUT_FILE)

    print("\nHoàn thành Feature Engineering.")

# ==================================================
# CHẠY HÀM CHÍNH
# ==================================================

if __name__ == "__main__":
    main()