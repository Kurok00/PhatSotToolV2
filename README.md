# 🚚 Tool Tra Cứu Số Điện Thoại Theo Mã Vận Đơn J&T Express

<p align="left">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/35/Logo_J%26T_Merah_Square.jpg" alt="J&T Logo" width="200" height="200" />
</p>
🚚 Release v1.1 : https://drive.google.com/file/d/1GRUPNKzaPHxbBylhNa-Z1If0R2hLImv-/view?usp=sharing
## 🌟 Tính năng nổi bật
- Giao diện đẹp, màu đỏ-trắng chuẩn J&T, thân thiện end user
- Tra cứu số điện thoại người nhận theo mã vận đơn
- Tra cứu tên shipper theo số điện thoại, chọn ngày bằng lịch
- Lấy nhanh token từ Chrome debug chỉ với 1 click
- Không cần biết code, chỉ cần copy-paste token là dùng được

---

## 🖥️ Yêu cầu hệ thống
- **Windows** (khuyên dùng Win 10/11)
- **Python 3.8+** (tải tại [python.org](https://www.python.org/downloads/))
- **Google Chrome** (bắt buộc, đã đăng nhập tài khoản J&T)
- **ChromeDriver** (đã có sẵn file `chromedriver.exe` trong thư mục này)

---

## ⚡ Cài đặt nhanh
1. **Cài Python** (nếu chưa có):
   - Tải và cài Python từ [python.org](https://www.python.org/downloads/)
   - Khi cài nhớ tick "Add Python to PATH"
2. **Cài các thư viện cần thiết:**
   Mở terminal/cmd tại thư mục chứa file, chạy:
   ```bash
   pip install tkinter selenium requests tkcalendar
   ```
   > Nếu bị lỗi `tkinter` thì cài lại Python bản chuẩn, hoặc dùng Microsoft Store để cài Python.

---

## 🛠️ Hướng dẫn sử dụng
### 1. Lấy token từ Chrome
- Chạy file `chrome_debug_shortcut.bat` để mở Chrome ở chế độ debug (profile riêng, không ảnh hưởng Chrome chính)
- Đăng nhập vào [J&T JMS](https://jms.jtexpress.vn/) trên Chrome debug vừa mở
- Bấm nút **"Lấy token từ Chrome đang mở (debug)"** trên tool, token sẽ tự động điền vào ô

### 2. Tra cứu số điện thoại theo mã vận đơn
- Nhập **authToken** vào ô trên cùng (hoặc dùng nút lấy token tự động)
- Nhập **mã vận đơn** (mỗi dòng 1 mã)
- Bấm **Tra cứu**
- Kết quả sẽ hiển thị ở bảng bên dưới

### 3. Tra cứu tên shipper từ số điện thoại
- Nhập **số điện thoại** vào ô to màu đỏ
- Chọn **Từ ngày** và **Đến ngày** bằng lịch (mặc định là cả tháng hiện tại)
- Bấm **Tra cứu tên shipper**
- Tên shipper sẽ hiển thị ngay bên dưới

---

## 💡 Lưu ý
- **Không cần commit thư mục `chrome_debug_profile/`, file `.exe`, `.venv/`, `__pycache__/` vào git** (đã có sẵn `.gitignore`)
- Nếu API trả về lỗi ngoài giờ hành chính (6h-22h), vui lòng thử lại trong khung giờ cho phép
- Nếu không lấy được token, kiểm tra lại Chrome debug đã mở đúng chưa

---

## 📦 Đóng góp & phát triển
- Repo: [https://github.com/Kurok00/PhatSotToolV2](https://github.com/Kurok00/PhatSotToolV2)
- Mọi ý kiến, bug, góp ý UI/UX, tính năng mới... cứ tạo issue hoặc liên hệ trực tiếp!

---

## 🏆 Cảm ơn bạn đã sử dụng tool! Chúc bạn tra cứu đơn J&T siêu nhanh 🚀 
