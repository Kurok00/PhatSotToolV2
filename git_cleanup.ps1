# Git Repository Cleanup Script
# Xóa các file dư thừa khỏi Git repository

Write-Host "🧹 Cleanup Git Repository..." -ForegroundColor Yellow

# Xóa toàn bộ thư mục build khỏi Git
Write-Host "🗑️ Xóa thư mục build/ khỏi Git..." -ForegroundColor Cyan
git rm -r build/

# Xóa các file archive cũ
Write-Host "🗑️ Xóa các file archive cũ..." -ForegroundColor Cyan
git rm "Phat-Sot-V1.1.spec"
git rm "Phat-Sot-V1.rar" 
git rm "Phat-Sot-v1.1.rar"
git rm "Phat-Sot-v1.1.zip"

# Xóa file spec cũ
Write-Host "🗑️ Xóa file spec cũ..." -ForegroundColor Cyan
git rm "fetch_phone_tool.spec"

# Xóa file batch cũ (đã có Run-Tool.bat thay thế)
Write-Host "🗑️ Xóa Tool.bat cũ..." -ForegroundColor Cyan
git rm "Tool.bat"

# Xóa logo cũ (đã có Logo_JT.ico)
Write-Host "🗑️ Xóa logo cũ..." -ForegroundColor Cyan
git rm "Logo_J&T.jpg"

Write-Host ""
Write-Host "✅ Đã xóa các file dư thừa khỏi Git!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Bước tiếp theo:" -ForegroundColor Yellow
Write-Host "1. git add . (add các file mới: requirements.txt, SETUP.md, etc.)" -ForegroundColor White
Write-Host "2. git commit -m '🧹 Clean up repository: remove build artifacts and redundant files'" -ForegroundColor White  
Write-Host "3. git push origin main" -ForegroundColor White
