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
import random
import sys

# ======= HOT RELOAD FUNCTION =======
def hot_reload():
    """Hot reload function - Reload app without restarting"""
    try:
        # Import lại module hiện tại
        import importlib
        current_module = sys.modules[__name__]
        importlib.reload(current_module)
        
        # Đóng window hiện tại
        root.quit()
        root.destroy()
        
        # Restart app
        os.system(f'python "{__file__}"')
        
    except Exception as e:
        show_copy_notify(f"Hot reload failed: {e}", JT_ERROR)

# ======= BIẾN TOÀN CỤC & HÀM TIỆN ÍCH (KHAI BÁO ĐẦU FILE) =======
now = datetime.datetime.now()
def get_month_list(years_back=2):
    months = []
    for y in range(now.year, now.year-years_back, -1):
        for m in range(12, 0, -1):
            if y == now.year and m > now.month:
                continue
            months.append(f"{m:02d}-{y}")
    return months
month_list = get_month_list(3)
def get_start_end_from_month(month_str):
    m, y = map(int, month_str.split("-"))
    start = datetime.date(y, m, 1)
    if y == now.year and m == now.month:
        end = now.date()
    else:
        end = datetime.date(y, m, calendar.monthrange(y, m)[1])
    return start, end

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
        "routerNameList": "%E7%BD%91%E7%82%B9%E7%82%B9%E7%BB%8F%E8%90%A5%3E%E8%BF%90%E5%8D%95%E7%AE%A1%E7%90%86%3E%E6%B4%BE%E4%BB%B6%E8%BF%90%E5%8D%95%E7%AE%A1%E7%90%86",
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

# Hàm xử lý khi nhấn nút tra cứu - Updated for new UI với cancel
def tra_cuu():
    waybills = txt_waybills.get("1.0", tk.END).strip().splitlines()
    auth_token = txt_token.get().strip()
    start, end = get_start_end_from_month(cb_month_top.get())
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    
    if not waybills or not auth_token:
        messagebox.showwarning("⚠️ Thiếu thông tin", "Vui lòng nhập mã vận đơn và authToken!")
        return
    
    # Check if currently processing
    if hasattr(tra_cuu, 'is_processing') and tra_cuu.is_processing:
        # Cancel current operation
        tra_cuu.should_cancel = True
        btn_tra_cuu.config(text="🛑 ĐANG HỦY...", bg=JT_WARNING)
        return
        
    # Start processing
    tra_cuu.is_processing = True
    tra_cuu.should_cancel = False
    
    # Update UI state
    btn_tra_cuu.config(state=tk.NORMAL, text="🛑 HỦY", bg=JT_ERROR)
    for row in tree.get_children():
        tree.delete(row)
    
    def show_countdown(secs):
        if hasattr(tra_cuu, 'should_cancel') and tra_cuu.should_cancel:
            return
        countdown_frame.pack(fill=tk.X, pady=(8, 0))
        def update(sec_left):
            if sec_left <= 0 or (hasattr(tra_cuu, 'should_cancel') and tra_cuu.should_cancel):
                countdown_label.config(text="")
                countdown_frame.pack_forget()
                return
            countdown_label.config(text=f"⏳ Chờ {sec_left}s để tránh spam...")
            countdown_label.after(1000, lambda: update(sec_left-1))
        update(secs)
    
    def worker():
        success_count = 0
        processed_count = 0
        total_count = len([w for w in waybills if w.strip()])
        
        for idx, waybill in enumerate(waybills):
            # Check for cancellation
            if hasattr(tra_cuu, 'should_cancel') and tra_cuu.should_cancel:
                break
                
            waybill = waybill.strip()
            if not waybill:
                continue
                
            processed_count += 1
            
            # Update progress in button
            progress = f"📊 {processed_count}/{total_count}"
            btn_tra_cuu.config(text=progress)
            
            phone = fetch_phone(waybill, auth_token)
            
            # Check for cancellation after API call
            if hasattr(tra_cuu, 'should_cancel') and tra_cuu.should_cancel:
                break
            
            # Auto lookup shipper if valid phone
            if phone and phone.isdigit() and len(phone) >= 8:
                ten_shipper = fetch_shipper(phone, auth_token, start, end)
                if not ten_shipper or 'không' in ten_shipper.lower() or 'lỗi' in ten_shipper.lower():
                    ten_shipper = "Không tìm thấy shipper"
                else:
                    success_count += 1
            else:
                ten_shipper = ""
            
            tree.insert("", tk.END, values=(waybill, phone, ten_shipper))
            
            # Stealth mode delay
            if stealth_mode.get() and idx < len(waybills) - 1:  # Don't delay on last item
                try:
                    dmin = int(delay_min.get())
                    dmax = int(delay_max.get())
                    if dmin > dmax:
                        dmin, dmax = dmax, dmin
                except:
                    dmin, dmax = 5, 10
                delay = random.randint(dmin, dmax)
                show_countdown(delay)
                for i in range(delay):
                    if hasattr(tra_cuu, 'should_cancel') and tra_cuu.should_cancel:
                        break
                    time.sleep(1)
                countdown_frame.pack_forget()
        
        # Reset UI state
        tra_cuu.is_processing = False
        btn_tra_cuu.config(
            state=tk.NORMAL, 
            text="🚀 BẮT ĐẦU TRA CỨU", 
            bg=JT_RED
        )
        
        # Show completion message
        if hasattr(tra_cuu, 'should_cancel') and tra_cuu.should_cancel:
            completion_msg = f"🛑 Đã hủy! Đã tra cứu {processed_count}/{total_count} đơn"
            show_copy_notify(completion_msg, JT_WARNING)
        else:
            completion_msg = f"✅ Hoàn thành! Tra cứu được {success_count}/{total_count} shipper"
            show_copy_notify(completion_msg, JT_RESULT)
        
    threading.Thread(target=worker, daemon=True).start()

