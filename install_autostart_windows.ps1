# Astronomical Watch - Windows Autostart Installer
# Automatically installs widget to Windows Startup folder

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " ASTRONOMICAL WATCH AUTOSTART INSTALLER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get current directory (where the script is located)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Get Windows Startup folder
$startupFolder = [System.Environment]::GetFolderPath('Startup')
Write-Host "Startup folder: $startupFolder" -ForegroundColor Yellow
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.6+ from https://python.org" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if astronomical_watch_widget_only.py exists
$widgetScript = Join-Path $scriptDir "astronomical_watch_widget_only.py"
if (-not (Test-Path $widgetScript)) {
    Write-Host "✗ Error: Widget script not found!" -ForegroundColor Red
    Write-Host "  Expected: $widgetScript" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Widget script found" -ForegroundColor Green
Write-Host ""

# Create VBScript launcher (silent, no console window)
$vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "$scriptDir"
WshShell.Run "pythonw.exe astronomical_watch_widget_only.py", 0, False
Set WshShell = Nothing
"@

$vbsPath = Join-Path $scriptDir "launch_widget_silent.vbs"
$vbsContent | Out-File -FilePath $vbsPath -Encoding ASCII -Force

Write-Host "✓ Created silent launcher: launch_widget_silent.vbs" -ForegroundColor Green

# Create shortcut in Startup folder
$shortcutPath = Join-Path $startupFolder "Astronomical Watch Widget.lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $vbsPath
$shortcut.WorkingDirectory = $scriptDir
$shortcut.Description = "Astronomical Watch Widget - Universal Time Display"
$shortcut.WindowStyle = 7  # Minimized

# Try to set icon if available
$iconPath = Join-Path $scriptDir "icons\astronomical_watch.ico"
if (Test-Path $iconPath) {
    $shortcut.IconLocation = $iconPath
    Write-Host "✓ Icon set: $iconPath" -ForegroundColor Green
}

$shortcut.Save()

Write-Host "✓ Shortcut created in Startup folder" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  INSTALLATION SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "The Astronomical Watch widget will now:" -ForegroundColor Cyan
Write-Host "  • Start automatically when Windows boots" -ForegroundColor White
Write-Host "  • Run silently in the background (no console)" -ForegroundColor White
Write-Host "  • Stay always on top (visible on desktop)" -ForegroundColor White
Write-Host ""
Write-Host "To test now, run:" -ForegroundColor Yellow
Write-Host "  python astronomical_watch_widget_only.py" -ForegroundColor White
Write-Host ""
Write-Host "To remove autostart:" -ForegroundColor Yellow
Write-Host "  1. Press Win+R" -ForegroundColor White
Write-Host "  2. Type: shell:startup" -ForegroundColor White
Write-Host "  3. Delete 'Astronomical Watch Widget.lnk'" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
