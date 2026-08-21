"""
File: merge_dataset.py

Description:
    Gộp (Merge) dữ liệu ứng dụng Google Play Store với dữ liệu
    phân tích cảm xúc (Sentiment Analysis) để tạo bộ dữ liệu
    hoàn chỉnh phục vụ EDA và huấn luyện mô hình Machine Learning.

Input:
    data/processed/googleplaystore_cleaned.csv
    data/processed/reviews_sentiment.csv

Output:
    data/processed/googleplaystore_merged.csv

Authors:
    - Đỗ Huy Hoàng -
    
Project:
    AI Rating Predictor
"""

from pathlib import Path

import pandas as pd

# ==================================================
# CẤU HÌNH ĐƯỜNG DẪN
# ==================================================
DATA_DIR = Path("data")

PROCESSED_DIR = DATA_DIR / "processed"

APPS_FILE = PROCESSED_DIR / "googleplaystore_cleaned.csv"

REVIEWS_FILE = PROCESSED_DIR / "reviews_sentiment.csv"

OUTPUT_FILE = PROCESSED_DIR / "googleplaystore_merged.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# TẢI DỮ LIỆU ỨNG DỤNG
# ==================================================
def load_apps_data(file_path: Path) -> pd.DataFrame:
    """
    Đọc dữ liệu ứng dụng đã làm sạch.

    Parameters
    ----------
    file_path : Path

    Returns
    -------
    pd.DataFrame
    """

    try:

        df = pd.read_csv(file_path)

        print("=" * 60)
        print("ĐỌC DỮ LIỆU ỨNG DỤNG")
        print("=" * 60)

        print(f"Số dòng : {df.shape[0]}")
        print(f"Số cột  : {df.shape[1]}")

        return df

    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        raise

    except Exception as error:
        print(error)
        raise

# ==================================================
# TẢI DỮ LIỆU ĐÁNH GIÁ
# ==================================================
def load_reviews_data(file_path: Path) -> pd.DataFrame:
    """
    Đọc dữ liệu sentiment.

    Parameters
    ----------
    file_path : Path

    Returns
    -------
    pd.DataFrame
    """

    try:

        df = pd.read_csv(file_path)

        print("\n" + "=" * 60)
        print("ĐỌC DỮ LIỆU SENTIMENT")
        print("=" * 60)

        print(f"Số dòng : {df.shape[0]}")
        print(f"Số cột  : {df.shape[1]}")

        return df

    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        raise

    except Exception as error:
        print(error)
        raise

# ==================================================
# CẢM XÚC THƯỜNG GẶP NHẤT
# ==================================================
def most_frequent_sentiment(series: pd.Series) -> str:
    """
    Lấy giá trị Sentiment xuất hiện nhiều nhất.

    Parameters
    ----------
    series : pd.Series

    Returns
    -------
    str
    """

    mode = series.mode()

    if mode.empty:
        return "Neutral"

    return mode.iloc[0]

# ==================================================
# TỔNG HỢP CẢM XÚC
# ==================================================
def aggregate_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tổng hợp điểm cảm xúc theo từng ứng dụng.

    Returns
    -------
    pd.DataFrame
    """

    print("\nĐang tổng hợp dữ liệu cảm xúc...")

    sentiment_summary = (
        df.groupby("App")
        .agg(
            Avg_Compound=("Compound", "mean"),
            Avg_Positive=("Positive", "mean"),
            Avg_Neutral=("Neutral", "mean"),
            Avg_Negative=("Negative", "mean"),
            Sentiment=("Sentiment", most_frequent_sentiment),
            Positive_Count=("Sentiment",
                            lambda x: (x == "Positive").sum()),
            Neutral_Count=("Sentiment",
                           lambda x: (x == "Neutral").sum()),
            Negative_Count=("Sentiment",
                            lambda x: (x == "Negative").sum()),
            Total_Reviews=("Sentiment", "count")
        )
        .reset_index()
    )

    print("Đã tổng hợp dữ liệu thành công.")

    return sentiment_summary

# ==================================================
# HỢP NHẤT TẬP DỮ LIỆU
# ==================================================
def merge_datasets(
    apps_df: pd.DataFrame,
    sentiment_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Gộp hai bộ dữ liệu theo cột App.

    Returns
    -------
    pd.DataFrame
    """

    print("\nĐang gộp dữ liệu...")

    merged_df = pd.merge(
        apps_df,
        sentiment_df,
        on="App",
        how="left"
    )

    sentiment_columns = [
        "Avg_Compound",
        "Avg_Positive",
        "Avg_Neutral",
        "Avg_Negative",
        "Positive_Count",
        "Neutral_Count",
        "Negative_Count",
        "Total_Reviews"
    ]

    merged_df["Sentiment"] = (
        merged_df["Sentiment"]
            .fillna("Unknown")
    )

    print("Đã gộp dữ liệu thành công.")

    return merged_df

# ==================================================
# KIỂM TRA DỮ LIỆU
# ==================================================
def inspect_data(df: pd.DataFrame) -> None:
    """
    Kiểm tra dữ liệu sau khi merge.
    """

    print("\n" + "=" * 60)
    print("THÔNG TIN DỮ LIỆU SAU KHI MERGE")
    print("=" * 60)

    print(f"Kích thước dữ liệu : {df.shape}")

    print("\nKiểu dữ liệu:")

    print(df.dtypes)

    print("\nSố lượng giá trị thiếu:")

    print(df.isnull().sum())

    print("\n5 dòng đầu:")

    print(df.head())
    
    print("\nPhân bố Sentiment:")

    print(df["Sentiment"].value_counts())

# ==================================================
# LƯU DỮ LIỆU
# ==================================================
def save_data(
    df: pd.DataFrame,
    output_path: Path
) -> None:
    """
    Lưu dữ liệu sau khi merge.
    """

    try:

        df.to_csv(output_path, index=False)

        print("\n" + "=" * 60)
        print("LƯU DỮ LIỆU")
        print("=" * 60)

        print(f"Đã lưu tại: {output_path}")

    except Exception as error:
        print(error)
        raise

# ==================================================
# HÀM CHÍNH
# ==================================================
def main() -> None:
    """
    Điều khiển toàn bộ chương trình.
    """

    print("=" * 60)
    print("MERGE DATASET")
    print("=" * 60)

    apps_df = load_apps_data(APPS_FILE)

    reviews_df = load_reviews_data(REVIEWS_FILE)

    sentiment_df = aggregate_sentiment(reviews_df)

    merged_df = merge_datasets(
        apps_df,
        sentiment_df
    )

    inspect_data(merged_df)

    save_data(
        merged_df,
        OUTPUT_FILE
    )

    print("\nHoàn thành chương trình.")

# ==================================================
# KHỞI ĐỘNG CHƯƠNG TRÌNH
# ==================================================
if __name__ == "__main__":
    main()