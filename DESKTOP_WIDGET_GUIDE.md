# Desktop Widget Installation Guide

## Astronomical Watch Desktop Widget

Desktop aplikacija sa widget/normal mode funkcionalnostima.

### Quick Start

#### Windows:
1. Dupli klik na `desktop_launcher.bat`
2. Aplikacija se otvara u widget mode u gornjem desnom uglu
3. Dupli klik na widget → otvara normal mode
4. U normal mode: "Minimize to Widget" dugme → vraća u widget mode

#### Linux:
1. Terminal: `./desktop_launcher.sh`
2. Ili direktno: `python3 desktop_widget_app.py`

### Features

#### Widget Mode:
- **Pozicija**: Gornji desni ugao ekrana
- **Always on Top**: Da, uvek vidljiv
- **Sadržaj**:
  - Naslov "Astronomical Watch" (mali font)
  - Dies.miliDies brojevi (veliki font)
  - Label "Dies . miliDies" (srednji font)  
  - Progress bar za mikroDies (0-1000)
- **Interakcija**: Dupli klik → Normal Mode

#### Normal Mode:
- **Full aplikacija** sa svim podacima
- **Tabbed interface**: Current, Solar, About
- **"Minimize to Widget"** dugme → vraća u Widget Mode
- **Real-time updates** svakih 100ms

### Technical Details

#### Core Integration:
- **Primary**: `AstroYear` astronomical core
- **Fallback**: Embedded calculator (za dev/testing)
- **Updates**: Real-time svakih 100ms
- **Precision**: VSOP87 calculations

#### UI Architecture:
```python
AstronomicalWatchApp
├── WidgetMode (minimal corner display)
└── NormalMode (full tabbed interface)
```

#### System Requirements:
- **Python**: 3.8+
- **GUI**: tkinter (usually included)
- **OS**: Windows 10+, Linux desktop environments

### Files Structure:

```
desktop_widget_app.py     # Main widget+normal mode app
desktop_launcher.bat      # Windows launcher with fallbacks  
desktop_launcher.sh       # Linux launcher with fallbacks
awatch_ultimate.py        # Fallback GUI/console app
instant_awatch.py         # Minimal console fallback
```

### Troubleshooting:

#### No GUI Display:
- **Container/SSH**: GUI applications need desktop environment
- **Linux**: Install desktop environment, X11, or use VNC
- **WSL**: Use WSL2 with GUI support or X server

#### tkinter Missing:
- **Ubuntu/Debian**: `sudo apt install python3-tk`
- **CentOS/RHEL**: `sudo yum install tkinter`
- **Windows**: Usually included with Python

#### Launcher Issues:
- Use direct command: `python desktop_widget_app.py`
- Check Python version: `python --version`
- Test tkinter: `python -c "import tkinter"`

### Installation Options:

#### Option 1: Direct Copy
1. Copy `desktop_widget_app.py` to target system
2. Run: `python desktop_widget_app.py`

#### Option 2: Full Package  
1. Copy entire folder to desktop
2. Use launchers: `desktop_launcher.bat` (Windows) or `./desktop_launcher.sh` (Linux)

#### Option 3: Create Executable
```bash
# Install pyinstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed desktop_widget_app.py
```

### Development:
- **Main application**: `desktop_widget_app.py` 
- **Test in container**: Limited (no GUI display)
- **Real testing**: Requires desktop system with GUI
- **Core updates**: Automatic from `src/astronomical_watch/core/`