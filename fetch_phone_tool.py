import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import selenium
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import datetime
import calendar
from tkcalendar import DateEntry
import webbrowser
from PIL import Image, ImageTk
import os

# Hàm fetch số điện thoại từ API
def fetch_phone(waybill_id, auth_token):
    url = f"https://jmsgw.jtexpress.vn/servicequality/integration/getWaybillsByReverse?type=1&waybillId={waybill_id}"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=utf-8",
        "authToken": auth_token,
        "lang": "VN",
        "langType": "VN",
        "Origin": "https://jms.jtexpress.vn",
        "Referer": "https://jms.jtexpress.vn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "routeName": "integratedComprehensive",
        "routerNameList": "%E6%9C%8D%E5%8A%A1%E8%B4%A8%E9%87%8F%3E%E7%BB%BC%E5%90%88%E6%9F%A5%E8%AF%A2%3E%E4%B8%80%E4%BD%93%E5%8C%96%E6%9F%A5%E8%AF%A2%EF%BC%88%E6%96%B0%EF%BC%89",
        "timezone": "GMT+0700"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("succ") and data.get("data"):
                return data["data"].get("receiverMobilePhone", "")
            else:
                return "Không tìm thấy"
        else:
            return f"Lỗi {resp.status_code}"
    except Exception as e:
        return f"Lỗi: {e}"

def fetch_shipper(phone, auth_token, start=None, end=None):
    url = "https://jmsgw.jtexpress.vn/networkmanagement/dispatchWaybill/list"
    # Nếu không truyền start/end thì lấy mặc định tháng hiện tại
    now = datetime.datetime.now()
    if not start:
        start = now.replace(day=1).strftime("%Y-%m-%d")
    if not end:
        end = now.replace(day=calendar.monthrange(now.year, now.month)[1]).strftime("%Y-%m-%d")
    body = {
        "current": 1,
        "size": 10,
        "oneNetwork": "028001",
        "receiverMobilePhone": phone,
        "twoNetwork": "028001",
        "searchTimeType": 0,
        "startTime": f"{start} 00:00:00",
        "endTime": f"{end} 23:59:59",
        "networkType": 2,
        "dispatchFinanceCode": "028001",
        "dispatchFinanceId": 4993,
        "franchiseeCode": "028001",
        "franchiseeId": 4993,
        "countryId": "1"
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "authToken": auth_token,
        "lang": "VN",
        "langType": "VN",
        "Origin": "https://jms.jtexpress.vn",
        "Referer": "https://jms.jtexpress.vn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "routeName": "dispatchWaybill",
        "routerNameList": "%E7%BD%91%E7%82%B9%E7%BB%8F%E8%90%A5%3E%E8%BF%90%E5%8D%95%E7%AE%A1%E7%90%86%3E%E6%B4%BE%E4%BB%B6%E8%BF%90%E5%8D%95%E7%AE%A1%E7%90%86",
        "timezone": "GMT+0700"
    }
    try:
        print(f"[DEBUG] Gọi API2 với SĐT: {phone}, start: {start}, end: {end}")
        resp = requests.post(url, headers=headers, json=body, timeout=10)
        print(f"[DEBUG] Status: {resp.status_code}")
        print(f"[DEBUG] Response: {resp.text}")
        if resp.status_code == 200:
            data = resp.json()
            records = data.get("data", [])
            # Nếu records là dict (kiểu cũ), lấy .get('records', [])
            if isinstance(records, dict):
                records = records.get("records", [])
            if isinstance(records, list) and len(records) > 0 and "dispatchStaffName" in records[0]:
                print(f"[DEBUG] Tên shipper lấy được: {records[0]['dispatchStaffName']}")
                return records[0]["dispatchStaffName"]
            else:
                print("[DEBUG] Không tìm thấy trường dispatchStaffName trong records")
                return "Không tìm thấy shipper"
        else:
            return f"Lỗi {resp.status_code}"
    except Exception as e:
        print(f"[DEBUG] Exception khi gọi API2: {e}")
        return f"Lỗi: {e}"