# Định nghĩa hàm tra_cuu_shipper TRƯỚC
def tra_cuu_shipper():
    phone = txt_phone.get().strip()
    auth_token = txt_token.get().strip()
    start, end = get_start_end_from_month(cb_month_shipper.get())
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    if not phone or not auth_token or not start or not end:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ SĐT, token, tháng!")
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

# ======= ENHANCED STYLE J&T =======
JT_RED = "#e60012"         # Đỏ J&T chính
JT_RED_LIGHT = "#ffebee"   # Đỏ nhạt
JT_RED_DARK = "#b71c1c"    # Đỏ đậm
JT_GRAY = "#f8f9fa"        # Xám nền modern
JT_GRAY_LIGHT = "#ffffff"  # Trắng
JT_GRAY_DARK = "#6c757d"   # Xám đậm
JT_WHITE = "#ffffff"
JT_LABEL = "#212529"       # Đen nhẹ
JT_BTN_TEXT = "#fff"
JT_TITLE = JT_RED
JT_RESULT = "#28a745"      # Xanh success
JT_ERROR = "#dc3545"       # Đỏ error
JT_WARNING = "#ffc107"     # Vàng warning
JT_INFO = "#17a2b8"        # Xanh info

# Shadow effects
JT_SHADOW = "#e9ecef"

# KHỞI TẠO ROOT TRƯỚC
root = tk.Tk()
root.title("🚚 Tool Tra Cứu J&T Express - v2.0")
root.geometry("1200x900")  # Tăng thêm width cho đẹp
root.resizable(True, True)
root.configure(bg=JT_GRAY)
root.minsize(1000, 700)

# Set icon nếu có
try:
    root.iconbitmap("Logo_JT.ico") if os.path.exists("Logo_JT.ico") else None
except:
    pass

# ======= KHỞI TẠO TKINTER VARIABLES SAU ROOT =======
stealth_mode = tk.BooleanVar(value=True)
delay_min = tk.IntVar(value=5)
delay_max = tk.IntVar(value=10)

# ======= MAIN CONTAINER WITH PADDING =======
main_container = tk.Frame(root, bg=JT_GRAY)
main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# ======= MODERN HEADER SECTION =======
header_frame = tk.Frame(main_container, bg=JT_GRAY, height=80)
header_frame.pack(fill=tk.X, pady=(0, 20))
header_frame.pack_propagate(False)

# Header top row - Links và buttons
header_top = tk.Frame(header_frame, bg=JT_GRAY, height=35)
header_top.pack(fill=tk.X, pady=(5, 0))

