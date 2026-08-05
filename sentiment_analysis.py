"""
File: sentiment_analysis.py

Description:
    Phân tích cảm xúc (Sentiment Analysis) cho dữ liệu đánh giá ứng dụng
    Google Play Store bằng thư viện NLTK VADER.

Input:
    data/raw/googleplaystore_user_reviews.csv

Output:
    data/processed/reviews_sentiment.csv

Authors:
    - Đỗ Huy Hoàng -

Project:
    AI Rating Predictor
"""

from copy import error
from pathlib import Path

import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer


# ==================================================
# PATH CONFIGURATION
# ==================================================

DATA_DIR = Path("data")

RAW_DIR = DATA_DIR / "raw"

PROCESSED_DIR = DATA_DIR / "processed"

INPUT_FILE = "googleplaystore_user_reviews.csv"

OUTPUT_FILE = PROCESSED_DIR / "reviews_sentiment.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# INITIALIZE NLTK
# ==================================================
def initialize_nltk() -> SentimentIntensityAnalyzer:
    """
    Khởi tạo bộ phân tích cảm xúc VADER.

    Returns
    -------
    SentimentIntensityAnalyzer
        Đối tượng dùng để phân tích cảm xúc.
    """

    try:
        nltk.download("vader_lexicon", quiet=True)
    except Exception as error:
        print(f"Không thể tải VADER Lexicon: {error}")
        raise

    print("\nĐã khởi tạo NLTK VADER.")

    return SentimentIntensityAnalyzer()

# ==================================================
# LOAD DATA
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
        DataFrame chứa dữ liệu đánh giá.
    """

    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise ValueError("Dataset rỗng.")

        print("=" * 60)
        print("ĐỌC DỮ LIỆU THÀNH CÔNG")
        print("=" * 60)

        print(f"Số dòng : {df.shape[0]}")
        print(f"Số cột  : {df.shape[1]}")

        return df

    except FileNotFoundError:
        print(f"\nKhông tìm thấy file: {file_path}")
        raise

    except Exception as error:
        print(f"\nLỗi khi đọc dữ liệu: {error}")
        raise

# ==================================================
# CLEAN REVIEWS
# ==================================================
def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Làm sạch dữ liệu đánh giá.

    Thực hiện:
    - Xóa giá trị thiếu
    - Xóa khoảng trắng đầu và cuối
    - Xóa review rỗng
    - Xóa App bị thiếu

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """

    print("\nĐang làm sạch dữ liệu đánh giá...")

    df = df.copy()

    required_columns = ["App", "Translated_Review"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Không tìm thấy cột '{column}'.")

    initial_rows = len(df)

    df = df.dropna(subset=["App", "Translated_Review"])
    
    df["Translated_Review"] = (
        df["Translated_Review"]
        .astype(str)
        .str.strip()
    )

    df = df[df["Translated_Review"] != ""]
    df = df.reset_index(drop=True)
    
    removed_rows = initial_rows - len(df)

    print(f"Đã loại bỏ {removed_rows} dòng không hợp lệ.")

    print(f"Còn lại {len(df)} dòng.")

    return df

# ==================================================
# CALCULATE SENTIMENT
# ==================================================
def calculate_sentiment(
    text: str,
    analyzer: SentimentIntensityAnalyzer
) -> dict:
    """
    Tính điểm cảm xúc cho một đoạn văn.

    Parameters
    ----------
    text : str
        Nội dung đánh giá.

    analyzer : SentimentIntensityAnalyzer
        Bộ phân tích cảm xúc.

    Returns
    -------
    dict
        Dictionary chứa các điểm cảm xúc.
    """

    return analyzer.polarity_scores(str(text))

# ==================================================
# GET SENTIMENT LABEL
# ==================================================

def get_sentiment_label(compound_score: float) -> str:
    """
    Chuyển điểm Compound thành nhãn cảm xúc.

    Parameters
    ----------
    compound_score : float
        Điểm Compound do VADER trả về.

    Returns
    -------
    str
        Positive, Neutral hoặc Negative.
    """

    if compound_score >= 0.05:
        return "Positive"

    if compound_score <= -0.05:
        return "Negative"

    return "Neutral"

# ==================================================
# PROCESS SENTIMENT
# ==================================================
def process_sentiment(
    df: pd.DataFrame,
    analyzer: SentimentIntensityAnalyzer
) -> pd.DataFrame:
    """
    Phân tích cảm xúc cho toàn bộ dữ liệu.

    Parameters
    ----------
    df : pd.DataFrame

    analyzer : SentimentIntensityAnalyzer

    Returns
    -------
    pd.DataFrame
        DataFrame sau khi thêm các cột cảm xúc.
    """

    print("\nĐang phân tích cảm xúc...")

    sentiment_scores = df["Translated_Review"].apply(
        calculate_sentiment,
        analyzer=analyzer
    )

    sentiment_df = sentiment_scores.apply(pd.Series)

    sentiment_df.columns = [
        "Negative",
        "Neutral",
        "Positive",
        "Compound"
    ]

    df = pd.concat(
        [df.reset_index(drop=True),
         sentiment_df.reset_index(drop=True)],
        axis=1
    )

    df["Sentiment"] = df["Compound"].apply(get_sentiment_label)

    print("Đã hoàn thành phân tích cảm xúc.")

    return df

# ==================================================
# SAVE DATA
# ==================================================
def save_data(
    df: pd.DataFrame,
    output_path: Path
) -> None:
    """
    Lưu dữ liệu ra file CSV.

    Parameters
    ----------
    df : pd.DataFrame

    output_path : Path
    """

    try:
        df.to_csv(output_path, index=False)

        print("\nĐã lưu dữ liệu thành công.")

        print(f"Đường dẫn: {output_path}")

    except Exception as error:
        print(f"\nLỗi khi lưu dữ liệu: {error}")
        raise

# ==================================================
# MAIN
# ==================================================
def main() -> None:
    """
    Hàm điều khiển toàn bộ chương trình.
    """

    print("=" * 60)
    print("SENTIMENT ANALYSIS")
    print("=" * 60)

    analyzer = initialize_nltk()

    df = load_data(INPUT_FILE)

    df = clean_reviews(df)

    df = process_sentiment(df, analyzer)

    print("\nThông tin dữ liệu:")

    df.info()
    
    print("\nPhân bố cảm xúc:")
    print(df["Sentiment"].value_counts())
    
    print("\nKích thước dữ liệu:")
    print(df.shape)

    print("\nPhân bố Sentiment:")
    print(df["Sentiment"].value_counts())

    print("\n5 dòng đầu tiên:")

    print(df.head())

    save_data(df, OUTPUT_FILE)

    print("\nHoàn thành chương trình.")


# ==================================================
# START PROGRAM
# ==================================================

if __name__ == "__main__":
    main()