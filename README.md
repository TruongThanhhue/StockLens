# StockLens — Dự báo cổ phiếu Việt Nam có dải bất định

Dashboard Streamlit cho bài toán dự báo cổ phiếu Việt Nam: lấy OHLCV qua VNstock, tính chỉ báo kỹ thuật, mô phỏng posterior predictive trên log-return và hiển thị khoảng credible interval.

## Chạy tại máy

```powershell
$python = 'C:\Users\ACER\AppData\Local\Programs\Python\Python311\python.exe'
& $python -m venv "$env:USERPROFILE\.venv"
& "$env:USERPROFILE\.venv\Scripts\python.exe" -m pip install -r https://vnstocks.com/files/requirements.txt
& "$env:USERPROFILE\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& "$env:USERPROFILE\.venv\Scripts\python.exe" -m streamlit run app.py
```

Nhập mã Việt Nam như `VCB`, `FPT`, `HPG` hoặc `VNM`. Lần đầu chạy VNstock có thể yêu cầu đăng ký API key theo hướng dẫn của thư viện.

## Chạy và debug trong Visual Studio Code

Mở thư mục dự án bằng VS Code, cài extension **Python** và **Python Debugger** của Microsoft. Nhấn `F5`, chọn **Chạy StockLens (Vnstock venv)**. Cấu hình `.vscode` đã cố định interpreter ở `C:\Users\ACER\.venv` và chạy Streamlit tại `http://localhost:8501`.

Nếu bạn thấy `No module named 'streamlit'`, Visual Studio/VS Code đang chạy một Python khác. Trong VS Code, chọn `Ctrl+Shift+P` → **Python: Select Interpreter** → chọn `C:\Users\ACER\.venv\Scripts\python.exe`, rồi chạy `F5`. Cách không phụ thuộc lựa chọn interpreter: vào **Terminal → Run Task** và chọn **Mở StockLens bằng Vnstock venv**.

## Chạy trong Visual Studio (bản tím)

Visual Studio không dùng cấu hình `.vscode`. Cài workload **Python development**, mở thư mục dự án, rồi vào **View → Other Windows → Python Environments**. Chọn **Add Environment → Existing environment** và trỏ interpreter đến:

```text
C:\Users\ACER\.venv\Scripts\python.exe
```

Đặt môi trường đó làm mặc định. Vì Streamlit là web server, cách chạy ổn định nhất trong Visual Studio là mở **View → Terminal** và dùng:

```powershell
& "C:\Users\ACER\.venv\Scripts\python.exe" -m streamlit run app.py
```

Sau đó mở `http://localhost:8501` trên trình duyệt.

Kết quả chỉ dùng cho học tập và nghiên cứu, không phải khuyến nghị đầu tư.
