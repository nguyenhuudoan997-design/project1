"""
File: eda.py

Description:
    Thực hiện phân tích khám phá dữ liệu (Exploratory Data Analysis - EDA)
    cho bộ dữ liệu Google Play Store sau khi đã tiền xử lý và gộp dữ liệu
    cảm xúc.

Input:
    data/processed/googleplaystore_merged.csv

Output:
    reports/eda_summary.txt
    reports/figures/*.png

Authors:
    - Nguyễn Hữu Đoàn -

Project:
    AI Rating Predictor
"""
from pathlib import Path
import statistics
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ==================================================
# CẤU HÌNH ĐƯỜNG DẪN
# ==================================================
DATA_DIR = Path("data")

PROCESSED_DIR = DATA_DIR / "processed"

REPORT_DIR = Path("reports")

FIGURE_DIR = REPORT_DIR / "figures"

INPUT_FILE = PROCESSED_DIR / "googleplaystore_merged.csv"

REPORT_FILE = REPORT_DIR / "eda_summary.txt"

# Tạo thư mục nếu chưa tồn tại
REPORT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# DỮ LIỆU TẢI VÀO
# ==================================================
def load_data(file_path: Path) -> pd.DataFrame:
    """
    Đọc dữ liệu từ file CSV.
    
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
        print("EDA - LOAD DATA")
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
    print("DATA OVERVIEW")
    print("=" * 60)

    print("\nShape")

    print(f"Số dòng : {df.shape[0]}")
    print(f"Số cột  : {df.shape[1]}")

    print("\nDanh sách cột")

    print(df.columns.tolist())

    print("\nKiểu dữ liệu")

    print(df.dtypes)

    print("\nMissing Values")

    print(df.isnull().sum())

    print("\nFirst 5 Rows")

    print(df.head())

    print("\nLast 5 Rows")

    print(df.tail())

    print("\nThông tin dữ liệu")

    df.info()

# ==================================================
# THỐNG KÊ MÔ TẢ
# ==================================================
def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Hiển thị thống kê mô tả.
    """

    print("\n" + "=" * 60)
    print("THỐNG KÊ MÔ TẢ")
    print("=" * 60)

    print(df.describe(include="all"))
    
    statistics = df.describe(include="all")

    print(statistics)

    return statistics
