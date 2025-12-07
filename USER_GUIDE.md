# Astronomical Watch - User Guide

## Installation

See [INSTALL.md](INSTALL.md) for complete installation instructions.

**Quick install on Linux:**
```bash
sudo ./install.sh
```

## Launching the Application

After installation:

- **From Menu**: Open your application launcher and search for "Astronomical Watch"
- **From Terminal**: Run `astronomical-watch` or `awatch`
- **Without Install**: Run `python3 astronomical_watch_desktop.py`

## Interface Overview

Astronomical Watch has two modes:

### 1. Widget Mode (Small Display)

- Compact floating window showing current astronomical time
- Shows **Dies** (day number since vernal equinox) and **miliDies** (fraction of the day)
- Updates every 86 milliseconds (1 mikroDies)
- Background color changes based on solar position in the sky
- Double-click to open Normal Mode

**Widget Features:**
- Drag to move anywhere on screen
- Transparent background option (Settings)
- Always on top option (Settings)
- Auto-start with system option (Settings)

### 2. Normal Mode (Full Interface)

Opens when you double-click the widget. Includes:

#### Tabs:

1. **Explanation** - Detailed explanation of the astronomical time system
   - Available in 20+ languages
   - Explains Dies, miliDies, vernal equinox, and reference meridian

2. **Comparison** - Convert between astronomical and standard time
   - Interactive calendar with Dies values for each day
   - Converter: miliDies ↔ HH:MM local time
   - Navigate months to see future/past conversions

3. **Settings** - Configure application preferences
   - Always on top toggle
   - Load on startup toggle
   - Transparent background (Windows)
   - Language selection (20+ languages)
   - Application information

## Understanding the Time Display

### Dies (DDD)
- Universal day number since this year's vernal equinox
- Same for everyone on the planet simultaneously
- Dies 0 = vernal equinox day
- Resets each year at the exact moment of vernal equinox

### miliDies (.mmm)
- Fraction of the current Dies (0-999)
- 1 miliDies = 86.4 seconds
- Represents solar movement from east to west
- Synchronized globally (no time zones)

### mikroDies
- 1/1000th of a miliDies = 0.0864 seconds
- Used internally for ultra-precise timing
- Display updates every mikroDies

### Format: DDD.mmm
Example: **285.647**
- Day 285 since vernal equinox
- 647/1000ths through the current day

## Background Colors

The interface background changes color based on the Sun's position:

- **Dark blue** → Night (Sun below horizon)
- **Orange/pink** → Dawn/dusk (twilight)
- **Light blue** → Day (Sun above horizon)

Colors are calculated using astronomical algorithms (VSOP87) for accurate solar position.

## Keyboard Shortcuts

### Comparison Card
- **Number keys**: Enter digits in converter fields
- **Numpad**: Works with both NumLock ON and OFF
- **Enter**: Convert between formats
- **Tab**: Move between fields
- **Auto-advance**: After entering 2-digit hour, focus moves to minutes

### All Windows
- **Drag title bar**: Move window
- **Close button (✕)**: Close window

## Language Support

Astronomical Watch supports 20+ languages:

- Arabic (ar)
- Bengali (bn)
- English (en)
- German (de)
- Greek (el)
- Spanish (es)
- Persian (fa)
- French (fr)
- Hausa (ha)
- Hebrew (he)
- Hindi (hi)
- Indonesian (id)
- Italian (it)
- Japanese (ja)
- Korean (ko)
- Kurdish (ku)
- Dutch (nl)
- Polish (pl)
- Portuguese (pt)
- Romanian (ro)
- Russian (ru)
- Serbian (sr)
- Vietnamese (vi)
- Zulu (zu)

Change language in Settings tab.

## Tips & Tricks

1. **Widget Transparency**: Enable in Settings for a floating overlay effect (Windows)

2. **Auto-start**: Enable "Load on startup" in Settings to launch on system boot

3. **Always on Top**: Keep widget visible above all windows

4. **Time Conversion**: Use the Comparison card to plan events across time zones
   - Enter miliDies to see corresponding local time
   - Or enter local time to see miliDies equivalent

5. **Calendar View**: Click any date in the Comparison calendar to see its Dies value

6. **Multi-language**: Switch languages anytime - all text updates instantly

## Troubleshooting

### Widget doesn't appear
- Check if it's minimized to system tray
- Try restarting: `pkill -f astronomical_watch && astronomical-watch`

### Colors not updating
- Widget updates theme every 86ms automatically
- If stuck, close and reopen Normal Mode

### Can't enter numbers in Comparison card
- Click on the input field first to activate it
- Both regular numbers and numpad work

### Settings not saving
- Check file permissions in `~/.config/astronomical_watch/`
- Settings saved to `settings.json`

### Window off-screen
- Delete settings: `rm ~/.config/astronomical_watch/settings.json`
- Restart application

## Configuration Files

Settings stored in:
- **Linux**: `~/.config/astronomical_watch/settings.json`
- **macOS**: `~/Library/Application Support/astronomical_watch/settings.json`
- **Windows**: `%APPDATA%\astronomical_watch\settings.json`

## Uninstalling

```bash
# Linux/macOS
sudo pip3 uninstall astronomical-watch

# Windows
pip uninstall astronomical-watch
```

## Support & Feedback

- **Issues**: Report bugs on GitHub
- **Documentation**: See `docs/` folder
- **Technical Details**: Read [SPEC.md](SPEC.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Learn More

- **What is Dies?**: See Explanation tab in the app
- **Astronomical Basis**: Read [docs/ASTRO_TIME_SYSTEM.md](docs/ASTRO_TIME_SYSTEM.md)
- **Equinox Calculation**: See [docs/PRECISE_EQUINOX.md](docs/PRECISE_EQUINOX.md)
- **VSOP87 System**: Read [VSOP87D_SYSTEM.md](VSOP87D_SYSTEM.md)

---

**Enjoy tracking time the astronomical way!** 🌍✨
