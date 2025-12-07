# Astronomical Watch - Windows Installation Guide

## Quick Start for Windows Users

### Step 1: Download the Project

**Option A: Using Git**
```cmd
git clone https://github.com/NndMlc/Astronomical-watch.git
cd Astronomical-watch
```

**Option B: Download ZIP**
1. Go to https://github.com/NndMlc/Astronomical-watch
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder (e.g., `C:\Users\YourName\Downloads\Astronomical-watch`)

### Step 2: Install Python (if not already installed)

1. Download Python 3.11 or newer from https://www.python.org/downloads/
2. **Important**: During installation, check "Add Python to PATH"
3. Click "Install Now"

### Step 3: Install Astronomical Watch

**Method 1: Easy Install with Desktop Shortcut (RECOMMENDED)**

1. Open File Explorer
2. Navigate to the `Astronomical-watch` folder
3. Double-click **`INSTALL_EASY.bat`** (or **`install.ps1`** if you prefer PowerShell)
4. Follow the on-screen instructions
5. When asked, press Y to launch the application

✅ This will automatically:
- Install the Python package
- Create a desktop shortcut with icon
- Ask if you want to launch it immediately

**Method 2: Using the Original Installer**

1. Open File Explorer
2. Navigate to the `Astronomical-watch` folder
3. Double-click `install.bat`
4. This now also creates a desktop shortcut automatically

**Method 3: Using Command Prompt (Manual)**

1. Open Command Prompt (press `Win + R`, type `cmd`, press Enter)
2. Navigate to the project folder:
   ```cmd
   cd C:\Users\YourName\Downloads\Astronomical-watch
   ```
3. Install:
   ```cmd
   pip install .
   ```

**Method 4: Using PowerShell (Advanced)**

```powershell
cd C:\Users\YourName\Downloads\Astronomical-watch
powershell -ExecutionPolicy Bypass -File install.ps1
```

### Step 4: Run the Application

**The shortcut was created automatically!**

Just double-click **"Astronomical Watch"** on your Desktop!

**Other options:**

**Option A: Test if it works (shows errors if any)**
- Double-click `TEST_LAUNCH.bat` in the project folder
- This will show any error messages in a console window

**Option B: From Command Prompt**
```cmd
astronomical-watch
```

**Option C: From Start Menu**
1. Press the Windows key
2. Type: `astronomical-watch`
3. Press Enter

**If the desktop shortcut doesn't work:**
1. Right-click the shortcut → Properties
2. Check "Target" field - should be: `pythonw.exe -m astronomical_watch.ui.main`
3. Or use `TEST_LAUNCH.bat` to see error messages

## Troubleshooting

### Desktop shortcut created but nothing happens when I double-click it

**Quick diagnosis:**
1. Double-click `TEST_LAUNCH.bat` - this will show error messages
2. Check if the package is installed: `pip list | findstr astronomical`
3. Test if Python/tkinter works: `python -m tkinter`

**Common causes:**

1. **Package not installed correctly**
   - Solution: Run `install.bat` or `INSTALL_EASY.bat` again
   - Verify: `pip show astronomical-watch`

2. **Python not in PATH**
   - The shortcut uses `pythonw.exe` which might not be found
   - Solution: Edit shortcut, use full path to pythonw.exe
   - Example: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\pythonw.exe`

3. **Tkinter missing**
   - Test: Open Command Prompt and run `python -m tkinter`
   - If error: Reinstall Python and make sure "tcl/tk and IDLE" is checked during installation

4. **Working directory wrong**
   - Right-click shortcut → Properties → "Start in" should be empty or project folder

**Fix the shortcut manually:**
1. Right-click "Astronomical Watch" shortcut → Properties
2. Target should be: `pythonw -m astronomical_watch.ui.main`
3. Or full path: `C:\Path\To\pythonw.exe -m astronomical_watch.ui.main`
4. Icon location: Browse to `icons\astronomical_watch.ico` in project folder
5. Click OK and try again
- Python is not installed or not in PATH
- Solution: Reinstall Python and check "Add Python to PATH"

### "pip is not recognized"
- pip is not installed
- Solution: Reinstall Python with pip included (default option)

### "Directory '.' is not installable"
- You're running the installer from the wrong directory
- Solution: Make sure you're in the `Astronomical-watch` folder where `pyproject.toml` is located

### "Permission denied" or "Access denied"
- Windows security or antivirus blocking installation
- Solution: Run Command Prompt as Administrator:
  1. Search for "cmd" in Start Menu
  2. Right-click "Command Prompt"
  3. Select "Run as administrator"
  4. Navigate to the project folder and run `pip install .`

### Application doesn't start
1. Check Python version: `python --version` (should be 3.11 or newer)
2. Try running with error output: `python -m astronomical_watch.ui.main`
3. Check if tkinter is installed: `python -m tkinter`
   - If error, reinstall Python (tkinter is included by default)

## Running Without Installation

You can run the application directly without installing:

```cmd
cd C:\Users\YourName\Downloads\Astronomical-watch
python astronomical_watch_desktop.py
```

## Autostart Configuration

To make the widget start automatically when Windows boots:

1. Press `Win + R`
2. Type: `shell:startup`
3. Press Enter (this opens the Startup folder)
4. Create a shortcut to the application:
   - Right-click in the folder → New → Shortcut
   - Location: `pythonw C:\Users\YourName\Downloads\Astronomical-watch\astronomical_watch_widget_only.py`
   - Name it "Astronomical Watch Widget"

Or double-click `AUTOSTART_WINDOWS.bat` in the project folder.

## Uninstalling

**Easy way:**
Double-click `uninstall.bat` in the project folder

**Manual way:**
```cmd
pip uninstall astronomical-watch
```

Then delete the desktop shortcut "Astronomical Watch"

## Additional Features

### Transparent Widget (Windows only)
1. Open the application
2. Double-click the widget to open Normal Mode
3. Click the "Settings" tab
4. Check "Transparent Background"
5. The widget will become semi-transparent

### Always on Top
1. Open Settings
2. Check "Always on top"
3. The widget will stay above all other windows

## Getting Help

- **Installation issues**: See [INSTALL.md](INSTALL.md)
- **Usage help**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Technical details**: See [README.md](README.md)

## System Requirements

- **OS**: Windows 10 or later (Windows 11 recommended)
- **Python**: 3.11 or newer
- **RAM**: 50 MB minimum
- **Disk Space**: 20 MB
- **Display**: Any resolution (widget is 180×110 pixels)

## Common Questions

**Q: Can I move the widget?**
A: Yes! Click and drag the widget anywhere on your screen.

**Q: How do I change the language?**
A: Double-click the widget → Settings tab → Language selector.

**Q: Does it work offline?**
A: Yes! All calculations are done locally. No internet required.

**Q: Is it free?**
A: Yes! Open source under MIT license.

**Q: Does it affect system time?**
A: No! It only displays astronomical time. Your system clock is not modified.

---

**Enjoy your astronomical timekeeping!** ⏰🌍
