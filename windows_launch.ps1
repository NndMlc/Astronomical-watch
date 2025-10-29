# Astronomical Watch Desktop - PowerShell Launcher
# Windows PowerShell optimized launcher

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "   ASTRONOMICAL WATCH DESKTOP - POWERSHELL" -ForegroundColor Cyan  
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🌟 Launching mikroDies precision desktop widget..." -ForegroundColor Yellow
Write-Host ""

# Check Python installation
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from https://python.org/downloads/" -ForegroundColor Yellow
    Write-Host "During installation, check 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check for required files and run the best available option
if (Test-Path "windows_awatch.py") {
    Write-Host "▶️  Running Windows optimized version..." -ForegroundColor Green
    python windows_awatch.py
} elseif (Test-Path "standalone_desktop.py") {
    Write-Host "▶️  Running standalone version..." -ForegroundColor Green  
    python standalone_desktop.py
} elseif (Test-Path "desktop_app.py") {
    Write-Host "▶️  Running main desktop application..." -ForegroundColor Green
    python desktop_app.py
} else {
    Write-Host "❌ No desktop application found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Required files:" -ForegroundColor Yellow
    Write-Host "- windows_awatch.py (recommended)" -ForegroundColor White
    Write-Host "- standalone_desktop.py" -ForegroundColor White
    Write-Host "- desktop_app.py" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "👋 Desktop application closed" -ForegroundColor Yellow
Read-Host "Press Enter to exit"