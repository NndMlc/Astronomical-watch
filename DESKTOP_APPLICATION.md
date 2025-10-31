# Astronomical Watch Desktop Application

## Overview
Desktop application with Widget Mode (small corner display) and Normal Mode (full window) for the Astronomical Watch timekeeping system.

## Features

### Widget Mode
- 🪟 **Small corner widget** (210x140 pixels)
- ⏰ **Live astronomical time** in Dies·miliDies format (e.g., `225·905`)
- 🎨 **Dynamic sky gradient** background that changes with solar altitude
- 🖱️ **Click to expand** to Normal Mode
- 📍 **Always on top** - stays visible while you work

### Normal Mode  
- 🖥️ **Full window display** (800x600 pixels) with detailed astronomical information
- 📊 **Progress indicators** showing completion through current Dies
- 🌍 **20-language support** including English, Serbian, Chinese, Arabic, and 16 others
- ℹ️ **Detailed explanations** of the astronomical time system
- 🎛️ **Language selector** with live switching
- 💾 **Settings persistence** - remembers your language choice

## Usage

### Quick Start
```bash
# Run the desktop application
python astronomical_watch_desktop.py
```

### Alternative Methods
```bash
# Direct module execution
python -m astronomical_watch.ui.main

# Via source directory
cd src && python -m astronomical_watch.ui.main
```

## User Interface

### Widget Mode Display
```
┌─────────────────┐
│    225·905      │  ← Current Dies·miliDies
│ Astronomical    │  
│     Time        │  ← Descriptive text
└─────────────────┘
```

### Normal Mode Features
- **Current Time Display**: Large format astronomical time
- **Progress Bar**: Visual indicator of progress through current Dies  
- **Information Panel**: Detailed explanations and system information
- **Language Menu**: Dropdown with all 20 supported languages
- **Close Button**: Graceful application shutdown

## Supported Languages
The application supports 20 languages with full translations:

| Language | Code | Native Name |
|----------|------|-------------|
| English | en | English |
| Serbian | sr | Српски |
| Spanish | es | Español |
| Chinese | zh | 中文 |
| Arabic | ar | العربية |
| Portuguese | pt | Português |
| French | fr | Français |
| German | de | Deutsch |
| Russian | ru | Русский |
| Japanese | ja | 日本語 |
| Hindi | hi | हिन्दी |
| Persian | fa | فارسی |
| Indonesian | id | Bahasa Indonesia |
| Swahili | sw | Kiswahili |
| Hausa | ha | Hausa |
| Turkish | tr | Türkçe |
| Greek | el | Ελληνικά |
| Polish | pl | Polski |
| Italian | it | Italiano |
| Dutch | nl | Nederlands |

## Technical Architecture

### Core Components
- **`astronomical_watch_desktop.py`**: Main launcher script
- **`src/astronomical_watch/ui/main.py`**: Application coordinator
- **`src/astronomical_watch/ui/widget.py`**: Widget Mode implementation  
- **`src/astronomical_watch/ui/normal_mode.py`**: Normal Mode implementation
- **`src/astronomical_watch/ui/gradient.py`**: Dynamic sky-themed backgrounds
- **`src/astronomical_watch/ui/translations.py`**: 20-language localization system

### Integration with Core System
- Uses `AstroYear` class for astronomical calculations
- Updates every second with live time readings
- Applies sky gradients based on solar altitude from VSOP87 data
- Respects the reference meridian at 168°58'30"W

## Installation Requirements

### Dependencies
```bash
# Core astronomical calculations
# (Already included in the project)

# UI Framework  
tkinter  # Usually included with Python

# Optional: For better UI appearance
python3-tk  # On some Linux distributions
```

### Platform Support
- ✅ **Linux**: Full support (tested on Ubuntu 24.04)
- ✅ **Windows**: Full support (requires Python with tkinter)
- ✅ **macOS**: Full support (requires Python with tkinter)

## Configuration

### Settings File
The application creates `astronomical_watch_settings.json` to store:
- Language preference
- Window positions (future)
- Theme preferences (future)

### Customization
- **Window Size**: Modify geometry settings in respective mode classes
- **Update Frequency**: Change timer intervals in `start_updates()` methods
- **Theme Colors**: Customize gradients in `gradient.py`

## Usage Patterns

### Workflow 1: Always-On Widget
1. Launch application → Widget appears in corner
2. Continue working with astronomical time visible
3. Click widget when you need detailed view
4. Close Normal Mode to return to widget-only

### Workflow 2: Full Information Display
1. Launch application → Widget appears
2. Immediately click widget → Normal Mode opens
3. Select preferred language from dropdown
4. Keep Normal Mode open for detailed monitoring

### Workflow 3: Quick Time Check
1. Launch application for quick time reading
2. Note current Dies·miliDies from widget
3. Close application when done

## Troubleshooting

### Common Issues

**Widget doesn't appear**:
- Check if tkinter is installed: `python -c "import tkinter"`
- Verify display is available (X11 forwarding for remote systems)

**Time shows as "ERR·000"**:
- Astronomical calculation error - check console for details
- Usually resolves automatically on next update cycle

**Language changes don't persist**:
- Check write permissions in application directory
- Settings saved to `astronomical_watch_settings.json`

**Window positioning issues**:
- Widget window can be dragged to preferred corner
- Normal Mode window can be resized and repositioned

### Debug Mode
```bash
# Run with Python error output
python astronomical_watch_desktop.py

# Check import errors
python -c "from astronomical_watch.ui import main; print('✅ Imports OK')"
```

## Future Enhancements
- 🔧 **Settings Dialog**: Comprehensive preferences management
- 📍 **Window Memory**: Remember position and size preferences  
- 🎨 **Theme Customization**: User-selectable color schemes
- 📊 **Extended Information**: More astronomical data displays
- 🔔 **Notifications**: Daily transition alerts and events
- 📱 **System Tray**: Minimize to system tray integration