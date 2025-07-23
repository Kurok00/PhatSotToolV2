# 🚚 Tool Tra Cứu J&T Express v2.0

<div align="center">
  <img src="https://img.shields.io/badge/version-2.0-red?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
</div>

<p align="center">
  <img src="Logo_JT.ico" alt="J&T Tool" width="120" height="120" />
</p>

<p align="center">
  <strong>� Công cụ tra cứu thông tin J&T Express chuyên nghiệp</strong><br>
  Tra cứu số điện thoại & tên shipper nhanh chóng, giao diện hiện đại
</p>

---

## ⭐ Tính năng nổi bật

### 🔍 **Tra cứu thông tin**
- ✅ Tra cứu số điện thoại theo mã vận đơn
- ✅ Tra cứu tên shipper theo số điện thoại
- ✅ Hỗ trợ tra cứu batch (nhiều mã cùng lúc)
- ✅ Tùy chọn khoảng thời gian tra cứu

### 🎨 **Giao diện & UX**
- ✅ Giao diện hiện đại, màu sắc chuẩn J&T
- ✅ Responsive design, tối ưu cho nhiều kích thước màn hình
- ✅ Copy dữ liệu bằng double-click
- ✅ Thông báo floating với animation

### 🛡️ **Bảo mật & Tính năng**
- ✅ Chế độ stealth chống ban account
- ✅ Auto login từ Chrome browser
- ✅ Delay ngẫu nhiên để tránh spam
- ✅ Hủy process giữa chừng

---

## 🚀 Cài đặt nhanh

### **Option 1: Sử dụng Executable (Khuyến nghị)**
1. Tải file `.exe` từ [Releases](https://github.com/Kurok00/PhatSotToolV2/releases)
2. Double-click để chạy
3. Không cần cài đặt gì thêm!

### **Option 2: Chạy từ Source Code**
```bash
git clone https://github.com/Kurok00/PhatSotToolV2.git
cd PhatSotToolV2
pip install -r requirements.txt
python main.py
```

### **Option 3: Script tự động**
```bash
# PowerShell (Khuyến nghị)
.\run_app.ps1

# Batch file
.\Run-Tool.bat
```

> 📋 **Chi tiết setup**: Xem [SETUP.md](SETUP.md)

---

## � Hướng dẫn sử dụng

### 🔑 **Bước 1: Lấy Auth Token**

**Cách 1: Auto Login (Khuyến nghị)**
1. Mở Chrome và đăng nhập [J&T JMS](https://jms.jtexpress.vn/)
2. Chạy `Chrome.bat` để mở Chrome ở chế độ debug
3. Click nút "🔧 Auto Đăng nhập" trong tool
4. Token sẽ tự động được điền vào ô

**Cách 2: Manual**
1. Mở F12 Developer Tools trên trang J&T JMS
2. Vào tab Application → Local Storage → https://jms.jtexpress.vn
3. Copy giá trị của key `YL_TOKEN`
4. Paste vào ô Auth Token

### 📦 **Bước 2: Tra cứu Batch**
1. Nhập các mã vận đơn (mỗi dòng 1 mã)
2. Chọn tháng tra cứu
3. Tùy chọn chế độ stealth (chống ban)
4. Click "🚀 BẮT ĐẦU TRA CỨU"

### 📞 **Bước 3: Tra cứu đơn lẻ**
1. Nhập số điện thoại
2. Chọn tháng tra cứu
3. Click "🔍 TRA CỨU SHIPPER"

---

## 🎯 Screenshots

<details>
<summary>Click để xem ảnh demo</summary>

### Main Interface
![Main Interface](docs/screenshots/main-interface.png)

### Batch Lookup
![Batch Lookup](docs/screenshots/batch-lookup.png)

### Results View
![Results View](docs/screenshots/results-view.png)

</details>

---

## 🛠️ Xây dựng từ Source

```bash
# Clone repository
git clone https://github.com/Kurok00/PhatSotToolV2.git
cd PhatSotToolV2

# Tạo virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python main.py

# Build executable (optional)
pyinstaller main.spec
```

---

## ⚙️ Cấu hình nâng cao

### **Stealth Mode Settings**
- **Delay Min/Max**: Thời gian chờ ngẫu nhiên giữa các request (5-10 giây)
- **Anti-Ban**: Tự động phát hiện và tránh các pattern có thể bị ban

### **Chrome Debug Setup**
```bash
# Tạo profile Chrome riêng cho debug
chrome.exe --remote-debugging-port=9222 --user-data-dir="./chrome_debug_profile"
```

---

## 🤝 Đóng góp

1. Fork repository này
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

---

## 📝 Changelog

### v2.0.0 (Current)
- ✨ Giao diện mới hoàn toàn với Material Design
- ✨ Hỗ trợ batch processing
- ✨ Chế độ stealth chống ban
- ✨ Floating notifications với animation
- ✨ Copy dữ liệu bằng double-click
- 🐛 Fix các lỗi UI responsive
- 🚀 Tối ưu performance

### v1.1.0
- ✨ Auto login từ Chrome
- ✨ Tra cứu theo khoảng thời gian
- 🐛 Fix lỗi encoding

---

## � License

Dự án này được phát hành dưới [MIT License](LICENSE).

---

## 💖 Cảm ơn

**Made with 💖 by Chú 7 Dog**

- 🌟 **Star** repo này nếu thấy hữu ích!
- 🐛 **Report bugs** tại [Issues](https://github.com/Kurok00/PhatSotToolV2/issues)
- 💡 **Suggest features** cho phiên bản tiếp theo
- 🤝 **Contribute** để cùng phát triển tool

---

<div align="center">
  <strong>🚀 Happy coding! 🚀</strong>
</div> 