# Windows Batch Files Guide

Quick reference for all `.bat` files in this project.

---

## Installation & Uninstallation

### `install.bat` ⭐ **START HERE**
**Complete installer for Windows**

- Checks Python and pip
- Installs package
- Creates desktop shortcut with icon
- Verifies installation
- Offers to launch application

**Usage:** Double-click to install

---

### `uninstall.bat`
**Complete uninstaller**

- Removes Python package
- Deletes desktop shortcut
- Confirms before removing

**Usage:** Double-click to uninstall

---

## Development & Testing

### `run_astronomical_watch.bat`
Launches the application **without installation** (development mode)

**Usage:** Double-click to test changes without reinstalling

---

### `startup_widget.bat`
Launches **widget-only mode** (no Normal Mode window)

**Usage:** For autostart or minimal display

---

### `AUTOSTART_WINDOWS.bat`
Adds Astronomical Watch to Windows startup

**Usage:** Run once to start widget automatically when Windows boots

---

## File Summary

| File | Purpose | When to Use |
|------|---------|-------------|
| `install.bat` | Install application | First time setup |
| `uninstall.bat` | Remove application | When uninstalling |
| `run_astronomical_watch.bat` | Run without install | Development/testing |
| `startup_widget.bat` | Widget-only mode | Minimal display |
| `AUTOSTART_WINDOWS.bat` | Add to startup | Auto-launch on boot |

---

## Installation Flow

```
1. Download ZIP from GitHub
2. Extract folder
3. Double-click: install.bat
4. Follow prompts
5. Launch from Desktop shortcut
```

---

## Need Help?

See **[README_WINDOWS.md](README_WINDOWS.md)** for:
- Detailed installation guide
- Troubleshooting
- Manual installation steps
- Common errors and fixes

---

**Tip:** Always run `install.bat` from the `Astronomical-watch` folder where `pyproject.toml` is located!
