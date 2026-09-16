# Tổng hợp công cụ xây dựng Web Dự đoán Cổ phiếu

Định hướng: xây dựng web app dự đoán giá/xu hướng cổ phiếu dựa trên dữ liệu lịch sử, ưu tiên mô hình chuỗi thời gian Bayesian và hiển thị mức độ bất định của dự báo.

## 1. Kiến trúc tổng thể

Người dùng nhập mã cổ phiếu (ticker), khoảng thời gian dữ liệu và số ngày cần dự báo. Frontend gửi yêu cầu đến backend; backend lấy dữ liệu thị trường, xử lý đặc trưng, gọi mô hình dự báo và trả về kết quả cùng biểu đồ.

- Frontend: form nhập ticker, chọn khoảng thời gian, dashboard hiển thị giá lịch sử và dự báo.
- Backend: API hoặc các route xử lý yêu cầu, kiểm tra mã cổ phiếu và điều phối luồng dữ liệu.
- Data layer: lấy OHLCV (Open, High, Low, Close, Volume), cache dữ liệu và lưu lịch sử dự báo nếu cần.
- Model layer: tiền xử lý, huấn luyện/dự báo Bayesian time series, tính khoảng dự báo.
- Visualization: biểu đồ nến, đường giá, đường dự báo và dải bất định.

## 2. Nguồn dữ liệu

- Yahoo Finance qua thư viện yfinance: phù hợp nhất để làm demo; có dữ liệu giá lịch sử, khối lượng và một số thông tin doanh nghiệp.
- Alpha Vantage: API dữ liệu tài chính có giới hạn miễn phí; cần API key.
- Kaggle: phù hợp khi cần dataset cố định để thử nghiệm, tái lập kết quả và viết báo cáo.
- Nguồn nội địa: dữ liệu chứng khoán Việt Nam cần kiểm tra điều khoản sử dụng của nguồn/API; có thể bắt đầu bằng mã quốc tế như AAPL, MSFT hoặc chỉ số S&P 500 để giảm khó khăn dữ liệu.

## 3. Thư viện Python

| Nhóm | Công cụ/thư viện | Vai trò |
|------|------------------|---------|
| Lấy dữ liệu | yfinance, requests | Tải dữ liệu thị trường và gọi API. |
| Xử lý dữ liệu | pandas, numpy | Làm sạch, biến đổi dữ liệu và tính toán đặc trưng. |
| Chỉ báo kỹ thuật | pandas-ta hoặc TA-Lib | Tính moving average, RSI, MACD, volatility. |
| Bayesian modeling | PyMC (khuyến nghị), ArviZ | Xây dựng mô hình Bayes, lấy posterior và kiểm tra hội tụ. |
| Forecasting đơn giản | Prophet | Tạo baseline dự báo trend/seasonality nhanh; dùng để so sánh. |
| ML baseline | scikit-learn | Linear Regression, Random Forest, metric MAE/RMSE/MAPE. |
| Web app nhanh | Streamlit | Tạo giao diện Python-only, rất phù hợp bản MVP/demo. |
| Backend web | Flask hoặc FastAPI | Xây API/backend khi cần frontend riêng. |
| Biểu đồ | Plotly | Candlestick, line chart, dải dự báo tương tác. |
| Lưu trữ | SQLite, SQLAlchemy; PostgreSQL | Cache dữ liệu, lưu dự báo và tài khoản khi mở rộng. |
| Lưu model | joblib, cloudpickle | Lưu mô hình hoặc artefact tiền xử lý khi phù hợp. |

## 4. Chọn stack

### Phương án A — Khuyến nghị cho đồ án

Streamlit + yfinance + pandas + PyMC/Prophet + Plotly + scikit-learn. Phương án này triển khai nhanh, không bắt buộc viết HTML/CSS, dễ trình diễn và vẫn thể hiện được phần Bayes.

### Phương án B — Web đầy đủ hơn

React hoặc HTML/CSS/JavaScript + FastAPI/Flask + yfinance + PyMC + Plotly. Phù hợp nếu muốn tách frontend/backend, có API và hướng đến portfolio web.

## 5. Quy trình xử lý

