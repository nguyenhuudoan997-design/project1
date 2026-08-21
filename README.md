# 🤖 AI Rating Predictor

## Giới thiệu

**AI Rating Predictor** là một ứng dụng web tích hợp Trí tuệ nhân tạo (AI) nhằm dự đoán điểm đánh giá (Rating) của một ứng dụng trên Google Play Store dựa trên các thuộc tính của ứng dụng như danh mục, số lượt cài đặt, kích thước, số lượng đánh giá, giá bán và các thông tin liên quan.

Ngoài chức năng dự đoán, hệ thống còn tích hợp chatbot AI giúp người dùng giải thích kết quả dự đoán, hỗ trợ phân tích dữ liệu và cung cấp các gợi ý nhằm cải thiện chất lượng ứng dụng.

---

# Mục tiêu dự án

Dự án được xây dựng với các mục tiêu sau:

* Xây dựng mô hình Machine Learning dự đoán Rating của ứng dụng.
* Làm sạch và tiền xử lý dữ liệu Google Play Store.
* Đánh giá hiệu quả của mô hình bằng các chỉ số thống kê.
* Xây dựng website để người dùng dễ dàng nhập dữ liệu và nhận kết quả dự đoán.
* Tích hợp AI Chat hỗ trợ giải thích và tư vấn kết quả dự đoán.

---

# Chức năng chính

## Đối với người dùng

* Đăng ký tài khoản.
* Đăng nhập hệ thống.
* Nhập thông tin ứng dụng.
* Dự đoán Rating bằng AI.
* Xem lịch sử dự đoán.
* Trao đổi với AI Chat để được giải thích kết quả.

## Đối với quản trị viên

* Quản lý người dùng.
* Quản lý dữ liệu dự đoán.
* Quản lý mô hình AI.
* Huấn luyện lại mô hình với dữ liệu mới.
* Theo dõi thống kê hệ thống.

---

# Công nghệ sử dụng

## Ngôn ngữ lập trình

* Python

## Machine Learning

* Pandas
* NumPy
* Scikit-learn
* Joblib

## Backend

* Flask

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

## Database

* MySQL
* SQLAlchemy

## AI Integration

* Gemini API (Google AI) hoặc API AI khác

---

# Cấu trúc thư mục

```text
AI-Rating-Predictor/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── googleplaystore.csv
│   └── googleplaystore_clean.csv
│
├── models/
│   ├── random_forest_model.pkl
│   └── scaler.pkl
│
├── services/
│   ├── preprocessing.py
│   ├── training.py
│   ├── prediction.py
│   └── ai_service.py
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── predict.py
│   └── admin.py
│
├── templates/
│
├── static/
│
└── database/
```

---

# Dataset

Dự án sử dụng bộ dữ liệu **Google Play Store Dataset**.

Thông tin chính của dữ liệu gồm:

* App
* Category
* Rating
* Reviews
* Size
* Installs
* Type
* Price
* Content Rating
* Genres
* Last Updated
* Current Version
* Android Version

---

# Quy trình xử lý dữ liệu

## Bước 1. Đọc dữ liệu

Đọc tệp **googleplaystore.csv** bằng Pandas.

## Bước 2. Kiểm tra dữ liệu

* Kiểm tra số lượng dòng và cột.
* Kiểm tra kiểu dữ liệu.
* Kiểm tra giá trị bị thiếu.

## Bước 3. Làm sạch dữ liệu

* Xóa dữ liệu trống.
* Chuyển đổi cột Size.
* Chuyển đổi cột Price.
* Chuyển đổi cột Installs.
* Chuyển đổi Reviews sang kiểu số.

## Bước 4. Tiền xử lý

* Encoding dữ liệu dạng văn bản.
* Chuẩn hóa dữ liệu.
* Chia tập Train và Test.

---

# Huấn luyện mô hình AI

Các bước huấn luyện:

1. Đọc dữ liệu đã làm sạch.
2. Chia dữ liệu Train/Test.
3. Huấn luyện mô hình Random Forest Regressor.
4. Đánh giá kết quả.
5. Lưu mô hình bằng Joblib.

---

# Đánh giá mô hình

Các chỉ số đánh giá được sử dụng:

* R² Score
* Mean Absolute Error (MAE)
* Mean Squared Error (MSE)
* Root Mean Squared Error (RMSE)

---

# Quy trình hoạt động của hệ thống

Người dùng nhập thông tin ứng dụng → Hệ thống tiền xử lý dữ liệu → Mô hình AI dự đoán Rating → Hiển thị kết quả → AI Chat giải thích kết quả và đưa ra gợi ý.

---

# Cài đặt dự án

## Bước 1

Clone dự án:

```bash
git clone https://github.com/nguyenhuudoan997-design/project1.git
```

## Bước 2

Di chuyển vào thư mục dự án:

```bash
cd AI-Rating-Predictor
```

## Bước 3

Cài đặt thư viện:

```bash
pip install -r requirements.txt
```

## Bước 4

Chạy ứng dụng:

```bash
python app.py
```

---

# Hướng phát triển

* Tích hợp Deep Learning.
* Dự đoán theo thời gian thực.
* Phân tích cảm xúc từ bình luận người dùng.
* Gợi ý cách cải thiện Rating bằng AI.
* Dashboard trực quan với biểu đồ thống kê.
* Triển khai hệ thống trên nền tảng Cloud.

---

# Kết quả mong đợi

Sau khi hoàn thành, hệ thống có thể:

* Dự đoán điểm Rating của ứng dụng.
* Hỗ trợ người dùng đánh giá chất lượng ứng dụng trước khi phát hành.
* Giúp nhà phát triển đưa ra quyết định dựa trên dữ liệu.
* Cung cấp giải thích và tư vấn thông minh thông qua AI Chat.

---

# Tác giả

**Nguyễn Hữu Đoàn**
**Đỗ Huy Hoàng**

Sinh viên ngành Công nghệ Thông tin

FPT Polytechnic

---

# Giấy phép

Dự án được phát triển phục vụ mục đích học tập, nghiên cứu và báo cáo đồ án.