# GitHub repository button - Enhanced với viền
github_frame = tk.Frame(header_top, bg=JT_RED, relief=tk.RAISED, bd=1)
github_frame.pack(side=tk.LEFT)

def open_github(event=None):
    webbrowser.open_new(r"https://github.com/Kurok00/PhatSotToolV2")

def on_github_hover(event):
    github_frame.config(bg=JT_RED_DARK)
    github_label.config(bg=JT_RED_DARK)

def on_github_leave(event):
    github_frame.config(bg=JT_RED)
    github_label.config(bg=JT_RED)

# Sử dụng icon GitHub Unicode thay vì file ảnh
github_label = tk.Label(
    github_frame,
    text="� GitHub Repository",
    font=("Segoe UI", 9, "bold"),
    fg=JT_WHITE,
    bg=JT_RED,
    padx=12,
    pady=6,
    cursor="hand2"
)
github_label.pack()
github_label.bind("<Button-1>", open_github)
github_label.bind("<Enter>", on_github_hover)
github_label.bind("<Leave>", on_github_leave)
github_frame.bind("<Button-1>", open_github)
github_frame.bind("<Enter>", on_github_hover)
github_frame.bind("<Leave>", on_github_leave)

# Reset Tool Button - Changed from Hot Reload
# Reset Tool Function - Real reset functionality
def reset_tool():
    """Reset tool về trạng thái ban đầu"""
    try:
        # Xóa token
        txt_token.delete(0, tk.END)
        
        # Xóa mã vận đơn
        txt_waybills.delete("1.0", tk.END)
        
        # Xóa số điện thoại
        txt_phone.delete(0, tk.END)
        
        # Reset tháng về tháng hiện tại
        cb_month_top.set(f"{now.month:02d}-{now.year}")
        cb_month_shipper.set(f"{now.month:02d}-{now.year}")
        
        # Cập nhật range hiển thị
        update_range_top()
        update_range_shipper()
        
        # Xóa kết quả treeview
        for row in tree.get_children():
            tree.delete(row)
        
        # Reset kết quả shipper
        lbl_shipper_result.config(text="Kết quả sẽ hiển thị ở đây...", fg=JT_GRAY_DARK)
        
        # Reset counter
        update_waybill_count()
        
        # Reset button states
        btn_tra_cuu.config(state=tk.NORMAL, text="🚀 BẮT ĐẦU TRA CỨU", bg=JT_RED)
        btn_tra_cuu_shipper.config(state=tk.NORMAL)
        
        # Ẩn countdown frame nếu đang hiển thị
        countdown_frame.pack_forget()
        
        # Reset delay values về mặc định
        delay_min.set(5)
        delay_max.set(10)
        
        # Reset stealth mode về True
        stealth_mode.set(True)
        
        # Hiển thị thông báo reset thành công
        show_copy_notify("🔄 Tool đã được reset về trạng thái ban đầu!", JT_RESULT)
        
    except Exception as e:
        show_copy_notify(f"❌ Lỗi khi reset tool: {e}", JT_ERROR)

def on_reset_hover(event):
    reset_frame.config(bg=JT_WARNING)
    reset_label.config(bg=JT_WARNING)

def on_reset_leave(event):
    reset_frame.config(bg=JT_INFO)
    reset_label.config(bg=JT_INFO)

reset_frame = tk.Frame(header_top, bg=JT_INFO, relief=tk.RAISED, bd=1)
reset_frame.pack(side=tk.LEFT, padx=(10, 0))

reset_label = tk.Label(
    reset_frame,
    text="� Reset Tool",
    font=("Segoe UI", 9, "bold"),
    fg=JT_WHITE,
    bg=JT_INFO,
    padx=12,
    pady=6,
    cursor="hand2"
)
reset_label.pack()
reset_label.bind("<Button-1>", lambda e: reset_tool())
reset_label.bind("<Enter>", on_reset_hover)
reset_label.bind("<Leave>", on_reset_leave)
reset_frame.bind("<Button-1>", lambda e: reset_tool())
reset_frame.bind("<Enter>", on_reset_hover)
reset_frame.bind("<Leave>", on_reset_leave)

# Made by label - Right side với khung đỏ chữ đen đậm
madeby_frame = tk.Frame(header_top, bg=JT_RED, relief=tk.RAISED, bd=2)
madeby_frame.pack(side=tk.RIGHT, padx=(0, 5))

