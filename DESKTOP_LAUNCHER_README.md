# 🌌 Astronomical Watch Desktop Application

## Quick Start

### Windows:
1. Double-click `run_astronomical_watch.bat`
   
   OR
   
2. Open Command Prompt/PowerShell and run:
   ```cmd
   cd path\to\Astronomical-watch
   python astronomical_watch_desktop.py
   ```

### Linux/Mac:
1. Double-click `run_astronomical_watch.sh` (if your file manager supports it)
   
   OR
   
2. Open Terminal and run:
   ```bash
   cd /path/to/Astronomical-watch
   ./run_astronomical_watch.sh
   ```
   
   OR
   
   ```bash
   python3 astronomical_watch_desktop.py
   ```

## What You'll See:
1. **Widget Mode**: Compact 180x110 borderless overlay display showing:
   - Localized title (changes with language)
   - Dies.miliDies format in DejaVu Sans Mono font (28px, white text with black outline)
   - Separated labels: "Dies" below left number, "miliDies" below right number
   - mikroDies progress bar (YellowGreen color, 0-999, visual only)
   - Ultra-fast updates (86ms intervals)
2. **Double-click the widget** to open Normal Mode with full features
3. **Drag the widget** to move it around (no title bar to grab)
4. **Language Selection**: Choose from 20 languages (applies to both modes)
5. **Explanation Button**: Detailed explanation in your chosen language

## Requirements:
- Python 3.8+ (usually pre-installed on most systems)
- No additional packages needed (uses built-in tkinter)

## Features:
- ⏰ Real-time astronomical time display (Dies.miliDies format)
- 🌍 20-language support
- 🎨 Sky gradient themes based on solar position
- 📊 Time conversion utilities
- 🔬 Astronomical calculations
- 📚 Educational explanations

## Troubleshooting:
- **"Python is not recognized"**: Install Python from python.org
- **Double-click doesn't work**: Use command line method above
- **Display issues**: Ensure your system supports tkinter (usually default)