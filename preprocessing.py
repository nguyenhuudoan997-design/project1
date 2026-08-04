"""
File: preprocessing.py

Description:
    Tiền xử lý dữ liệu Google Play Store.

    Chức năng:
    - Đọc dữ liệu
    - Kiểm tra dữ liệu
    - Xóa dòng dữ liệu lỗi
    - Làm sạch Reviews
    - Làm sạch Installs
    - Làm sạch Price
    - Làm sạch Size
    - Xử lý Missing Values
    - Xóa dữ liệu trùng lặp
    - Lưu dữ liệu đã làm sạch

Input:
    data/raw/googleplaystore.csv

Output:
    data/processed/googleplaystore_cleaned.csv

Authors:
    - Nguyễn Hữu Đoàn

Project:
    AI Rating Predictor
"""

from pathlib import Path
import numpy as np
import pandas as pd

# ==================================================
# CẤU HÌNH ĐƯỜNG DẪN
# ==================================================
DATA_DIR = Path("data")

RAW_DIR = DATA_DIR / "raw"

PROCESSED_DIR = DATA_DIR / "processed"

INPUT_FILE = RAW_DIR / "googleplaystore.csv"

OUTPUT_FILE = PROCESSED_DIR / "googleplaystore_cleaned.csv"

# Tạo thư mục processed nếu chưa tồn tại
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# ĐỌC DỮ LIỆU
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
        DataFrame chứa dữ liệu.
    """

    try:
        df = pd.read_csv(file_path)

        print("=" * 60)
        print("BƯỚC 1: ĐỌC DỮ LIỆU")
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
    print("THÔNG TIN DỮ LIỆU")
    print("=" * 60)

    print("\nDanh sách cột:")
    print(df.columns.tolist())

    print("\nKiểu dữ liệu:")
    print(df.dtypes)

    print("\nThông tin chi tiết:")
    df.info()

    print("\nGiá trị thiếu:")
    print(df.isnull().sum())

    print("\n5 dòng đầu:")
    print(df.head())

# ==================================================
# XÓA DỮ LIỆU LỖI
# ==================================================
def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Xóa dòng dữ liệu bị lỗi trong bộ Google Play Store.
    """

    before = len(df)

    df = df[df["Category"] != "1.9"]

    after = len(df)

    print(f"\nĐã xóa {before - after} dòng dữ liệu lỗi.")

    return df

# ==================================================
# LÀM SẠCH REVIEWS
# ==================================================
def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuyển cột Reviews sang kiểu số.
    """

    df["Reviews"] = pd.to_numeric(
        df["Reviews"],
        errors="coerce"
    )

    print("Đã chuyển Reviews sang kiểu số.")
    
    return df


# ==================================================
# LÀM SẠCH INSTALLS
# ==================================================

def clean_installs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuyển cột Installs sang kiểu số.
    """

    df["Installs"] = (
        df["Installs"]
        .astype(str)
        .str.strip()
        .str.replace(",", "", regex=False)
        .str.replace("+", "", regex=False)
    )

    df["Installs"] = pd.to_numeric(
        df["Installs"],
        errors="coerce"
    )
    print("Đã làm sạch Installs.")
    
    return df

# ==================================================
# LÀM SẠCH PRICE
# ==================================================
def clean_price(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuyển cột Price sang kiểu số thực.
    """

    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.strip()
        .str.replace("$", "", regex=False)
    )

    df["Price"] = pd.to_numeric(
        df["Price"],
        errors="coerce"
    )
    print("Đã làm sạch Price.")
    return df

# ==================================================
# LÀM SẠCH SIZE
# ==================================================
def convert_size(size: str) -> float:
    """
    Chuyển đổi cột Size về đơn vị MB.

    Ví dụ:
        19M -> 19.0
        850k -> 0.85
        Varies with device -> NaN
    """

    if pd.isna(size):
        return np.nan

    size = str(size).strip()

    if size == "Varies with device":
        return np.nan

    try:
        
        size = size.replace(",", ".")
        
        if size.endswith("M"):
            return float(size[:-1])

        if size.endswith("k"):
            return float(size[:-1]) / 1000

    except ValueError:
        return np.nan

    return np.nan

# ==================================================
# LÀM SẠCH SIZE
# ==================================================

def clean_size(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuyển cột Size về đơn vị MB.
    """

    df["Size"] = df["Size"].astype(str).str.strip()
    df["Size"] = df["Size"].apply(convert_size)

    print("Đã làm sạch Size.")
    return df

# ==================================================
# XỬ LÝ GIÁ TRỊ THIẾU
# ==================================================
def remove_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Xóa các dòng chứa giá trị thiếu ở những cột quan trọng.
    """

    before = len(df)

    df = df.dropna(
        subset=[
            "Rating",
            "Type",
            "Content Rating",
            "Current Ver",
            "Android Ver",
            "Reviews",
            "Installs",
            "Price",
            "Size",
        ]
    )

    after = len(df)

    print(f"Đã xóa {before - after} dòng chứa Missing Value.")

    return df

# ==================================================
# XÓA DỮ LIỆU TRÙNG LẶP
# ==================================================
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Xóa các ứng dụng bị trùng tên.
    """

    before = len(df)

    df = df.drop_duplicates(
    subset=["App"],
    keep="first"
    )

    after = len(df)

    print(f"Đã xóa {before - after} dòng trùng lặp.")

    return df

# ==================================================
# LƯU DỮ LIỆU
# ==================================================
def save_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Lưu dữ liệu đã làm sạch ra file CSV.
    """

    try:
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        df.to_csv(
            output_path,
            index=False,
            encoding="utf-8-sig"
        )

        print("\n" + "=" * 60)
        print("LƯU DỮ LIỆU")
        print("=" * 60)
        print(f"Đã lưu dữ liệu tại: {output_path}")

    except Exception as error:
        print(f"Lỗi khi lưu file: {error}")
        raise

# ==================================================
# HÀM CHÍNH
# ==================================================
def main() -> None:
    """
    Điều khiển toàn bộ quy trình tiền xử lý dữ liệu.
    """
    df = load_data(INPUT_FILE)

    inspect_data(df)

    df = remove_invalid_rows(df)

    print("\nLàm sạch Reviews...")
    df = clean_reviews(df)

    print("Làm sạch Installs...")
    df = clean_installs(df)

    print("Làm sạch Price...")
    df = clean_price(df)

    print("Làm sạch Size...")
    df = clean_size(df)

    df = remove_missing_values(df)

    df = remove_duplicates(df)

    print("\n" + "=" * 60)
    print("KẾT QUẢ SAU KHI LÀM SẠCH")
    print("=" * 60)

    print(f"Kích thước dữ liệu: {df.shape}")

    print("\nKiểu dữ liệu:")
    print(df.dtypes)

    print("\nGiá trị thiếu còn lại:")
    print(df.isnull().sum())

    print("\n5 dòng đầu:")
    print(df.head())

    save_data(df, OUTPUT_FILE)

    print("\nHoàn thành quá trình tiền xử lý dữ liệu.")


# ==================================================
# ĐIỂM BẮT ĐẦU CHƯƠNG TRÌNH
# ==================================================

if __name__ == "__main__":
    main()