madeby_label = tk.Label(
    madeby_frame,
    text="Made with 💖 by Chú 7 Dog",
    font=("Segoe UI", 9, "bold"),
    fg=JT_WHITE,
    bg=JT_RED,
    padx=12,
    pady=6
)
madeby_label.pack()

# Main title - Modern typography
title_frame = tk.Frame(header_frame, bg=JT_GRAY)
title_frame.pack(expand=True, fill=tk.BOTH)

title = tk.Label(
    title_frame, 
    text="🚚 Tool Tra Cứu J&T Express", 
    font=("Segoe UI", 24, "bold"), 
    fg=JT_TITLE, 
    bg=JT_GRAY
)
title.pack(expand=True)

subtitle = tk.Label(
    title_frame,
    text="Tra cứu thông tin shipper & khách hàng nhanh chóng",
    font=("Segoe UI", 11),
    fg=JT_GRAY_DARK,
    bg=JT_GRAY
)
subtitle.pack()

# ======= MODERN CARD-BASED LAYOUT =======
# Main content container
content_container = tk.Frame(main_container, bg=JT_GRAY)
content_container.pack(fill=tk.BOTH, expand=True)

# Left panel - Forms
left_panel = tk.Frame(content_container, bg=JT_GRAY, width=580)
left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
left_panel.pack_propagate(False)

# Right panel - Results  
right_panel = tk.Frame(content_container, bg=JT_GRAY)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# ======= CARD 1: BATCH LOOKUP - Enhanced với viền =======
card1 = tk.LabelFrame(
    left_panel, 
    text="  📦 Tra cứu Batch (Nhiều mã vận đơn)  ", 
    font=("Segoe UI", 12, "bold"), 
    fg=JT_TITLE, 
    bg=JT_WHITE, 
    bd=2,
    relief=tk.GROOVE,
    padx=15,
    pady=15
)
card1.pack(fill=tk.X, pady=(0, 15))

# Token input - Modern design
token_frame = tk.Frame(card1, bg=JT_WHITE)
token_frame.pack(fill=tk.X, pady=(0, 12))

tk.Label(
    token_frame, 
    text="🔑 Auth Token:", 
    font=("Segoe UI", 10, "bold"), 
    fg=JT_LABEL, 
    bg=JT_WHITE
).pack(anchor=tk.W, pady=(0, 4))

token_input_frame = tk.Frame(token_frame, bg=JT_WHITE)
token_input_frame.pack(fill=tk.X)

txt_token = tk.Entry(
    token_input_frame, 
    font=("Consolas", 10), 
    bg=JT_GRAY, 
    relief=tk.SUNKEN, 
    bd=2,
    fg=JT_LABEL
)
txt_token.pack(side=tk.LEFT, fill=tk.X, expand=True)

btn_get_token_debug = tk.Button(
    token_input_frame, 
    text="� Auto Đăng nhập", 
    command=get_token_from_chrome_debug, 
    font=("Segoe UI", 9, "bold"), 
    bg=JT_INFO, 
    fg=JT_WHITE, 
    relief=tk.FLAT, 
    bd=0,
    padx=15,
    pady=8,
    cursor="hand2"
)
btn_get_token_debug.pack(side=tk.RIGHT, padx=(8, 0))

# Waybills input
waybills_frame = tk.Frame(card1, bg=JT_WHITE)
waybills_frame.pack(fill=tk.X, pady=(0, 12))

tk.Label(
    waybills_frame, 
    text="📝 Mã vận đơn (mỗi dòng 1 mã) - Enter để tra cứu:", 
    font=("Segoe UI", 10, "bold"), 
    fg=JT_LABEL, 
    bg=JT_WHITE
).pack(anchor=tk.W, pady=(0, 4))

txt_waybills = tk.Text(
    waybills_frame, 
    height=6, 
    font=("Consolas", 10), 
    bg=JT_GRAY, 
    relief=tk.SUNKEN, 
    bd=2,
    fg=JT_LABEL,
    wrap=tk.WORD
)
txt_waybills.pack(fill=tk.X)

# Counter và controls row
counter_controls_frame = tk.Frame(card1, bg=JT_WHITE)
counter_controls_frame.pack(fill=tk.X, pady=(8, 12))

