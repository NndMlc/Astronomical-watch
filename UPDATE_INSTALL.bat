@echo off
REM Quick update for Astronomical Watch
REM Use this to reinstall after downloading new version from GitHub

echo ================================
echo Astronomical Watch - Quick Update
================================
echo.

cd /d "%~dp0"

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo ERROR: pyproject.toml not found!
    echo.
    echo Make sure you run this script from the Astronomical-watch folder.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

echo Uninstalling old version...
pip uninstall -y astronomical-watch 2>nul

echo.
echo Installing new version...
pip install --force-reinstall .

if errorlevel 1 (
    echo.
    echo ================================
    echo ERROR: Update failed
    echo ================================
    echo.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================
echo Update complete!
echo ================================
echo.
echo The desktop shortcut should still work.
echo If not, run INSTALL_EASY.bat to recreate it.
echo.
echo Press any key to test the application...
pause > nul

REM Launch the app
echo.
echo Starting Astronomical Watch...
start "" pythonw -m astronomical_watch.ui.main

echo.
echo If the application didn't start, run TEST_LAUNCH.bat to see errors.
echo.
pause
