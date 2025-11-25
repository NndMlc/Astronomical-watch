REM Instructions for Windows Autostart Setup
REM ==========================================

REM Method 1: Startup Folder
REM 1. Press Win+R, type: shell:startup
REM 2. Copy startup_widget.bat to the opened folder
REM 3. Widget will auto-start with Windows

REM Method 2: Task Scheduler
REM 1. Open Task Scheduler (taskschd.msc)
REM 2. Create Basic Task
REM 3. Name: "Astronomical Watch Widget"
REM 4. Trigger: "When I log on"
REM 5. Action: "Start a program"
REM 6. Program: Path to startup_widget.bat
REM 7. Click Finish

REM Method 3: Registry (Advanced)
REM Add registry entry to:
REM HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
REM Name: AstronomicalWidget
REM Value: "C:\path\to\startup_widget.bat"

echo To enable autostart:
echo 1. Copy startup_widget.bat to Windows Startup folder
echo 2. Press Win+R and type: shell:startup
echo 3. Paste the .bat file there
echo 4. Widget will start automatically with Windows
pause