# ==================================================
# PHÂN TÍCH GIÁ TRỊ BỊ THIẾU
# ==================================================
def analyze_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Thống kê Missing Value.
    """

    missing = pd.DataFrame(
        {
            "Missing Count": df.isnull().sum(),
            "Missing Percent": (
                df.isnull().sum() / len(df) * 100
            ).round(2),
        }
    )

    print("\n" + "=" * 60)

    print("PHÂN TÍCH GIÁ TRỊ BỊ THIẾU")

    print("=" * 60)

    print(missing)

    return missing

# ==================================================
# PHÂN TÍCH DỮ LIỆU TRÙNG LẶP
# ==================================================
def analyze_duplicates(df: pd.DataFrame) -> int:
    """
    Đếm số lượng dữ liệu trùng.
    """

    duplicate_count = df.duplicated().sum()

    print("\n" + "=" * 60)

    print("BẢN SAO TRÙNG LẶP")

    print("=" * 60)

    print(f"Số lượng dòng trùng lặp: {duplicate_count}")

    return duplicate_count

# ==================================================
#LƯU BÁO CÁO EDA
# ==================================================
def save_report(
    df: pd.DataFrame,
    missing_df: pd.DataFrame,
    duplicate_count: int,
    output_file: Path
) -> None:
    """
    Lưu kết quả phân tích EDA
    ra file báo cáo.

    Parameters
    ----------
    df : pd.DataFrame

    missing_df : pd.DataFrame

    duplicate_count : int

    output_file : Path
    Returns
    -------
    None
    """

    try:

        with open(output_file, "w", encoding="utf-8") as file:

            file.write("=" * 60 + "\n")

            file.write("BÁO CÁO TỔNG QUAN EDA\n")

            file.write("=" * 60 + "\n\n")

            file.write(
                f"Rows    : {df.shape[0]}\n"
            )

            file.write(
                f"Cột : {df.shape[1]}\n\n"
            )

            file.write("Cột\n")

            file.write("-" * 40 + "\n")

            for column in df.columns:

                file.write(f"{column}\n")

            file.write("\n")

            file.write("Các kiểu dữ liệu\n")

            file.write("-" * 40 + "\n")

            file.write(df.dtypes.to_string())

            file.write("\n\n")

            file.write("Giá trị bị thiếu\n")

            file.write("-" * 40 + "\n")

            file.write(missing_df.to_string())

            file.write("\n\n")

            file.write(f"Các hàng trùng lặp: {duplicate_count}\n\n")

            file.write("Thống kê mô tả\n")

            file.write("-" * 40 + "\n")

            statistics = df.describe(include="all")

            file.write(statistics.to_string())
            
            file.write("\n\n")

            file.write("=" * 60)
            
            file.write("\n\n")

            file.write("=" * 60 + "\n")

            file.write("PHÂN TÍCH CHIẾN LƯỢC GIÁ\n")

            file.write("=" * 60 + "\n")

            correlation = df["Price"].corr(df["Rating"])

            file.write(
            f"Hệ số tương quan (Giá vs Xếp hạng): {correlation:.4f}\n\n"
            )

            free_mean = df[df["Price"] == 0]["Rating"].mean()

            paid_mean = df[df["Price"] > 0]["Rating"].mean()

            file.write(
    f"Average Rating (Free): {free_mean:.2f}\n"
)

            file.write(
                f"Đánh giá trung bình (Trả phí): {paid_mean:.2f}\n"
            )
            
            file.write("\n\n")

            file.write("=" * 60 + "\n")
            file.write("PHÂN TÍCH CHIẾN LƯỢC GIÁ\n")
            file.write("=" * 60 + "\n\n")

            correlation = price_rating_correlation(df)

            file.write(f"Hệ số tương quan (Giá - Xếp hạng): {correlation:.4f}\n\n")

            file.write(analyze_price_strategy(df))
            file.write("\n\n")

            file.write(analyze_developer_insight(df))
            file.write("\n\n")

            file.write(analyze_admin_recommendation(df))
            
            file.write("\n KẾT THÚC BÁO CÁO\n")
        print("\nĐã lưu báo cáo EDA.")

        print(f"Đường dẫn: {output_file}")

    except Exception as error:

        print(f"Lỗi khi lưu báo cáo: {error}")

        raise
    
# ==================================================
# PHÂN TÍCH PHÂN PHỐI XẾP HẠNG
# ==================================================
def plot_rating_distribution(df: pd.DataFrame) -> None:
    """
    Vẽ biểu đồ phân bố Rating.
    """

    print("\nĐang tạo biểu đồ Rating...")

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["Rating"],
        bins=20,
        edgecolor="black",
        color="skyblue"
    )

    plt.title("PHÂN PHỐI XẾP HẠNG")

    plt.xlabel("Rating")

    plt.ylabel("Frequency")
    
    plt.grid(alpha=0.3)
    
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "rating_distribution.png",
        dpi=300
    )

    plt.close()
    
    print("Đã lưu rating_distribution.png")
    
# ==================================================
# PHÂN TÍCH LOẠI
# ==================================================
def plot_category_distribution(df: pd.DataFrame) -> None:
    """
    Vẽ Top 10 Category.
    """

    print("Đang tạo biểu đồ Category...")

    category = (
        df["Category"]
        .value_counts()
        .head(10)
    )

    plt.figure(figsize=(10, 6))

    category.plot(
        kind="bar"
    )

    plt.title("Top 10 Categories")

    plt.xlabel("Category")

    plt.ylabel("Number of Apps")
    
    plt.grid(axis="y", alpha=0.3)
    
    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "category_distribution.png",
        dpi=300
    )

    plt.close()

    print("Đã lưu category_distribution.png")
    
# ==================================================
# PHÂN TÍCH LOẠI ỨNG DỤNG (FREE/PAID)
# ==================================================
def plot_type_distribution(df: pd.DataFrame) -> None:
    """
    Vẽ biểu đồ số lượng ứng dụng Free và Paid.
    """

    print("Đang tạo biểu đồ Type...")

    type_counts = df["Type"].value_counts()

    plt.figure(figsize=(6, 5))

    type_counts.plot(
        kind="bar",
        edgecolor="black"
    )

    plt.title("Phân phối loại ứng dụng")

    plt.xlabel("Type")

    plt.ylabel("Number of Apps")

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "type_distribution.png",
        dpi=300
    )

    plt.close()   

    print("Đã lưu type_distribution.png")

# ==================================================
# PHÂN TÍCH CẢM XÚC
# ==================================================
def plot_sentiment_distribution(df: pd.DataFrame) -> None:
    """
    Vẽ biểu đồ phân bố Sentiment.
    """

    if "Sentiment" not in df.columns:

        return

    print("Đang tạo biểu đồ Sentiment...")

    sentiment = df["Sentiment"].value_counts()

    plt.figure(figsize=(6, 5))

    sentiment.plot(kind="bar")

    plt.title("PHÂN BỐ CẢM XÚC")

    plt.xlabel("Sentiment")

    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "sentiment_distribution.png",
        dpi=300
    )

    plt.close()

    print("Đã lưu sentiment_distribution.png")

# ==================================================
# PHÂN TÍCH ĐÁNH GIÁ
# ==================================================
def plot_reviews_distribution(df: pd.DataFrame) -> None:
    """
    Vẽ biểu đồ Reviews.
    """

    print("Đang tạo biểu đồ Reviews...")

    plt.figure(figsize=(8, 5))

    plt.hist(
        np.log1p(df["Reviews"]),
        bins=30,
        edgecolor="black"
    )

    plt.title("PHÂN BỐ ĐÁNH GIÁ (Log Scale)")

    plt.xlabel("log(Reviews + 1)")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "reviews_distribution.png",
        dpi=300
    )

    plt.close()

    print("Đã lưu reviews_distribution.png")

# ==================================================
# PHÂN TÍCH CÀI ĐẶT
# ==================================================
def plot_installs_distribution(df: pd.DataFrame) -> None:
    """
    Vẽ biểu đồ Installs.
    """

    print("Đang tạo biểu đồ Installs...")

    plt.figure(figsize=(8, 5))

    plt.hist(
        np.log1p(df["Installs"]),
        bins=30,
        edgecolor="black"
    )

    plt.grid(alpha=0.3)

    plt.title("PHÂN BỐ CÀI ĐẶT (Log Scale)")

    plt.xlabel("log(Installs + 1)")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "installs_distribution.png",
        dpi=300
    )

    plt.close()

    print("Đã lưu installs_distribution.png")

# ==================================================
# PHÂN TÍCH GIÁ CẢ
# ==================================================
def plot_price_distribution(df: pd.DataFrame) -> None:
    """
    Vẽ biểu đồ Price.
    """

    print("Đang tạo biểu đồ Price...")

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["Price"],
        bins=30,
        edgecolor="black"
    )

    plt.grid(alpha=0.3)

    plt.title("PHÂN BỐ GIÁ CẢ")

    plt.xlabel("Price ($)")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "price_distribution.png",
        dpi=300
    )

    plt.close()

    print("Đã lưu price_distribution.png")

# ==================================================
# PHÂN TÍCH KÍCH CỠ
# ==================================================
def plot_size_distribution(df: pd.DataFrame) -> None:
    """
    Vẽ biểu đồ Size.
    """

    print("Đang tạo biểu đồ Size...")

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["Size"],
        bins=30,
        edgecolor="black"
    )

    plt.title("PHÂN BỐ KÍCH CỠ")

    plt.xlabel("Size (MB)")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "size_distribution.png",
        dpi=300
    )

    plt.close()
    
    print("Đã lưu size_distribution.png")
    
# ==================================================
# PHÂN TÍCH MA TRẬN TƯƠNG QUAN
# ==================================================
def plot_correlation_matrix(df: pd.DataFrame) -> None:
    """
    Vẽ ma trận tương quan giữa các thuộc tính số.
    """

    print("Đang tạo Correlation Matrix...")

    numeric_df = df.select_dtypes(include=[np.number])

    correlation = numeric_df.corr(numeric_only=True)

    plt.figure(figsize=(10, 8))

    plt.imshow(correlation, cmap="coolwarm", aspect="auto")

    plt.colorbar()
    
    plt.clim(-1, 1)

    plt.xticks(
        range(len(correlation.columns)),
        correlation.columns,
        rotation=90
    )

    plt.yticks(
        range(len(correlation.columns)),
        correlation.columns
    )

    plt.title("MA TRẬN TƯƠNG QUAN")

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "correlation_matrix.png",
        dpi=300
    )

    plt.close()

    print("Đã lưu correlation_matrix.png")

# ==================================================
# PHÂN TÍCH MỐI QUAN HỆ GIỮA RATING VÀ CÁC THUỘC TÍNH
# ==================================================
def plot_scatter_relationships(df: pd.DataFrame) -> None:
    """
    Vẽ các biểu đồ Scatter giữa Rating và các thuộc tính quan trọng.
    """

    print("Đang tạo Scatter Plot...")

    # Rating vs Reviews
    if "Reviews" in df.columns:
        plt.figure(figsize=(7, 5))

        plt.scatter(
            np.log1p(df["Reviews"]),
            df["Rating"],
            alpha=0.5
        )

        plt.xlabel("log(Reviews + 1)")

        plt.ylabel("Rating")
    
        plt.grid(alpha=0.3)
    
        plt.title("Rating vs Reviews")

        plt.tight_layout()

        plt.savefig(
            FIGURE_DIR / "rating_reviews_scatter.png",
            dpi=300
        )

        plt.close()
    print("Đã lưu rating_reviews_scatter.png")
    
    # Rating vs Installs
    if "Installs" in df.columns:
        
        plt.figure(figsize=(7, 5))

        plt.scatter(
            np.log1p(df["Installs"]),
            df["Rating"],
            alpha=0.5
        )

        plt.xlabel("log(Installs + 1)")

        plt.ylabel("Rating")

        plt.title("Rating vs Installs")

        plt.grid(alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            FIGURE_DIR / "rating_installs_scatter.png",
            dpi=300
        )

        plt.close()
        
    print("Đã lưu rating_installs_scatter.png")

    # Rating vs Compound

    if "Average Sentiment Score" in df.columns:

        plt.figure(figsize=(7, 5))

        plt.scatter(
            df["Average Sentiment Score"],
            df["Rating"],
            alpha=0.5
        )

        plt.xlabel("Average Sentiment Score")

        plt.ylabel("Rating")

        plt.title("Rating vs Sentiment")

        plt.grid(alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            FIGURE_DIR / "rating_sentiment_scatter.png",
            dpi=300
        )

        plt.close()

    print("Đã lưu rating_sentiment_scatter.png")

# ==================================================
# PHÂN TÍCH GIÁ CẢ VÀ XẾP HẠNG
# ==================================================

def plot_price_vs_rating(df: pd.DataFrame) -> None:
    """
    Vẽ biểu đồ Scatter giữa Price và Rating.
    """

    print("Đang tạo Price vs Rating Scatter Plot...")

    plt.figure(figsize=(8, 6))

    plt.scatter(
        df["Price"],
        df["Rating"],
        alpha=0.4
    )

    plt.title("Price vs Rating")

    plt.xlabel("Price ($)")

    plt.ylabel("Rating")

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "price_vs_rating.png",
        dpi=300
    )

    plt.close()

    print("Đã lưu price_vs_rating.png")

# ==================================================
# PHÂN TÍCH SO SÁNH XẾP HẠNG GIỮA ỨNG DỤNG MIỄN PHÍ VÀ TRẢ PHÍ
# ==================================================

def plot_price_strategy(df: pd.DataFrame) -> None:
    """
    So sánh Rating giữa ứng dụng Free và Paid.
    """

    print("Đang tạo Boxplot Price Strategy...")

    free_rating = df[df["Price"] == 0]["Rating"]

    paid_rating = df[df["Price"] > 0]["Rating"]

    plt.figure(figsize=(8, 6))

    plt.boxplot(
        [free_rating, paid_rating],
        tick_labels=["Free", "Paid"]
    )

    plt.title("So sánh Xếp hạng giữa Ứng dụng Miễn phí và Trả phí")

    plt.ylabel("Rating")

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "price_strategy_boxplot.png",
        dpi=300
    )

    plt.close()

    print("Đã lưu price_strategy_boxplot.png")

# ==================================================
# PHÂN TÍCH HỆ SỐ TƯƠNG QUAN GIỮA GIÁ VÀ XẾP HẠNG
# ==================================================

def price_rating_correlation(df: pd.DataFrame) -> float:
    """
    Tính hệ số tương quan giữa Price và Rating.
    """

    correlation = df["Price"].corr(df["Rating"])

    print("\n" + "=" * 60)

    print("HỆ SỐ TƯƠNG QUAN GIỮA GIÁ VÀ XẾP HẠNG")

    print("=" * 60)

    print(f"Correlation: {correlation:.4f}")

    return correlation

# ==================================================
# PHÂN TÍCH CHIẾN LƯỢC GIÁ CẢ ẢNH HƯỞNG TỚI XẾP HẠNG
# ==================================================

def analyze_price_strategy(df: pd.DataFrame) -> str:
    """
    Phân tích chiến lược giá ảnh hưởng tới Rating.
    """

    free_mean = df[df["Price"] == 0]["Rating"].mean()

    paid_mean = df[df["Price"] > 0]["Rating"].mean()

    print("\n" + "=" * 60)

    print("PHÂN TÍCH CHIẾN LƯỢC GIÁ CẢ ẢNH HƯỞNG TỚI XẾP HẠNG")

    print("=" * 60)

    print(f"Đánh giá trung bình của các ứng dụng miễn phí : {free_mean:.2f}")

    print(f"Đánh giá trung bình của các ứng dụng trả phí : {paid_mean:.2f}")

    if free_mean > paid_mean:

        conclusion = (
            "Các ứng dụng miễn phí nhận được đánh giá trung bình cao hơn."
        )

    elif paid_mean > free_mean:

        conclusion = (
            "Các ứng dụng trả phí nhận được đánh giá trung bình cao hơn."
        )

    else:

        conclusion = (
            "Không có sự khác biệt đáng kể giữa các ứng dụng miễn phí và trả phí."
        )

    print("\nConclusion:")

    print(conclusion)

    return conclusion

# ==================================================
# PHÂN TÍCH GÓC NHÌN DÀNH CHO DEVELOPER
# ==================================================
def analyze_developer_insight(df: pd.DataFrame) -> str:
    """
    Phân tích góc nhìn dành cho Developer.
    """

    free_apps = df[df["Type"] == "Free"]

    paid_apps = df[df["Type"] == "Paid"]

    free_rating = free_apps["Rating"].mean()

    paid_rating = paid_apps["Rating"].mean()

    free_installs = free_apps["Installs"].mean()

    paid_installs = paid_apps["Installs"].mean()

    insight = (
        "\nThông tin dành cho nhà phát triển\n"
        "------------------------------\n"
        f"Average Rating (Free): {free_rating:.2f}\n"
        f"Average Rating (Paid): {paid_rating:.2f}\n\n"
        f"Average Installs (Free): {free_installs:,.0f}\n"
        f"Average Installs (Paid): {paid_installs:,.0f}\n"
    )

    if free_rating > paid_rating:
        insight += (
            "\nCác ứng dụng miễn phí nhận được đánh giá của người dùng cao hơn."
        )
    else:
        insight += (
            "\nCác ứng dụng trả phí nhận được đánh giá của người dùng cao hơn."
        )

    print(insight)

    return insight

# ==================================================
# PHÂN TÍCH GÓC NHÌN DÀNH CHO ADMIN
# ==================================================
def analyze_admin_recommendation(df: pd.DataFrame) -> str:
    """
    Đưa ra khuyến nghị dành cho Admin.
    """

    recommendation = (
        "\nKhuyến nghị dành cho Admin\n"
        "------------------------------\n"
        "- Theo dõi xếp hạng thường xuyên.\n"
        "- Cải thiện trải nghiệm người dùng.\n"
        "- Khuyến khích đánh giá tích cực.\n"
        "- Tối ưu hóa chiến lược giá.\n"
        "- Theo dõi điểm cảm xúc theo thời gian.\n"
    )

    print(recommendation)

    return recommendation

# ==================================================
# HÀM CHÍNH
# ==================================================
def main() -> None:
    """
    Điều khiển toàn bộ quá trình Exploratory Data Analysis (EDA).
    """

    print("=" * 60)
    print("PHÂN TÍCH DỮ LIỆU KHÁM PHÁ (Exploratory Data Analysis - EDA)")
    print("=" * 60)

    # Load dữ liệu
    df = load_data(INPUT_FILE)

    # Kiểm tra dữ liệu
    inspect_data(df)

    descriptive_statistics(df)

    missing_df = analyze_missing_values(df)

    duplicate_count = analyze_duplicates(df)

    # Visualization
    plot_rating_distribution(df)

    plot_category_distribution(df)

    plot_sentiment_distribution(df)

    plot_reviews_distribution(df)

    plot_installs_distribution(df)

    plot_price_distribution(df)

    plot_size_distribution(df)

    plot_correlation_matrix(df)

    plot_scatter_relationships(df)

    # Price Strategy Analysis
    plot_price_vs_rating(df)

    plot_price_strategy(df)

    correlation = price_rating_correlation(df)

    conclusion = analyze_price_strategy(df)

    # Save Report
    save_report(
        df=df,
        missing_df=missing_df,
        duplicate_count=duplicate_count,
        output_file=REPORT_FILE
    )

    print("\n" + "=" * 60)
    print("EDA HOÀN THÀNH")
    print("=" * 60)

    print(f"Báo cáo : {REPORT_FILE}")

    print(f"Hình ảnh: {FIGURE_DIR}")

    print(f"Hệ số tương quan Price-Rating : {correlation:.4f}")

    print(f"Kết luận: {conclusion}")

# ==================================================
# BẮT ĐẦU CHƯƠNG TRÌNH
# ==================================================

if __name__ == "__main__":
    main()