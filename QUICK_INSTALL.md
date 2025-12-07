# Quick Installation Guide

## Install Astronomical Watch on Your Computer

### Linux (Ubuntu, Debian, Fedora, etc.)

```bash
# 1. Clone or download the repository
git clone https://github.com/NndMlc/Astronomical-watch.git
cd Astronomical-watch

# 2. Run the installer (requires sudo)
sudo ./install.sh
```

After installation, launch from:
- **Application Menu**: Look for "Astronomical Watch"
- **Terminal**: Run `astronomical-watch` or `awatch`

### macOS

```bash
pip3 install .
astronomical-watch
```

### Windows

**Important**: Make sure you're inside the `Astronomical-watch` folder!

```bash
# Navigate to the project directory
cd path\to\Astronomical-watch

# Double-click install.bat
# OR run manually:
pip install .
astronomical-watch
```

Or create a desktop shortcut:
1. Right-click Desktop → New → Shortcut
2. Target: `pythonw -m astronomical_watch.ui.main`
3. Choose icon from `icons/astronomical_watch.ico`

📖 **Detailed Windows guide**: [README_WINDOWS.md](README_WINDOWS.md)

## Uninstall

```bash
# Linux/macOS
sudo pip3 uninstall astronomical-watch

# Windows
pip uninstall astronomical-watch
```

---

📖 **Full installation guide**: See [INSTALL.md](INSTALL.md)
