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
Write-Host ""
Write-Host "📋 Bước tiếp theo:" -ForegroundColor Yellow
Write-Host "1. git add ." -ForegroundColor White
Write-Host "2. git commit -m `"🧹 Clean up redundant files and improve documentation`"" -ForegroundColor White
Write-Host "3. git push origin main" -ForegroundColor White
