# Script chạy Tool J&T với virtual environment
Write-Host "================================" -ForegroundColor Cyan
Write-Host "    🚀 KHỞI CHẠY TOOL J&T 🚀    " -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Đang kích hoạt virtual environment..." -ForegroundColor Green
& ".\.venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Virtual environment đã được kích hoạt! ✅" -ForegroundColor Green
Write-Host ""

Write-Host "Đang chạy ứng dụng..." -ForegroundColor Magenta
Write-Host ""

python main.py

Write-Host ""
Write-Host "Ứng dụng đã đóng. Nhấn phím bất kỳ để thoát..." -ForegroundColor Yellow
Read-Host