# Left side - Counter
counter_side = tk.Frame(counter_controls_frame, bg=JT_WHITE)
counter_side.pack(side=tk.LEFT)

frame_count = tk.Frame(counter_side, bg=JT_RED, relief=tk.RAISED, bd=2)
frame_count.pack()

lbl_count_title = tk.Label(
    frame_count, 
    text="📊 Đã nhập:", 
    font=("Segoe UI", 8, "bold"), 
    fg=JT_WHITE, 
    bg=JT_RED
)
lbl_count_title.pack(padx=8, pady=(4, 0))

lbl_count_waybills = tk.Label(
    frame_count, 
    text="0", 
    font=("Segoe UI", 14, "bold"), 
    fg=JT_WHITE, 
    bg=JT_RED, 
    width=6
)
lbl_count_waybills.pack(padx=8, pady=(0, 4))

# Right side - Month selector
month_side = tk.Frame(counter_controls_frame, bg=JT_WHITE)
month_side.pack(side=tk.RIGHT)

tk.Label(
    month_side, 
    text="📅 Tháng tra cứu:", 
    font=("Segoe UI", 9), 
    fg=JT_LABEL, 
    bg=JT_WHITE
).pack()

cb_month_top = ttk.Combobox(
    month_side, 
    values=month_list, 
    font=("Segoe UI", 9), 
    width=12, 
    state="readonly"
)
cb_month_top.set(f"{now.month:02d}-{now.year}")
cb_month_top.pack(pady=(2, 0))

# Date range display
lbl_range_top = tk.Label(
    month_side, 
    text="", 
    font=("Segoe UI", 8), 
    fg=JT_GRAY_DARK, 
    bg=JT_WHITE
)
lbl_range_top.pack(pady=(2, 0))

def update_range_top(event=None):
    start, end = get_start_end_from_month(cb_month_top.get())
    lbl_range_top.config(text=f"{start.strftime('%d/%m')} - {end.strftime('%d/%m/%Y')}")
cb_month_top.bind("<<ComboboxSelected>>", update_range_top)
update_range_top()

# Stealth mode controls
stealth_frame = tk.Frame(card1, bg=JT_WHITE)
stealth_frame.pack(fill=tk.X, pady=(0, 12))

stealth_left = tk.Frame(stealth_frame, bg=JT_WHITE)
stealth_left.pack(side=tk.LEFT)

chk_stealth = tk.Checkbutton(
    stealth_left, 
    text="🥷 Chế độ chống Ban Acc", 
    variable=stealth_mode, 
    bg=JT_WHITE,
    font=("Segoe UI", 9),
    fg=JT_LABEL
)
chk_stealth.pack()

stealth_right = tk.Frame(stealth_frame, bg=JT_WHITE)
stealth_right.pack(side=tk.RIGHT)

tk.Label(
    stealth_right, 
    text="⏱️ Chờ:", 
    font=("Segoe UI", 9), 
    fg=JT_LABEL, 
    bg=JT_WHITE
).pack(side=tk.LEFT)

txt_delay_min = tk.Entry(
    stealth_right, 
    width=3, 
    textvariable=delay_min, 
    font=("Segoe UI", 9), 
    bg=JT_GRAY, 
    relief=tk.FLAT, 
    bd=4,
    justify=tk.CENTER
)
txt_delay_min.pack(side=tk.LEFT, padx=(4, 2))

tk.Label(stealth_right, text="-", font=("Segoe UI", 9), fg=JT_LABEL, bg=JT_WHITE).pack(side=tk.LEFT)

txt_delay_max = tk.Entry(
    stealth_right, 
    width=3, 
    textvariable=delay_max, 
    font=("Segoe UI", 9), 
    bg=JT_GRAY, 
    relief=tk.FLAT, 
    bd=4,
    justify=tk.CENTER
)
txt_delay_max.pack(side=tk.LEFT, padx=(2, 4))

tk.Label(stealth_right, text="giây", font=("Segoe UI", 9), fg=JT_GRAY_DARK, bg=JT_WHITE).pack(side=tk.LEFT)

