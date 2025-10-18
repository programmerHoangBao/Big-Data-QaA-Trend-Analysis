Đồ án môn học: Phân tích dữ liệu - Đại học Sư phạm Kỹ thuật Hồ Chí Minh
Tên đề tài: Phân tích dữ liệu câu hỏi trong lĩnh vực lập trình theo thời gian thực
Nhóm sinh viên:
-  Nguyễn Hoàng Bảo
-  Trần Thị Kim Chung
-  Ngô Trung Hiếu
-  Lưu Quốc Thành
  
📖 Giới thiệu
- Trong kỷ nguyên số hóa và dữ liệu lớn (Big Data), việc thu thập, lưu trữ, xử lý và phân tích dữ liệu hiệu quả đã trở thành yếu tố quyết định lợi thế cạnh tranh của doanh nghiệp.
Tuy nhiên, các kiến trúc dữ liệu truyền thống như Data Warehouse và Data Lake riêng lẻ thường gặp phải giới hạn về:

🔒 Quản lý giao dịch (ACID)

📉 Chất lượng dữ liệu

⚙️ Tính linh hoạt và mở rộng

- Kiến trúc Lakehouse ra đời như một giải pháp lai tối ưu, kết hợp ưu điểm của Data Warehouse và Data Lake, cho phép:
  + Lưu trữ dữ liệu đa dạng (structured, semi-structured, unstructured)
  + Hỗ trợ giao dịch ACID
  + Cải thiện hiệu năng truy vấn và chi phí lưu trữ

🎯 Mục tiêu dự án
- Dự án tập trung vào việc tự động hóa quá trình xây dựng một Lakehouse thống nhất. Cụ thể, hệ thống được thiết kế để:
- Thu thập dữ liệu batch (JSON) và streaming
- Xử lý, làm sạch, và làm giàu dữ liệu qua các lớp Bronze, Silver, Gold
- Tự động hóa pipeline thông qua Apache Airflow DAGs
- Phân tích và trực quan hóa kết quả bằng Apache Superset
- Ứng dụng mô hình Logistic Regression để huấn luyện và dự đoán dữ liệu cuối cùng

⚙️ Kiến trúc tổng quan
- Hệ thống được chia thành các lớp chính theo mô hình Lakehouse:

┌────────────────────────┐
│     Data Sources        │
│ (Batch JSON, Streaming) │
└────────────┬───────────┘
             ▼
        🟤 Bronze Layer
  → Dữ liệu thô, chưa xử lý
             ▼
        ⚪ Silver Layer
  → Làm sạch, chuẩn hóa
             ▼
        🟡 Gold Layer
  → Dữ liệu đã làm giàu, sẵn sàng phân tích
             ▼
   📊 Apache Superset / ML Model

🧰 Công nghệ sử dụng
Thành phần	Công nghệ
Xử lý dữ liệu	Apache Spark, Delta Lake
Orchestration	Apache Airflow
Streaming	Apache Kafka
Visualization	Apache Superset
Machine Learning	Scikit-learn (LogisticRegression)
Lưu trữ	HDFS / MinIO / Delta Tables
Ngôn ngữ lập trình	Python
Hạ tầng	Docker Compose

🧑‍💻 Cài đặt và chạy thử
1. Clone dự án
git clone https://github.com/<username>/lakehouse-pipeline.git
cd lakehouse-pipeline

2. Khởi tạo môi trường
docker-compose up -d

3. Truy cập các dịch vụ
Dịch vụ	URL
Airflow Web UI	http://localhost:8080
Superset	http://localhost:8088
Kafka UI	http://localhost:9000

🔄 Pipeline tự động hóa
- Các DAGs trong Airflow đảm nhận vai trò:
  + Ingest dữ liệu batch và streaming
  + Tiền xử lý (Bronze) – lưu dữ liệu thô
  + Làm sạch (Silver) – chuẩn hóa và xử lý lỗi
  + Làm giàu (Gold) – tổng hợp, tạo dữ liệu phân tích
  + Xuất dữ liệu sang Superset và mô hình Logistic Regression

📈 Trực quan hóa và mô hình học máy
- Dữ liệu sau khi xử lý được trực quan hóa trên Apache Superset
- Mô hình Logistic Regression được train trên dữ liệu lớp Gold để:
  + Phân tích xu hướng
  + Dự đoán các hành vi hoặc phân loại dữ liệu

🧩 Cấu trúc thư mục
lakehouse-pipeline/
├── dags/                 # DAGs cho Airflow
├── scripts/              # Script xử lý dữ liệu
├── config/               # Cấu hình môi trường
├── data/                 # Dữ liệu đầu vào / đầu ra
├── notebooks/            # Phân tích và huấn luyện mô hình
├── docker-compose.yml
└── README.md

📜 Kết luận: Dự án minh họa quy trình xây dựng Lakehouse hiện đại và tự động hóa pipeline dữ liệu – từ ingest, transform đến visualization và machine learning.
- Kết quả mang lại một hệ thống:
- Dễ mở rộng
- Linh hoạt với nhiều loại dữ liệu
- Tích hợp tốt giữa batch và streaming
- Phù hợp cho phân tích dữ liệu nâng cao
