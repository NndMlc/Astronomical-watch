# PowerShell Installation Script for Astronomical Watch
# Run this with: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Astronomical Watch - Installation" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check if pyproject.toml exists
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "ERROR: pyproject.toml not found!" -ForegroundColor Red
    Write-Host "Please run this script from the Astronomical-watch directory." -ForegroundColor Red
    Write-Host ""
    Write-Host "Current directory: $PWD" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✓ Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.11 or newer from https://www.python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Check if pip is available
try {
    $pipVersion = & pip --version 2>&1
    Write-Host "✓ Found pip" -ForegroundColor Green
} catch {
    Write-Host "ERROR: pip is not installed." -ForegroundColor Red
    Write-Host "Please reinstall Python with pip included." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Install the package
Write-Host "📦 Installing Astronomical Watch..." -ForegroundColor Cyan
Write-Host "Installing from: $PWD" -ForegroundColor Gray
Write-Host ""

& pip install --upgrade . 2>&1 | Out-Host

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Installation failed." -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Create desktop shortcut
Write-Host "🔗 Creating desktop shortcut..." -ForegroundColor Cyan

# Get Python executable paths
$pythonExe = (Get-Command python).Source
$pythonwExe = $pythonExe -replace "python.exe", "pythonw.exe"

# Get desktop path
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "Astronomical Watch.lnk"

# Get icon path
$iconPath = Join-Path $scriptDir "icons\astronomical_watch.ico"

# Create shortcut
$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $pythonwExe
$shortcut.Arguments = "-m astronomical_watch.ui.main"
$shortcut.WorkingDirectory = $scriptDir
$shortcut.Description = "Astronomical Watch - Astronomical Time Tracking"

if (Test-Path $iconPath) {
    $shortcut.IconLocation = $iconPath
    Write-Host "✓ Icon set to: $iconPath" -ForegroundColor Green
} else {
    Write-Host "⚠ Icon file not found, using default" -ForegroundColor Yellow
}

$shortcut.Save()

Write-Host "✓ Desktop shortcut created: $shortcutPath" -ForegroundColor Green
Write-Host ""

Write-Host "You can now:" -ForegroundColor Cyan
Write-Host "  • Double-click 'Astronomical Watch' on your Desktop" -ForegroundColor White
Write-Host "  • Or type: " -NoNewline -ForegroundColor White
Write-Host "astronomical-watch" -ForegroundColor Yellow -NoNewline
Write-Host " in Command Prompt" -ForegroundColor White
Write-Host ""
Write-Host "To uninstall:" -ForegroundColor Cyan
Write-Host "  pip uninstall astronomical-watch" -ForegroundColor White
Write-Host "  (and delete the desktop shortcut)" -ForegroundColor Gray
Write-Host ""

# Ask if user wants to launch now
$response = Read-Host "Would you like to launch Astronomical Watch now? (Y/N)"
if ($response -eq "Y" -or $response -eq "y") {
    Write-Host ""
    Write-Host "🚀 Launching Astronomical Watch..." -ForegroundColor Cyan
    Start-Process $shortcutPath
}

Write-Host ""
Write-Host "Installation finished!" -ForegroundColor Green
Read-Host "Press Enter to exit"