# Main action button với viền
btn_tra_cuu = tk.Button(
    card1, 
    text="🚀 BẮT ĐẦU TRA CỨU", 
    command=tra_cuu, 
    font=("Segoe UI", 11, "bold"), 
    bg=JT_RED, 
    fg=JT_WHITE, 
    relief=tk.RAISED, 
    bd=2,
    pady=12,
    cursor="hand2"
)
btn_tra_cuu.pack(fill=tk.X)

# Progress/countdown frame với viền (hidden by default)
countdown_frame = tk.Frame(card1, bg=JT_WARNING, relief=tk.RAISED, bd=2)
countdown_frame.pack(fill=tk.X, pady=(8, 0))

countdown_label = tk.Label(
    countdown_frame, 
    text="", 
    font=("Segoe UI", 10, "bold"), 
    fg=JT_WHITE, 
    bg=JT_WARNING
)
countdown_label.pack(pady=6)
# Function đếm số mã vận đơn realtime với màu đẹp
def update_waybill_count(event=None):
    content = txt_waybills.get("1.0", tk.END).strip()
    if not content:
        count = 0
    else:
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        count = len(lines)
    
    lbl_count_waybills.config(text=str(count))
    
    # Modern color scheme
    if count == 0:
        color = JT_GRAY_DARK
    elif count <= 5:
        color = JT_RESULT  # Xanh success
    elif count <= 15:
        color = JT_WARNING  # Vàng warning  
    elif count <= 30:
        color = JT_INFO     # Xanh info
    else:
        color = JT_RED      # Đỏ khi quá nhiều
    
    frame_count.config(bg=color)
    lbl_count_title.config(bg=color)
    lbl_count_waybills.config(bg=color)

# Bind events
txt_waybills.bind('<KeyRelease>', update_waybill_count)
txt_waybills.bind('<Button-1>', update_waybill_count)
# Bind Enter key để tra cứu
txt_waybills.bind('<Return>', lambda event: tra_cuu())  # Enter để tra cứu
# ======= CARD 2: SINGLE LOOKUP - Enhanced với viền =======
card2 = tk.LabelFrame(
    left_panel, 
    text="  📞 Tra cứu Đơn lẻ (Theo SĐT)  ", 
    font=("Segoe UI", 12, "bold"), 
    fg=JT_TITLE, 
    bg=JT_WHITE, 
    bd=2,
    relief=tk.GROOVE,
    padx=15,
    pady=15
)
card2.pack(fill=tk.X)

# Phone input row
phone_row = tk.Frame(card2, bg=JT_WHITE)
phone_row.pack(fill=tk.X, pady=(0, 12))

phone_left = tk.Frame(phone_row, bg=JT_WHITE)
phone_left.pack(side=tk.LEFT, fill=tk.X, expand=True)

tk.Label(
    phone_left, 
    text="📱 Số điện thoại:", 
    font=("Segoe UI", 10, "bold"), 
    fg=JT_LABEL, 
    bg=JT_WHITE
).pack(anchor=tk.W, pady=(0, 4))

txt_phone = tk.Entry(
    phone_left, 
    font=("Consolas", 12, "bold"), 
    fg=JT_TITLE, 
    bg=JT_GRAY, 
    relief=tk.SUNKEN, 
    bd=2
)
txt_phone.pack(fill=tk.X)

# Month selector for single lookup
phone_right = tk.Frame(phone_row, bg=JT_WHITE, width=120)
phone_right.pack(side=tk.RIGHT, padx=(12, 0))
phone_right.pack_propagate(False)

tk.Label(
    phone_right, 
    text="📅 Tháng:", 
    font=("Segoe UI", 9), 
    fg=JT_LABEL, 
    bg=JT_WHITE
).pack(pady=(0, 4))

cb_month_shipper = ttk.Combobox(
    phone_right, 
    values=month_list, 
    font=("Segoe UI", 9), 
    width=10, 
    state="readonly"
)
cb_month_shipper.set(f"{now.month:02d}-{now.year}")
cb_month_shipper.pack()

lbl_range_shipper = tk.Label(
    phone_right, 
    text="", 
    font=("Segoe UI", 7), 
    fg=JT_GRAY_DARK, 
    bg=JT_WHITE
)
lbl_range_shipper.pack(pady=(2, 0))

