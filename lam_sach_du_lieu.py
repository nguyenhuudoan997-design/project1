import numpy as np
import pandas as pd

# Đọc file dữ liệu user reviews
df = pd.read_csv("googleplaystore_user_reviews.csv")

# Kiểm tra tổng quan dữ liệu
print("Kích thước dữ liệu gốc:", df.shape)
print("Các cột có trong file:", df.columns.tolist())
df.info()

# Kiểm tra số lượng dòng null trước khi xử lý
print("Số lượng thiếu trước khi xử lý:\n", df.isnull().sum())

# Xóa các dòng có giá trị NaN ở cột 'Translated_Review' hoặc 'Sentiment'
df.dropna(
    subset=["Translated_Review", "Sentiment", "Sentiment_Polarity"],
    inplace=True,
)

# Kiểm tra lại kích thước sau khi xóa
print("Kích thước sau khi làm sạch:", df.shape)

df["Translated_Review"] = df["Translated_Review"].astype(str).str.lower()

# Lưu file đã xử lý ra file CSV mới
df.to_csv("googleplaystore_user_reviews_cleaned.csv", index=False)
print("Đã làm sạch và lưu file user_reviews thành công!")