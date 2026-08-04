import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Tải lexicon VADER nếu chưa có
nltk.download('vader_lexicon')

# Đọc dữ liệu
df_apps = pd.read_csv("googleplaystore_cleaned.csv")
df_reviews = pd.read_csv("googleplaystore_user_reviews.csv")

print("Apps shape:", df_apps.shape)
print("Reviews shape:", df_reviews.shape)
print("Reviews columns:", df_reviews.columns.tolist())

# Khởi tạo VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Làm sạch dữ liệu Reviews (loại bỏ các dòng không có nội dung Review)
df_reviews_clean = df_reviews.dropna(subset=['Translated_Review']).copy()

# Tính điểm Sentiment bằng VADER (dùng compound score)
df_reviews_clean['VADER_Compound'] = df_reviews_clean['Translated_Review'].apply(lambda x: sia.polarity_scores(str(x))['compound'])

# Tính điểm Sentiment trung bình theo từng ứng dụng (App)
sentiment_by_app = df_reviews_clean.groupby('App')['VADER_Compound'].mean().reset_index()
sentiment_by_app.rename(columns={'VADER_Compound': 'Avg_Sentiment_Score'}, inplace=True)

# Merge vào bảng Apps cleaned
df_merged = pd.merge(df_apps, sentiment_by_app, on='App', how='left')

print("\n--- MẪU DỮ LIỆU SAU KHI MERGE ---")
print(df_merged[['App', 'Rating', 'Reviews', 'Avg_Sentiment_Score']].head())
print("\nSố lượng ứng dụng có điểm Sentiment:", df_merged['Avg_Sentiment_Score'].notna().sum())