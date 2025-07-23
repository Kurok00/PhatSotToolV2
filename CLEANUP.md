# 🧹 Repository Cleanup Guide

Hướng dẫn dọn dẹp các file dư thừa trong repository để giữ cho codebase sạch sẽ và chuyên nghiệp.

## 🗑️ Files cần xóa

### 1. Build Artifacts & Executables
```bash
# Xóa toàn bộ thư mục build
Remove-Item -Recurse -Force .\build\

# Xóa các file .exe
Remove-Item -Force ".\J&T Express Tool v2.0.exe"
Remove-Item -Force ".\Phat-Sot-V1.1.exe"

# Xóa các file .spec cũ
Remove-Item -Force ".\fetch_phone_tool.spec"
Remove-Item -Force ".\Phat-Sot-V1.1.spec"
```

### 2. Archive Files
```bash
# Xóa các file nén cũ
Remove-Item -Force ".\J&T-Express-Tool-v2.0-Release.zip"
Remove-Item -Force ".\Phat-Sot-v1.1.rar"
Remove-Item -Force ".\Phat-Sot-V1.1.spec"
Remove-Item -Force ".\Phat-Sot-v1.1.zip"
Remove-Item -Force ".\Phat-Sot-V1.rar"
```

### 3. Chrome Debug Profile (Optional)
```bash
# Xóa Chrome debug profile (sẽ được tạo lại khi chạy tool)
Remove-Item -Recurse -Force .\chrome_debug_profile\
```

## ✅ Files cần giữ lại

### Core Application Files
- `main.py` - Main application code
- `main.spec` - PyInstaller spec for current version
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules

### Documentation
- `README.md` - Project documentation
- `SETUP.md` - Setup instructions
- `HOW_TO_RUN.md` - Running instructions

### Assets & Scripts
- `Logo_JT.ico` - Application icon
- `github_icon.png` - GitHub icon
- `Chrome.bat` - Chrome debug launcher
- `run_app.ps1` - PowerShell launcher
- `Run-Tool.bat` - Batch launcher
- `chromedriver.exe` - Chrome WebDriver

## 🚀 PowerShell Script để cleanup tự động

Tạo file `cleanup.ps1`:

```powershell
# Repository Cleanup Script
Write-Host "🧹 Dọn dẹp repository..." -ForegroundColor Yellow

# Xóa build artifacts
if (Test-Path ".\build\") {
    Remove-Item -Recurse -Force ".\build\"
    Write-Host "✅ Đã xóa thư mục build" -ForegroundColor Green
}

# Xóa executables cũ
$exeFiles = @(
    ".\J&T Express Tool v2.0.exe",
    ".\Phat-Sot-V1.1.exe"
)

foreach ($file in $exeFiles) {
    if (Test-Path $file) {
        Remove-Item -Force $file
        Write-Host "✅ Đã xóa $(Split-Path $file -Leaf)" -ForegroundColor Green
    }
}

# Xóa spec files cũ
$specFiles = @(
    ".\fetch_phone_tool.spec",
    ".\Phat-Sot-V1.1.spec"
)

foreach ($file in $specFiles) {
    if (Test-Path $file) {
        Remove-Item -Force $file
        Write-Host "✅ Đã xóa $(Split-Path $file -Leaf)" -ForegroundColor Green
    }
}

# Xóa archive files
$archiveFiles = @(
    ".\J&T-Express-Tool-v2.0-Release.zip",
    ".\Phat-Sot-v1.1.rar",
    ".\Phat-Sot-v1.1.zip", 
    ".\Phat-Sot-V1.rar"
)

foreach ($file in $archiveFiles) {
    if (Test-Path $file) {
        Remove-Item -Force $file
        Write-Host "✅ Đã xóa $(Split-Path $file -Leaf)" -ForegroundColor Green
    }
}

Write-Host "🎉 Cleanup hoàn thành!" -ForegroundColor Cyan
Write-Host "📁 Repository hiện tại chỉ còn lại các file cần thiết" -ForegroundColor Cyan
```

## 📋 Checklist sau khi cleanup

- [ ] Kiểm tra `git status` để xem các file đã bị xóa
- [ ] Commit changes: `git add . && git commit -m "🧹 Clean up redundant files and improve documentation"`
- [ ] Test build: `python main.py` để đảm bảo ứng dụng vẫn hoạt động
- [ ] Push changes: `git push origin main`

## 🏆 Lợi ích

- ⚡ Giảm size repository từ ~200MB xuống ~50MB
- 🔄 Clone/download nhanh hơn
- 📁 Cấu trúc project rõ ràng, chuyên nghiệp
- 🚀 CI/CD deploy hiệu quả hơn
- 👥 Dễ dàng onboard developer mới