# Hàm xử lý khi nhấn nút tra cứu
def tra_cuu():
    waybills = txt_waybills.get("1.0", tk.END).strip().splitlines()
    auth_token = txt_token.get().strip()
    start = date_start_top.get_date().strftime("%Y-%m-%d")
    end = date_end_top.get_date().strftime("%Y-%m-%d")
    if not waybills or not auth_token:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã vận đơn và authToken!")
        return
    btn_tra_cuu.config(state=tk.DISABLED)
    for row in tree.get_children():
        tree.delete(row)
    def worker():
        for waybill in waybills:
            waybill = waybill.strip()
            if not waybill:
                continue
            phone = fetch_phone(waybill, auth_token)
            # Tự động tra tên shipper nếu có SĐT hợp lệ
            if phone and phone.isdigit() and len(phone) >= 8:
                ten_shipper = fetch_shipper(phone, auth_token, start, end)
                if not ten_shipper or 'không' in ten_shipper.lower() or 'lỗi' in ten_shipper.lower():
                    ten_shipper = "Không tìm thấy shipper"
            else:
                ten_shipper = ""
            tree.insert("", tk.END, values=(waybill, phone, ten_shipper))
        btn_tra_cuu.config(state=tk.NORMAL)
    threading.Thread(target=worker, daemon=True).start()

# Định nghĩa hàm tra_cuu_shipper TRƯỚC
def tra_cuu_shipper():
    phone = txt_phone.get().strip()
    auth_token = txt_token.get().strip()
    start = date_start.get_date().strftime("%Y-%m-%d")
    end = date_end.get_date().strftime("%Y-%m-%d")
    if not phone or not auth_token or not start or not end:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ SĐT, token, ngày bắt đầu và kết thúc!")
        return
    btn_tra_cuu_shipper.config(state=tk.DISABLED)
    lbl_shipper_result.config(text="Đang tra cứu...", fg="orange")
    def worker():
        ten_shipper = fetch_shipper(phone, auth_token, start, end)
        if "không" in ten_shipper.lower() or "lỗi" in ten_shipper.lower():
            lbl_shipper_result.config(text=f"Tên shipper: {ten_shipper}", fg="red")
        else:
            lbl_shipper_result.config(text=f"Tên shipper: {ten_shipper}", fg="green")
        btn_tra_cuu_shipper.config(state=tk.NORMAL)
    threading.Thread(target=worker, daemon=True).start()

def get_token_from_chrome():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(r'user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data')
        options.add_argument('profile-directory=Profile 2')
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options=options)
        driver.get('https://jms.jtexpress.vn/')
        time.sleep(3)  # Đợi trang load, có thể tăng nếu mạng chậm
        token = driver.execute_script("return window.localStorage.getItem('YL_TOKEN');")
        driver.quit()
        if token:
            txt_token.delete(0, tk.END)
            txt_token.insert(0, token)
            show_copy_notify('Lấy token thành công!', JT_RESULT)
        else:
            show_copy_notify('Không tìm thấy YL_TOKEN trong localStorage!', JT_ERROR)
    except Exception as e:
        show_copy_notify(f'Lấy token thất bại: {e}', JT_ERROR)

