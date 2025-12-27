# Windows Autostart Setup

## Problem

Previous autostart methods required manual steps:
- Copying files to Startup folder
- Creating shortcuts manually
- Widget not always staying visible on desktop

## Solution

### Automatic Installation

**Method 1: Using install_autostart.bat (Recommended)**

Simply double-click `install_autostart.bat` and it will:
- ✅ Check if Python is installed
- ✅ Create a silent VBScript launcher (no console window)
- ✅ Automatically create shortcut in Windows Startup folder
- ✅ Set widget to always stay on top (visible)

**Method 2: Using PowerShell Script**

Right-click `install_autostart_windows.ps1` → "Run with PowerShell"

If you get an error about execution policy:
```powershell
powershell -ExecutionPolicy Bypass -File install_autostart_windows.ps1
```

### What Gets Installed

1. **Silent Launcher** (`launch_widget_silent.vbs`)
   - Uses `pythonw.exe` instead of `python.exe` (no console window)
   - Runs in background without interrupting your work

2. **Startup Shortcut** (`%APPDATA%\...\Startup\Astronomical Watch Widget.lnk`)
   - Automatically starts when Windows boots
   - Minimized window style (doesn't interrupt login)

3. **Always On Top Setting**
   - Widget defaults to `always_on_top = False` (normal window behavior)
   - Visible on desktop, but hides behind other applications when they're open
   - Enable via: Right-click widget → "Always on top" to keep it above all windows
   - Can also toggle in Settings (Normal Mode)

## Testing

After installation, test immediately without rebooting:

```cmd
python astronomical_watch_desktop.py
```

The widget should:
- Appear on your desktop
- Stay on top of other windows
- Be draggable with left-click
- Open Normal Mode with double-click

## Removing Autostart

### Quick Method
1. Press `Win+R`
2. Type: `shell:startup`
3. Delete: `Astronomical Watch Widget.lnk`

### Complete Removal
Also delete the silent launcher:
- `launch_widget_silent.vbs` (in application directory)

## Troubleshooting

### Widget disappears behind other windows
- Right-click widget → Check "Always on top"
- Or use Settings in Normal Mode to enable it

### Console window appears at startup
- Make sure you're using the VBScript launcher, not the .bat file directly
- The installer creates `launch_widget_silent.vbs` which uses `pythonw.exe`

### Widget doesn't start at boot
- Verify shortcut exists: `Win+R` → `shell:startup`
- Check Python is in system PATH: `python --version`
- Try running manually first to confirm it works

### Python not found error
- Install Python from https://python.org
- During installation, check "Add Python to PATH"
- Restart your computer after Python installation

## Advanced: Manual Installation

If automatic scripts don't work:

1. Create `launch_widget_silent.vbs`:
   ```vbscript
   Set WshShell = CreateObject("WScript.Shell")
   WshShell.CurrentDirectory = "C:\path\to\Astronomical-watch"
   WshShell.Run "pythonw.exe astronomical_watch_desktop.py", 0, False
   ```

2. Create shortcut to the `.vbs` file

3. Move shortcut to: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

## Technical Details

### Why VBScript?
- `.bat` files show console window (annoying at startup)
- VBScript can run programs silently (no window flash)
- `pythonw.exe` is Python without console (double protection)

### Why Not Task Scheduler?
- More complex for users
- VBScript method is simpler and equally reliable
- Startup folder is the Windows-recommended approach

### Widget Visibility
- Changed default: `self._always_on_top = False` (normal window behavior)
- Widget visible on desktop but hides behind active applications
- Enable "Always on top" via right-click menu or Settings to keep it above all windows
- Can still be toggled on/off at any time

## See Also

- `AUTOSTART_WINDOWS.bat` - Old instructions (deprecated)
- `startup_widget.bat` - Simple launcher (shows console)
- `setup_autostart_linux.sh` - Linux autostart setup