1. Người dùng nhập ticker, ví dụ AAPL, và số ngày dự báo, ví dụ 30 ngày.
2. Hệ thống kiểm tra ticker rồi tải dữ liệu lịch sử (khuyến nghị tối thiểu 2–5 năm dữ liệu ngày).
3. Làm sạch: sắp xếp theo ngày, xử lý thiếu dữ liệu, dùng Adjusted Close/Close nhất quán.
4. Tạo đặc trưng: log return, moving average, RSI, MACD, rolling volatility, volume change. Tránh dùng dữ liệu tương lai khi tạo đặc trưng.
5. Chia train/test theo thời gian: train là giai đoạn cũ, test là giai đoạn mới; không chia ngẫu nhiên chuỗi thời gian.
6. Huấn luyện baseline (naive forecast, moving average, ARIMA hoặc hồi quy) để có mốc so sánh.
7. Huấn luyện mô hình Bayes: xác định prior cho tham số trend/volatility, likelihood cho quan sát và lấy posterior bằng MCMC hoặc variational inference.
8. Sinh dự báo nhiều mẫu từ posterior, lấy median/mean dự báo và khoảng credible interval 80% hoặc 95%.
9. Đánh giá trên test: MAE, RMSE, MAPE; kiểm tra coverage của khoảng dự báo.
10. Hiển thị dashboard: giá quá khứ, giá dự báo, dải bất định, thông số mô hình và cảnh báo không phải lời khuyên đầu tư.

## 6. Mô hình Bayes gợi ý

- MVP: Bayesian Linear Regression dự báo log return/ngà¥» kế tiếp từ lagged returns, volatility và technical indicators. Dễ giải thích, phù hợp để chứng minh định lý Bayes.
- Trung cấp: Bayesian Structural Time Series (local trend + seasonal component + regression features). Phù hợp khi muốn phân tách xu hướng và nhiễu.
- Nâng cao: stochastic volatility hoặc Gaussian Process; phức tạp và tốn thời gian hơn.
- Prophet nên được dùng như một baseline forecasting thuận tiện. Không nên khẳng định toàn bộ Prophet là một mô hình Bayes tổng quát cho mọi nhu cầu.

## 7. Chức năng web tối thiểu

- Ô nhập ticker và chọn thị trường/mã«» mẫu.
- Chọn số năm dữ liệu lịch sử và horizon dự báo (7, 14, 30 ngày).
- Biểu đồ candlestick hoặc line chart cho dữ liệu lịch sử.
- Biểu đồ dự báo với đường trung tâm và dải credible interval.
- Bảng metric: MAE, RMSE, MAPE, ngày dữ liệu cuối cùng.
- Tải kết quả dự báo dưới dạng CSV.
- Thông báo lỗi khi ticker không hợp lệ hoặc dữ liệu không đủ.
- Disclaimer: mô hình phục vụ học tập, không phải khuyến nghị mua/bá»».

## 8. Cấu trúc thư mục đề xuất

```
stock_prediction/
├── app.py                    # Streamlit entry point hoặc Flask entry point
├── requirements.txt
├── README.md
├── src/
│   ├── data_fetcher.py       # yfinance, cache, validation
│   ├── features.py           # preprocessing và indicators
│   ├── model_bayesian.py     # PyMC model/train/predict
│   ├── evaluation.py         # metrics, backtesting
│   └── charts.py             # Plotly figures
├── data/                     # dữ liệu cache, không commit dữ liệu lớn
├── models/                   # model artefacts
└── tests/                    # unit tests cơ bản
```

## 9. Requirements mẫu

```
streamlit
yfinance
pandas
numpy
plotly
scikit-learn
pymc
arviz
pandas-ta
joblib
```

## 10. Triển khai

- Phát triển cục bộ: tạo virtual environment, cài requirements, chạy streamlit run app.py hoặc flask run.
- Deploy bản Streamlit: Streamlit Community Cloud phù hợp demo học tập; cần repository GitHub và requirements.txt.
- Deploy Flask/FastAPI: Render/Railway/PythonAnywhere là các lựa chọn dễ tiếp cận. Nếu PyMC/MCMC chạy nặng, nên huấn luyện trước hoặc giới hạn dữ liệu/số mẫu.
- Dùng biến môi trường cho API key, không đưa khóa vào GitHub.

## 11. Lộ trình 4 tuần

- Tuần 1: lấy dữ liệu yfinance, EDA, biểu đồ giá và baseline forecast.
- Tuần 2: feature engineering, chia dữ liệu đúng theo thời gian, đánh giá baseline.
- Tuần 3: xây Bayesian model bằng PyMC, tạo posterior predictive forecast và credible interval.
- Tuần 4: hoàn thiện web, kiểm thử, deploy, viết README và báo cáo.

## 12. Lưu ý học thuật và thực tế

Giá«» cổ phiếu có nhiễu lớn và bị tác động bởi tin tức, thanh khoản, sự kiện kinh tế vĩ mô. Mục tiêu thuyết phục của project nên là dự báo có định lượng bất định, đánh giá nghiêm túc bằng backtesting và minh bạch giới hạn mô hình; không cam kết lợi nhuận hoặc coi kết quả là khuyến nghị đầu tư.