def get_token_from_chrome_debug():
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        service = Service('chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # Lấy danh sách các tab đang mở
        handles = driver.window_handles
        if handles:
            driver.switch_to.window(handles[0])  # Giữ nguyên tab hiện tại (tab đầu tiên)
            token = driver.execute_script("return window.localStorage.getItem('YL_TOKEN');")
        else:
            token = None
        driver.quit()
        if token:
            txt_token.delete(0, tk.END)
            txt_token.insert(0, token)
            show_copy_notify('Lấy token từ Chrome đang mở thành công!', JT_RESULT)
        else:
            show_copy_notify('Không tìm thấy YL_TOKEN trong localStorage!', JT_ERROR)
    except Exception as e:
        show_copy_notify(f'Lấy token thất bại: {e}', JT_ERROR)

# ======= STYLE J&T ĐỎ - TRẮNG =======
JT_RED = "#e60012"         # Đỏ J&T
JT_RED_LIGHT = "#ffebee"   # Đỏ nhạt/pastel
JT_GRAY = "#f5f5f5"        # Xám nền nhẹ
JT_WHITE = "#ffffff"
JT_LABEL = "#333333"
JT_BTN_TEXT = "#fff"
JT_TITLE = JT_RED
JT_RESULT = "#388e3c"
JT_ERROR = "#d32f2f"

# KHỞI TẠO ROOT TRƯỚC
root = tk.Tk()
root.title("Tool tra cứu số điện thoại theo mã vận đơn")
root.geometry("1100x650")
root.resizable(True, True)
root.configure(bg=JT_GRAY)

# ======= LABEL GITHUB LINK GÓC TRÁI TRÊN (CÓ ICON + HOVER) =======
GITHUB_ICON_PATH = "github_icon.png"
# Nếu chưa có icon, tải về hoặc tạo icon nhỏ 20x20px, nền trong suốt
if not os.path.exists(GITHUB_ICON_PATH):
    import requests
    url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    r = requests.get(url)
    with open(GITHUB_ICON_PATH, "wb") as f:
        f.write(r.content)
# Load icon
icon_img = Image.open(GITHUB_ICON_PATH).resize((20, 20))
github_icon = ImageTk.PhotoImage(icon_img)

def open_github(event=None):
    webbrowser.open_new(r"https://github.com/Kurok00/PhatSotToolV2")

def on_github_hover(event):
    label_github.config(bg=JT_WHITE, fg=JT_TITLE, highlightbackground=JT_TITLE, highlightcolor=JT_TITLE)

def on_github_leave(event):
    label_github.config(bg=JT_TITLE, fg=JT_BTN_TEXT, highlightbackground=JT_TITLE, highlightcolor=JT_TITLE)

label_github = tk.Label(
    root,
    text=" GitHub: Kurok00/PhatSotToolV2",
    font=("Arial", 10, "bold"),
    fg=JT_BTN_TEXT,           # Chữ trắng
    bg=JT_TITLE,              # Nền đỏ J&T
    anchor="w",
    bd=1,
    relief="solid",
    highlightbackground=JT_TITLE,
    highlightcolor=JT_TITLE,
    highlightthickness=1,
    padx=10,
    pady=2,
    cursor="hand2",
    image=github_icon,
    compound="left"
)
label_github.place(relx=0.0, y=8, anchor="nw")
label_github.bind("<Button-1>", open_github)
label_github.bind("<Enter>", on_github_hover)
label_github.bind("<Leave>", on_github_leave)
# Bo góc nhẹ (nếu tk 8.6+):
try:
    label_github.config(borderwidth=1)
    label_github.after(100, lambda: label_github.tk.call(label_github._w, 'configure', '-borderwidth', 1, '-relief', 'solid'))
except:
    pass

# ======= LABEL MADE BY GÓC PHẢI TRÊN =======
label_madeby = tk.Label(
    root,
    text="Made By Ân Vnt 028R07",
    font=("Arial", 10, "italic"),
    fg=JT_BTN_TEXT,           # Chữ trắng
    bg=JT_TITLE,              # Nền đỏ J&T
    anchor="e",
    bd=1,
    relief="solid",
    highlightbackground=JT_TITLE,
    highlightcolor=JT_TITLE,
    highlightthickness=1,
    padx=10,
    pady=2
)
label_madeby.place(relx=1.0, y=8, anchor="ne")
# Bo góc nhẹ (nếu tk 8.6+):
try:
    label_madeby.config(borderwidth=1)
    label_madeby.after(100, lambda: label_madeby.tk.call(label_madeby._w, 'configure', '-borderwidth', 1, '-relief', 'solid'))
except:
    pass

# ======= TIÊU ĐỀ TOOL =======
title = tk.Label(root, text="Tool Tra Cứu J&T", font=("Arial", 22, "bold"), fg=JT_TITLE, bg=JT_GRAY)
title.pack(pady=(12, 8))

# ======= KHUNG AUTH & MÃ VẬN ĐƠN =======
frame_top = tk.LabelFrame(root, text="Tra cứu Tên Shipper từ Mã Vận đơn", font=("Arial", 13, "bold"), fg=JT_TITLE, bg=JT_WHITE, bd=2, relief=tk.GROOVE, labelanchor="n")
frame_top.pack(fill="x", padx=40, pady=(10, 14))

# Khai báo biến ngày đầu/tháng cuối tháng hiện tại (dùng cho cả 2 khung)
now = datetime.datetime.now()
first_day = now.replace(day=1)
last_day = now.replace(day=calendar.monthrange(now.year, now.month)[1])

# Hàng nhập token
lbl_token = tk.Label(frame_top, text="Nhập authToken:", font=("Arial", 12, "bold"), fg=JT_LABEL, bg=JT_WHITE)
lbl_token.grid(row=0, column=0, sticky="e", padx=(18, 6), pady=(16, 8))
txt_token = tk.Entry(frame_top, width=38, font=("Arial", 13), bg=JT_GRAY, relief=tk.GROOVE, bd=2)
txt_token.grid(row=0, column=1, padx=(0, 0), pady=(16, 8), sticky="we")
btn_get_token_debug = tk.Button(frame_top, text="Lấy Token Auto", command=get_token_from_chrome_debug, font=("Arial", 11, "bold"), bg=JT_RED, fg=JT_BTN_TEXT, relief=tk.RAISED, bd=2, activebackground="#ff8a80", width=14, height=1)
btn_get_token_debug.grid(row=0, column=2, padx=(10, 18), pady=(16, 8), sticky="w")
frame_top.grid_columnconfigure(1, weight=1)

# Hàng nhập mã vận đơn
lbl_waybills = tk.Label(frame_top, text="Nhập mã vận đơn (mỗi dòng 1 mã):", font=("Arial", 12, "bold"), fg=JT_LABEL, bg=JT_WHITE)
lbl_waybills.grid(row=1, column=0, sticky="ne", padx=(18, 6), pady=(2, 16))
txt_waybills = tk.Text(frame_top, height=5, width=38, font=("Arial", 13), bg=JT_GRAY, relief=tk.GROOVE, bd=2)
txt_waybills.grid(row=1, column=1, columnspan=2, padx=(0, 18), pady=(2, 16), sticky="we")
txt_waybills.bind("<Return>", lambda event: (tra_cuu(), "break"))

# Thêm field chọn ngày start/end
lbl_start_top = tk.Label(frame_top, text="Từ ngày:", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_start_top.grid(row=2, column=0, sticky="e", padx=(18, 4), pady=(2, 8))
date_start_top = DateEntry(frame_top, width=12, font=("Arial", 12), date_pattern="yyyy-mm-dd", background=JT_RED_LIGHT, foreground=JT_TITLE, borderwidth=2)
date_start_top.set_date(first_day)
date_start_top.grid(row=2, column=1, sticky="w", padx=(0, 8), pady=(2, 8))
lbl_end_top = tk.Label(frame_top, text="Đến ngày:", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_end_top.grid(row=2, column=1, sticky="e", padx=(180, 4), pady=(2, 8))
date_end_top = DateEntry(frame_top, width=12, font=("Arial", 12), date_pattern="yyyy-mm-dd", background=JT_RED_LIGHT, foreground=JT_TITLE, borderwidth=2)
date_end_top.set_date(last_day)
date_end_top.grid(row=2, column=2, sticky="w", padx=(0, 18), pady=(2, 8))

btn_tra_cuu = tk.Button(frame_top, text="Tra cứu", command=tra_cuu, font=("Arial", 12, "bold"), bg=JT_RED, fg=JT_BTN_TEXT, relief=tk.RAISED, bd=2, activebackground="#ff8a80", width=12)
btn_tra_cuu.grid(row=3, column=2, sticky="e", padx=(0, 18), pady=(0, 12))

# ======= KHUNG TRA CỨU SHIPPER =======
frame_shipper = tk.LabelFrame(root, text="Tra cứu tên shipper từ số điện thoại", font=("Arial", 13, "bold"), fg=JT_TITLE, bg=JT_WHITE, bd=2, relief=tk.GROOVE, labelanchor="n")
frame_shipper.pack(fill="x", padx=40, pady=(0, 14))

lbl_phone = tk.Label(frame_shipper, text="Số điện thoại:", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_phone.grid(row=0, column=0, sticky="w", padx=(8, 4), pady=8)
txt_phone = tk.Entry(frame_shipper, width=18, font=("Arial", 14, "bold"), fg=JT_TITLE, bg=JT_GRAY, relief=tk.GROOVE, bd=3)
txt_phone.grid(row=0, column=1, padx=(0, 12), pady=8)
txt_phone.bind("<Return>", lambda event: tra_cuu_shipper())
lbl_start = tk.Label(frame_shipper, text="Từ ngày:", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_start.grid(row=0, column=2, sticky="w", padx=(0, 4))
# Khai báo biến ngày đầu/tháng cuối tháng hiện tại
now = datetime.datetime.now()
first_day = now.replace(day=1)
last_day = now.replace(day=calendar.monthrange(now.year, now.month)[1])
date_start = DateEntry(frame_shipper, width=12, font=("Arial", 12), date_pattern="yyyy-mm-dd", background=JT_RED_LIGHT, foreground=JT_TITLE, borderwidth=2)
date_start.set_date(first_day)
date_start.grid(row=0, column=3, padx=(0, 8))
lbl_end = tk.Label(frame_shipper, text="Đến ngày:", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_end.grid(row=0, column=4, sticky="w", padx=(0, 4))
date_end = DateEntry(frame_shipper, width=12, font=("Arial", 12), date_pattern="yyyy-mm-dd", background=JT_RED_LIGHT, foreground=JT_TITLE, borderwidth=2)
date_end.set_date(last_day)
date_end.grid(row=0, column=5, padx=(0, 8))
btn_tra_cuu_shipper = tk.Button(frame_shipper, text="Tra cứu tên shipper", command=tra_cuu_shipper, font=("Arial", 12, "bold"), bg=JT_RED, fg=JT_BTN_TEXT, relief=tk.RAISED, bd=2, activebackground="#ff8a80", width=18)
btn_tra_cuu_shipper.grid(row=0, column=6, padx=(0, 8), pady=2)
lbl_shipper_result = tk.Label(frame_shipper, text="Tên shipper: ...", fg=JT_TITLE, font=("Arial", 13, "bold"), bg=JT_WHITE)
lbl_shipper_result.grid(row=1, column=0, columnspan=7, sticky="w", pady=(10,0), padx=(8,0))

# ======= KHUNG KẾT QUẢ TREEVIEW =======
frame = tk.LabelFrame(root, text="Kết quả tra cứu", font=("Arial", 13, "bold"), fg=JT_TITLE, bg=JT_GRAY, bd=2, relief=tk.GROOVE, labelanchor="n")
frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 24))

cols = ("Mã vận đơn", "Số điện thoại", "Tên shipper")
tree = ttk.Treeview(frame, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=220, anchor="center")
tree.pack(fill=tk.BOTH, expand=True)

# ======= STYLE TREEVIEW =======
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview",
    background=JT_GRAY,
    foreground=JT_LABEL,
    rowheight=32,
    fieldbackground=JT_GRAY,
    font=("Arial", 12)
)
style.configure("Treeview.Heading",
    background=JT_RED,
    foreground=JT_BTN_TEXT,
    font=("Arial", 12, "bold")
)

# Thêm label thông báo copy ở giữa dưới giao diện
copy_notify_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg=JT_TITLE, bg="#fff", bd=2, relief="groove")
copy_notify_label.place(relx=0.5, rely=1.0, anchor="s", y=-24)
copy_notify_label.lower()  # Ẩn mặc định

def show_copy_notify(msg, color=JT_TITLE):
    copy_notify_label.config(text=msg, fg=color)
    copy_notify_label.lift()
    # Fade out effect sau 2s
    def fade_out(alpha=1.0):
        if alpha <= 0:
            copy_notify_label.lower()
            copy_notify_label.config(fg=color)  # reset lại màu cho lần sau
            return
        copy_notify_label.config(fg=color, bg="#fff")
        copy_notify_label.tk.call(copy_notify_label._w, 'configure', '-foreground', color)
        copy_notify_label.tk.call(copy_notify_label._w, 'configure', '-background', '#fff')
        copy_notify_label.attributes = getattr(copy_notify_label, 'attributes', {})
        copy_notify_label.attributes['alpha'] = alpha
        # Giả lập fade bằng cách giảm màu chữ (opacity không native với Label, nên chỉ giảm dần màu)
        gray = int(255 * (1 - alpha))
        fg_fade = f"#{gray:02x}{gray:02x}{gray:02x}"
        copy_notify_label.config(fg=fg_fade)
        copy_notify_label.after(50, lambda: fade_out(alpha - 0.1))
    copy_notify_label.after(2000, fade_out)

def on_treeview_double_click(event):
    item = tree.identify_row(event.y)
    col = tree.identify_column(event.x)
    if not item or not col:
        return
    col_idx = int(col.replace('#', '')) - 1
    values = tree.item(item, 'values')
    if col_idx < 0 or col_idx >= len(values):
        return
    value = values[col_idx]
    if value:
        root.clipboard_clear()
        root.clipboard_append(value)
        root.update()  # Đảm bảo clipboard nhận giá trị
        show_copy_notify(f"Đã copy: {value}")

tree.bind("<Double-1>", on_treeview_double_click)

root.update()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop() 