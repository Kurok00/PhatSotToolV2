# 🚀 Setup Guide - Tool Tra Cứu J&T Express v2.0

## 📋 Yêu cầu hệ thống

- **Python 3.8+** (Khuyến nghị Python 3.9 trở lên)
- **Windows 10/11** (Đã test)
- **Chrome Browser** (Cho tính năng auto login)

## ⚡ Cài đặt nhanh

### 1. Clone repository
```bash
git clone https://github.com/Kurok00/PhatSotToolV2.git
cd PhatSotToolV2
```

### 2. Tạo virtual environment
```bash
python -m venv .venv
```

### 3. Activate virtual environment
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat
```

### 4. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 5. Chạy ứng dụng
```bash
python main.py
```

## 🎯 Cách chạy nhanh nhất

Sử dụng script có sẵn:

### Option 1: PowerShell Script (Khuyến nghị)
```bash
.\run_app.ps1
```

### Option 2: Batch File
```bash
.\Run-Tool.bat
```

## 🔧 Build executable

Để build thành file .exe:

```bash
# Activate virtual environment trước
.\.venv\Scripts\Activate.ps1

# Build bằng PyInstaller
pyinstaller main.spec
```

File .exe sẽ được tạo trong thư mục `dist/`

## 📁 Cấu trúc dự án

```
PhatSotToolV2/
├── main.py              # 🎯 File chính của ứng dụng
├── main.spec            # ⚙️ Cấu hình PyInstaller
├── requirements.txt     # 📦 Dependencies
├── chromedriver.exe     # 🌐 Chrome WebDriver
├── Logo_JT.ico         # 🖼️ Icon ứng dụng
├── run_app.ps1         # 🚀 Script PowerShell
├── Run-Tool.bat        # 🚀 Script Batch
├── Chrome.bat          # 🔧 Chrome debug mode
├── HOW_TO_RUN.md       # 📖 Hướng dẫn sử dụng
├── README.md           # 📋 Tài liệu dự án
├── SETUP.md            # ⚡ Hướng dẫn setup
└── .gitignore          # 🚫 Git ignore rules
```

## 🔍 Troubleshooting

### Lỗi thiếu module
```bash
pip install -r requirements.txt --upgrade
```

### Lỗi ChromeDriver
- Đảm bảo `chromedriver.exe` cùng thư mục với `main.py`
- Cập nhật ChromeDriver phù hợp với phiên bản Chrome

### Lỗi tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

## 💡 Tips

1. **Auto login**: Sử dụng tính năng "Auto Đăng nhập" thay vì nhập token thủ công
2. **Stealth mode**: Bật chế độ chống ban để tránh bị giới hạn API
3. **Batch processing**: Có thể tra cứu nhiều mã vận đơn cùng lúc

## 🆘 Hỗ trợ

Nếu gặp vấn đề, vui lòng tạo issue tại: [GitHub Issues](https://github.com/Kurok00/PhatSotToolV2/issues)

---
Made with 💖 by Chú 7 Dog