def update_range_shipper(event=None):
    start, end = get_start_end_from_month(cb_month_shipper.get())
    lbl_range_shipper.config(text=f"{start.strftime('%d/%m')} - {end.strftime('%d/%m')}")
cb_month_shipper.bind("<<ComboboxSelected>>", update_range_shipper)
update_range_shipper()

# Action button với viền
btn_tra_cuu_shipper = tk.Button(
    card2, 
    text="🔍 TRA CỨU SHIPPER", 
    command=tra_cuu_shipper, 
    font=("Segoe UI", 10, "bold"), 
    bg=JT_INFO, 
    fg=JT_WHITE, 
    relief=tk.RAISED, 
    bd=2,
    pady=10,
    cursor="hand2"
)
btn_tra_cuu_shipper.pack(fill=tk.X, pady=(0, 10))

# Result display
lbl_shipper_result = tk.Label(
    card2, 
    text="Kết quả sẽ hiển thị ở đây...", 
    fg=JT_GRAY_DARK, 
    font=("Segoe UI", 10), 
    bg=JT_WHITE,
    wraplength=400,
    justify=tk.LEFT
)
lbl_shipper_result.pack(fill=tk.X)

# Bind Enter key for phone input
txt_phone.bind("<Return>", lambda event: tra_cuu_shipper())

# ======= MODERN RESULTS PANEL - Enhanced với viền =======
results_card = tk.LabelFrame(
    right_panel, 
    text="  📋 Kết quả tra cứu  ", 
    font=("Segoe UI", 12, "bold"), 
    fg=JT_TITLE, 
    bg=JT_WHITE, 
    bd=2,
    relief=tk.GROOVE,
    padx=15,
    pady=15
)
results_card.pack(fill=tk.BOTH, expand=True)

# Info bar
info_frame = tk.Frame(results_card, bg=JT_WHITE)
info_frame.pack(fill=tk.X, pady=(0, 10))

info_label = tk.Label(
    info_frame,
    text="💡 Double-click vào ô để copy dữ liệu",
    font=("Segoe UI", 9),
    fg=JT_GRAY_DARK,
    bg=JT_WHITE
)
info_label.pack(side=tk.LEFT)

# Results count
results_count_label = tk.Label(
    info_frame,
    text="📊 0 kết quả",
    font=("Segoe UI", 9, "bold"),
    fg=JT_INFO,
    bg=JT_WHITE
)
results_count_label.pack(side=tk.RIGHT)

# Treeview container with scrollbar
tree_container = tk.Frame(results_card, bg=JT_WHITE)
tree_container.pack(fill=tk.BOTH, expand=True)

# Modern treeview
cols = ("Mã vận đơn", "Số điện thoại", "Tên shipper")
tree = ttk.Treeview(tree_container, columns=cols, show="headings", height=30)

# Configure columns với đường kẻ dọc ngăn cách
tree.heading("Mã vận đơn", text="📦 Mã vận đơn")
tree.heading("Số điện thoại", text="📱 Số điện thoại") 
tree.heading("Tên shipper", text="👤 Tên shipper")

tree.column("Mã vận đơn", width=120, anchor="center", minwidth=100)
tree.column("Số điện thoại", width=120, anchor="center", minwidth=100)
tree.column("Tên shipper", width=180, anchor="w", minwidth=150)

# Scrollbars
v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Pack treeview and scrollbars
tree.grid(row=0, column=0, sticky="nsew")
v_scrollbar.grid(row=0, column=1, sticky="ns")
h_scrollbar.grid(row=1, column=0, sticky="ew")

tree_container.grid_rowconfigure(0, weight=1)
tree_container.grid_columnconfigure(0, weight=1)

# ======= MODERN TREEVIEW STYLE =======
style = ttk.Style()
style.theme_use('clam')  # Modern theme

# Configure treeview với đường kẻ grid cho dữ liệu
style.configure("Treeview",
    background=JT_WHITE,
    foreground=JT_LABEL,
    rowheight=35,
    fieldbackground=JT_WHITE,
    font=("Segoe UI", 10),
    borderwidth=1,
    relief="solid",
    focuscolor="none",
    selectbackground=JT_RED_LIGHT,
    selectforeground=JT_LABEL
)

# Configure heading không có viền  
style.configure("Treeview.Heading",
    background=JT_RED,
    foreground=JT_WHITE,
    font=("Segoe UI", 10, "bold"),
    borderwidth=0,
    relief="flat"
)

