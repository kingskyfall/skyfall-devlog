Write-Host ""
Write-Host "========== Skyfall Sync ==========" -ForegroundColor Cyan

Set-Location "$PSScriptRoot\.."

git add .

$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

git commit -m "Auto update $time"

git push

Write-Host ""
Write-Host "Done! Website will update in about a minute." -ForegroundColor Green
Pause