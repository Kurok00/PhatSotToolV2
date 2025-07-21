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
            tree.insert("", tk.END, values=(waybill, phone))
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
            messagebox.showinfo('Thành công', 'Lấy token thành công!')
        else:
            messagebox.showerror('Lỗi', 'Không tìm thấy YL_TOKEN trong localStorage!')
    except Exception as e:
        messagebox.showerror('Lỗi', f'Lấy token thất bại: {e}')

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
            messagebox.showinfo('Thành công', 'Lấy token từ Chrome đang mở thành công!')
        else:
            messagebox.showerror('Lỗi', 'Không tìm thấy YL_TOKEN trong localStorage!')
    except Exception as e:
        messagebox.showerror('Lỗi', f'Lấy token thất bại: {e}')

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

# ======= TIÊU ĐỀ TOOL =======
title = tk.Label(root, text="Tool tra cứu số điện thoại theo mã vận đơn", font=("Arial", 18, "bold"), fg=JT_TITLE, bg=JT_GRAY)
title.pack(pady=(12, 8))

# ======= KHUNG AUTH & MÃ VẬN ĐƠN =======
frame_top = tk.Frame(root, bg=JT_WHITE, bd=2, relief=tk.GROOVE)
frame_top.pack(fill="x", padx=30, pady=(0, 10))

lbl_token = tk.Label(frame_top, text="Nhập authToken:", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_token.grid(row=0, column=0, sticky="w", padx=(12, 4), pady=(10, 2))
txt_token = tk.Entry(frame_top, width=80, font=("Arial", 12), bg=JT_GRAY, relief=tk.GROOVE, bd=2)
txt_token.grid(row=0, column=1, padx=(0, 12), pady=(10, 2))

lbl_waybills = tk.Label(frame_top, text="Nhập mã vận đơn (mỗi dòng 1 mã):", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_waybills.grid(row=1, column=0, sticky="nw", padx=(12, 4), pady=(2, 10))
txt_waybills = tk.Text(frame_top, height=6, width=80, font=("Arial", 12), bg=JT_GRAY, relief=tk.GROOVE, bd=2)
txt_waybills.grid(row=1, column=1, padx=(0, 12), pady=(2, 10))

btn_tra_cuu = tk.Button(frame_top, text="Tra cứu", command=tra_cuu, font=("Arial", 12, "bold"), bg=JT_RED, fg=JT_BTN_TEXT, relief=tk.RAISED, bd=2, activebackground="#ff8a80")
btn_tra_cuu.grid(row=2, column=1, sticky="e", padx=(0, 12), pady=(0, 10))

# ======= KHUNG TRA CỨU SHIPPER =======
frame_shipper = tk.LabelFrame(root, text="Tra cứu tên shipper từ số điện thoại", padx=16, pady=12, font=("Arial", 12, "bold"), fg=JT_TITLE, bg=JT_WHITE, bd=2, relief=tk.GROOVE, labelanchor="n")
frame_shipper.pack(fill="x", padx=30, pady=(0, 10))

# Khai báo biến ngày đầu/tháng cuối tháng hiện tại
now = datetime.datetime.now()
first_day = now.replace(day=1)
last_day = now.replace(day=calendar.monthrange(now.year, now.month)[1])

lbl_phone = tk.Label(frame_shipper, text="Số điện thoại:", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_phone.grid(row=0, column=0, sticky="w", padx=(0, 4), pady=4)
txt_phone = tk.Entry(frame_shipper, width=20, font=("Arial", 15, "bold"), fg=JT_TITLE, bg=JT_GRAY, relief=tk.GROOVE, bd=3)
txt_phone.grid(row=0, column=1, padx=(0, 12), pady=4)

lbl_start = tk.Label(frame_shipper, text="Từ ngày:", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_start.grid(row=0, column=2, sticky="w", padx=(0, 4))
date_start = DateEntry(frame_shipper, width=12, font=("Arial", 12), date_pattern="yyyy-mm-dd", background=JT_RED_LIGHT, foreground=JT_TITLE, borderwidth=2)
date_start.set_date(first_day)
date_start.grid(row=0, column=3, padx=(0, 8))

lbl_end = tk.Label(frame_shipper, text="Đến ngày:", font=("Arial", 12), fg=JT_LABEL, bg=JT_WHITE)
lbl_end.grid(row=0, column=4, sticky="w", padx=(0, 4))
date_end = DateEntry(frame_shipper, width=12, font=("Arial", 12), date_pattern="yyyy-mm-dd", background=JT_RED_LIGHT, foreground=JT_TITLE, borderwidth=2)
date_end.set_date(last_day)
date_end.grid(row=0, column=5, padx=(0, 8))

btn_tra_cuu_shipper = tk.Button(frame_shipper, text="Tra cứu tên shipper", command=tra_cuu_shipper, font=("Arial", 12, "bold"), bg=JT_RED, fg=JT_BTN_TEXT, relief=tk.RAISED, bd=2, activebackground="#ff8a80")
btn_tra_cuu_shipper.grid(row=0, column=6, padx=(0, 0), pady=2)

lbl_shipper_result = tk.Label(frame_shipper, text="Tên shipper: ...", fg=JT_TITLE, font=("Arial", 13, "bold"), bg=JT_WHITE)
lbl_shipper_result.grid(row=1, column=0, columnspan=7, sticky="w", pady=(10,0))

# ======= KHUNG NÚT LẤY TOKEN =======
frame_token = tk.Frame(root, bg=JT_GRAY)
frame_token.pack(fill="x", padx=30, pady=(0, 10))
btn_get_token_debug = tk.Button(frame_token, text="Lấy token từ Chrome đang mở (debug)", command=get_token_from_chrome_debug, font=("Arial", 12), bg=JT_RED, fg=JT_BTN_TEXT, relief=tk.RAISED, bd=2, activebackground="#ff8a80")
btn_get_token_debug.pack(pady=4)

# ======= KHUNG KẾT QUẢ TREEVIEW =======
frame = tk.Frame(root, bg=JT_GRAY)
frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))

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

root.update()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop() 