# Tool Tra Cứu Số Điện Thoại Theo Mã Vận Đơn J&T Express

## 1. Mô tả
Tool này giúp bạn tra cứu nhanh số điện thoại người nhận và lấy token từ Chrome cho hệ thống J&T Express. Giao diện đơn giản, dễ dùng, không cần biết code!

## 2. Yêu cầu môi trường
- **Python 3.8+** (khuyên dùng bản mới nhất)
- **Google Chrome** (bắt buộc, đã đăng nhập tài khoản J&T)
- **ChromeDriver** (phiên bản phù hợp với Chrome, đã có sẵn file `chromedriver.exe` trong thư mục này)

## 3. Cài đặt các thư viện cần thiết
Mở terminal/cmd tại thư mục chứa file, chạy lệnh sau:
```bash
pip install tkinter selenium requests
```
> Nếu bị lỗi `tkinter` thì cài thêm qua package manager của Python hoặc cài lại Python có sẵn tkinter.

## 4. Hướng dẫn sử dụng
### Bước 1: Lấy token (authToken)
Có 2 cách:
- **Cách 1 (tự động, khuyên dùng):**
    1. Mở Chrome bằng debug mode:
        - Đóng hết Chrome.
        - Mở terminal/cmd, chạy:
          ```bash
          chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Users/Administrator/AppData/Local/Google/Chrome/User Data"
          ```
        - Đăng nhập vào https://jms.jtexpress.vn/.
    2. Bấm nút "Lấy token từ Chrome đang mở (debug)" trên tool.
- **Cách 2 (thủ công):**
    - Vào F12 > Application > Local Storage > copy giá trị `YL_TOKEN` dán vào ô authToken.

### Bước 2: Tra cứu số điện thoại
1. Nhập danh sách mã vận đơn (mỗi dòng 1 mã) vào ô tương ứng.
2. Nhập/copy authToken vào ô trên.
3. Bấm nút "Tra cứu".
4. Xem kết quả ở bảng phía dưới.

## 5. Lưu ý
- Token hết hạn thì lấy lại như bước 1.
- Nếu không lấy được token, kiểm tra lại Chrome đã chạy debug mode chưa.
- Nếu bị lỗi ChromeDriver, tải đúng phiên bản tại: https://chromedriver.chromium.org/downloads

## 6. Style techlead genZ
- Code dễ hiểu, UI thân thiện, debug dễ.
- Có gì lỗi cứ inbox, mình support nhiệt tình!

---
Chúc bạn tra cứu vui vẻ! 🚀 