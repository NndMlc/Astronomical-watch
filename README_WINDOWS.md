# Astronomical Watch - Windows Guide

Simple installation for Windows users.

---

## Requirements

- **Windows 10/11** (or 7/8 with updates)
- **Python 3.11+** from [python.org](https://www.python.org/downloads/)
  - ⚠️ Check **"Add Python to PATH"** during installation!

---

## Installation

### 1. Download

From GitHub: https://github.com/NndMlc/Astronomical-watch
- Click green **"Code"** button → **"Download ZIP"**
- Extract to a folder (e.g., `Downloads\Astronomical-watch`)

### 2. Install

Double-click: **`install.bat`**

The installer will:
- ✓ Check Python installation
- ✓ Install the package
- ✓ Create desktop shortcut with icon
- ✓ Verify everything works

If your Desktop folder is in a custom location, the installer will ask for the path.

### 3. Run

**Double-click "Astronomical Watch" icon on your Desktop!**

---

## Using the Application

### Widget Mode (Default)
Small floating display showing astronomical time (DDD.mmm format).

- **Double-click widget** → Open full interface
- **Right-click widget** → Menu
- **Drag widget** → Reposition

### Full Interface
Tabs for:
- **Current Time** - Live display
- **Explanation** - System guide (28 languages)
- **Comparison** - Time conversion
- **Settings** - Customize behavior

---

## 🚀 Auto-Start with Windows

Want the widget to appear automatically when Windows boots?

**Simply double-click: `install_autostart.bat`**

This will:
- ✅ Create silent launcher (no console window)
- ✅ Add shortcut to Windows Startup folder
- ✅ Widget starts automatically when you log in
- ✅ Widget visible on desktop (hides behind active windows)
- 💡 Enable "Always on top" via right-click if you want it above all windows

**To remove autostart:**
1. Press `Win+R`
2. Type: `shell:startup`
3. Delete: `Astronomical Watch Widget.lnk`

For more details, see [WINDOWS_AUTOSTART_GUIDE.md](WINDOWS_AUTOSTART_GUIDE.md)

---

## Uninstall

Double-click: **`uninstall.bat`**

---

## Troubleshooting

### "Python not found"
**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. During install, check **"Add Python to PATH"**
3. Restart Command Prompt
4. Run `install.bat` again

### "pip not found"
**Solution:**
- Reinstall Python (pip is included by default)

### "Desktop shortcut not created"
**Solution:**
1. When `install.bat` asks, enter your Desktop path:
   - Open File Explorer
   - Right-click "Desktop" in sidebar → Properties
   - Look at "Location" tab for full path
   - Example: `C:\Users\YourName\Desktop`
2. Or run from Command Prompt: `astronomical-watch`

### "Application doesn't start from shortcut"
**Solution:**
- Open Command Prompt: `astronomical-watch`
- This shows any error messages
- Most common: tkinter missing (reinstall Python with all components)

### "tkinter not available"
**Solution:**
1. Control Panel → Programs → Uninstall Python
2. Reinstall Python
3. Choose "Customize installation"
4. Check "tcl/tk and IDLE"
5. Complete installation
6. Run `install.bat` again

### "Application closes when I close Command Prompt"
**Fix:**
- Use the **desktop shortcut** instead
- The shortcut uses `pythonw.exe` which runs without a console window
- If running from Command Prompt, the app is tied to that terminal

---

## Manual Installation (Alternative)

If `install.bat` doesn't work:

1. Open Command Prompt (`Win + R`, type `cmd`)
2. Navigate to folder:
   ```cmd
   cd C:\Path\To\Astronomical-watch
   ```
3. Install package:
   ```cmd
   pip install .
   ```
4. Run application:
   ```cmd
   astronomical-watch
   ```

To create shortcut manually:
1. Right-click Desktop → New → Shortcut
2. Enter location:
   ```
   pythonw -m astronomical_watch.ui.main
   ```
3. Name it "Astronomical Watch"
4. Right-click shortcut → Properties → Change Icon
5. Browse to: `icons\astronomical_watch.ico`

---

## Command Line Usage

After installation:

```cmd
# Launch GUI
astronomical-watch

# Show current time (text only)
awatch

# Help
astronomical-watch --help
```

---

## Updating

When new version is available:

1. Download new version from GitHub
2. Extract to same folder (overwrite old files)
3. Run `install.bat` again

The installer will upgrade automatically.

---

## Need Help?

- **GitHub Issues:** https://github.com/NndMlc/Astronomical-watch/issues
- **Documentation:** See `README.md` in project folder
- **System Info:** See `docs/ASTRO_TIME_SYSTEM.md` for technical details

---

## Quick Reference

| File | Purpose |
|------|---------|
| `install.bat` | Install application |
| `uninstall.bat` | Remove application |
| `astronomical_watch_desktop.py` | Run without installing (dev mode) |
| `astronomical_watch_widget_only.py` | Widget-only mode (dev) |

---

**Enjoy astronomical timekeeping! 🌍🌞**
