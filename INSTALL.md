# Astronomical Watch - Installation Guide

Cross-platform installation instructions.

---

## Requirements

- **Python 3.11+**
- **pip** (included with Python)
- **tkinter** (usually included with Python)

---

## Windows

### Simple Installation

1. **Download** from GitHub (ZIP)
2. **Extract** the folder
3. **Double-click:** `install.bat`
4. **Launch** from Desktop shortcut

See [README_WINDOWS.md](README_WINDOWS.md) for detailed Windows guide.

**Uninstall:** Run `uninstall.bat`

---

## Linux

### Quick Install

```bash
git clone https://github.com/NndMlc/Astronomical-watch.git
cd Astronomical-watch
sudo ./install.sh
```

This installs:
- Python package (system-wide)
- Desktop entry (application menu)
- Commands: `astronomical-watch`, `awatch`

### Launch

- **Application Menu:** "Astronomical Watch"
- **Terminal:** `astronomical-watch`


---

## macOS

```bash
pip3 install .
astronomical-watch
```

**Note:** Requires Python 3.11+ from [python.org](https://www.python.org/downloads/)

---

## Manual Installation (All Platforms)

```bash
cd Astronomical-watch
pip install .
astronomical-watch
```

**Uninstall:** `pip uninstall astronomical-watch`

---

## Development Installation

For live code updates:

```bash
pip install -e .
pip install -e ".[dev]"  # Includes pytest, mypy, ruff
```

---

## Verification

After installation:

```bash
# Check installation
pip show astronomical-watch

# Test CLI
awatch

# Launch GUI
astronomical-watch
```

---

## Troubleshooting

### "Python not found"
- Install Python 3.11+ from [python.org](https://www.python.org/downloads/)
- Make sure "Add to PATH" is checked during installation

### "tkinter not available"
**Linux:**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**Windows/macOS:** Reinstall Python (tkinter included)

### "Command not found: astronomical-watch"
- Installation might not have added to PATH
- Try: `python -m astronomical_watch.ui.main`
- Or reinstall with pip

### "Module not found: src"
- Update to latest version (import bug fixed)
- Run: `pip install --upgrade --force-reinstall .`

---

## Quick Start After Installation

1. **Launch:** `astronomical-watch`
2. **Widget appears** (small floating display)
3. **Double-click widget** → Full interface
4. **Explore tabs:** Current Time, Explanation, Comparison, Settings

---


---

For platform-specific details:
- **Windows users:** See [README_WINDOWS.md](README_WINDOWS.md)
- **Technical info:** See [docs/ASTRO_TIME_SYSTEM.md](docs/ASTRO_TIME_SYSTEM.md)

## Running Without Installation

You can also run directly from the repository:

```bash
python3 astronomical_watch_desktop.py
```

Or just the widget:

```bash
python3 astronomical_watch_widget_only.py
```

## Additional Resources

- **README.md**: Project overview and features
- **SPEC.md**: Technical specification
- **CONTRIBUTING.md**: How to contribute
- **docs/**: Additional documentation

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation in `docs/`