# Hover effects
style.map("Treeview",
    background=[('selected', JT_RED_LIGHT)],
    foreground=[('selected', JT_LABEL)]
)

style.map("Treeview.Heading",
    background=[('active', JT_RED_DARK)]
)

# ======= MODERN NOTIFICATION SYSTEM - Enhanced với viền =======
notification_frame = tk.Frame(main_container, bg=JT_GRAY, height=40, relief=tk.RIDGE, bd=1)
notification_frame.pack(fill=tk.X, side=tk.BOTTOM)
notification_frame.pack_propagate(False)

copy_notify_label = tk.Label(
    notification_frame, 
    text="", 
    font=("Segoe UI", 11, "bold"), 
    fg=JT_WHITE, 
    bg=JT_RESULT,
    relief=tk.FLAT,
    bd=0
)
copy_notify_label.pack(expand=True, fill=tk.BOTH)
copy_notify_label.pack_forget()  # Hide initially

def show_copy_notify(msg, color=JT_RESULT):
    copy_notify_label.config(text=f"  {msg}  ", bg=color)
    copy_notify_label.pack(expand=True, fill=tk.BOTH)
    
    # Auto hide after 3 seconds
    def hide_notification():
        copy_notify_label.pack_forget()
    
    copy_notify_label.after(3000, hide_notification)

# ======= ENHANCED DOUBLE-CLICK TO COPY WITH FLOATING NOTIFICATION =======
def show_floating_copy_notification(text, x, y):
    """Hiển thị thông báo copy nổi với animation"""
    # Tạo popup window cho thông báo
    popup = tk.Toplevel(root)
    popup.wm_overrideredirect(True)  # Bỏ title bar
    popup.configure(bg=JT_RESULT)
    popup.attributes('-topmost', True)  # Luôn ở trên cùng
    
    # Tính toán vị trí hiển thị
    popup_x = root.winfo_x() + x + 20
    popup_y = root.winfo_y() + y - 30
    popup.geometry(f"+{popup_x}+{popup_y}")
    
    # Tạo frame với viền đẹp
    frame = tk.Frame(popup, bg=JT_RESULT, relief=tk.RAISED, bd=2)
    frame.pack(padx=2, pady=2)
    
    # Icon và text
    label = tk.Label(
        frame,
        text=f"📋 Đã copy: {text}",
        font=("Segoe UI", 10, "bold"),
        fg=JT_WHITE,
        bg=JT_RESULT,
        padx=15,
        pady=8
    )
    label.pack()
    
    # Animation fade out
    alpha = 1.0
    def fade_out():
        nonlocal alpha
        alpha -= 0.05
        if alpha <= 0:
            popup.destroy()
            return
        try:
            popup.attributes('-alpha', alpha)
            popup.after(50, fade_out)
        except:
            popup.destroy()
    
    # Bắt đầu fade sau 2 giây
    popup.after(2000, fade_out)

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
        root.update()
        
        # Hiển thị thông báo nổi tại vị trí chuột
        show_floating_copy_notification(value, event.x_root - root.winfo_x(), event.y_root - root.winfo_y())
        
        # Vẫn giữ thông báo dưới để backup
        col_names = ["Mã vận đơn", "SĐT", "Tên shipper"]
        col_name = col_names[col_idx] if col_idx < len(col_names) else "Dữ liệu"
        show_copy_notify(f"📋 Đã copy {col_name}: {value}", JT_INFO)

tree.bind("<Double-1>", on_treeview_double_click)

# Update results count when tree changes
def update_results_count():
    count = len(tree.get_children())
    results_count_label.config(text=f"📊 {count} kết quả")

# Bind to tree changes (this is a simple approach, could be enhanced)
original_insert = tree.insert
def enhanced_insert(*args, **kwargs):
    result = original_insert(*args, **kwargs)
    root.after_idle(update_results_count)
    return result
tree.insert = enhanced_insert

original_delete = tree.delete
def enhanced_delete(*args, **kwargs):
    result = original_delete(*args, **kwargs)
    root.after_idle(update_results_count)
    return result
tree.delete = enhanced_delete

# Initialize
update_results_count()
root.mainloop() 