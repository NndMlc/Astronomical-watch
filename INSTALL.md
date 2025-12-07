# Astronomical Watch - Installation Guide

## Requirements

- **Python**: 3.11 or newer
- **pip3**: Python package installer
- **Operating System**: Linux, macOS, or Windows
- **Tkinter**: Usually comes with Python (for GUI)

## Linux Installation

### Quick Install (Recommended)

```bash
# Clone or download the repository
git clone https://github.com/NndMlc/Astronomical-watch.git
cd Astronomical-watch

# Run the installation script
sudo ./install.sh
```

This will:
- Install the Python package system-wide
- Create a desktop entry in your application menu
- Install the application icon
- Add `astronomical-watch` and `awatch` commands to your PATH

### Manual Installation

```bash
# Install using pip
sudo pip3 install .

# Or install in development mode
pip3 install -e .
```

### Running the Application

After installation, you can launch Astronomical Watch in several ways:

1. **From Application Menu**: Look for "Astronomical Watch" in your applications
2. **From Terminal**: 
   ```bash
   astronomical-watch
   # or
   awatch
   ```

## macOS Installation

```bash
# Install using pip
pip3 install .

# Run the application
astronomical-watch
```

**Note**: You may need to install Python 3.11+ from [python.org](https://www.python.org/downloads/) if not already installed.

## Windows Installation

### Using the Installation Script

1. **Download or clone the repository**:
   ```bash
   # Using Git
   git clone https://github.com/NndMlc/Astronomical-watch.git
   
   # Or download ZIP and extract it
   ```

2. **Open the folder** in File Explorer

3. **Double-click `install.bat`**
   - This will install the package using pip
   - Make sure you run it from inside the `Astronomical-watch` folder

4. **Run the application**:
   - Open Command Prompt or PowerShell
   - Type: `astronomical-watch`

### Manual Installation Using pip

```bash
# Navigate to the project directory
cd path\to\Astronomical-watch

# Install using pip
pip install .

# Run the application
astronomical-watch
```

**Important**: Make sure to run the commands from inside the `Astronomical-watch` directory where `pyproject.toml` is located.

### Creating a Shortcut

1. Right-click on Desktop → New → Shortcut
2. Enter location: `pythonw -m astronomical_watch.ui.main`
3. Name it "Astronomical Watch"
4. Optional: Set icon from `icons/astronomical_watch.ico`

## Development Installation

For development work with live code updates:

```bash
pip3 install -e .
pip3 install -e ".[dev]"  # Includes pytest, mypy, ruff
```

## Uninstallation

### Linux/macOS

```bash
# Remove the package
sudo pip3 uninstall astronomical-watch

# Remove desktop entry (Linux only)
sudo rm /usr/share/applications/astronomical-watch.desktop
sudo rm /usr/share/pixmaps/astronomical-watch.png
sudo update-desktop-database /usr/share/applications/
```

### Windows

```bash
pip uninstall astronomical-watch
```

## Troubleshooting

### "python3: command not found"
- Install Python 3.11 or newer from your package manager or [python.org](https://www.python.org)

### "tkinter not found" / GUI doesn't start
- **Ubuntu/Debian**: `sudo apt install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Tkinter should be included with Python from python.org
- **Windows**: Tkinter is included by default

### Permission errors
- Use `sudo` for system-wide installation on Linux/macOS
- Run Command Prompt as Administrator on Windows

### Icon not showing
- Make sure `icons/astronomical_watch.png` exists
- On Linux, run: `sudo update-icon-caches /usr/share/icons/*`

## Autostart Configuration

### Linux

The application includes `setup_autostart_linux.sh`:

```bash
./setup_autostart_linux.sh
```

This creates `~/.config/autostart/astronomical-watch.desktop` to start the widget on login.

### Windows

Run `AUTOSTART_WINDOWS.bat` to add the application to Windows startup.

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
