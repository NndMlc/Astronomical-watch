# Astronomical Watch - AI Coding Agent Instructions

## Project Overview
Astronomical Watch implements an experimental timekeeping system based on astronomical phenomena rather than conventional calendars. The core represents time as `DDD.mmm` where `DDD` is "Dies" (universal days since vernal equinox) and `mmm` is "miliDies" (thousandths of a Dies).

## Core Architecture

### 1. Dual-Licensed Codebase Structure
- **Core algorithms** (`src/astronomical_watch/core/`): Under restrictive Astronomical Watch Core License
- **Everything else**: MIT licensed (CLI, UI, web, tests)
- When modifying core algorithms, preserve immutable interface contracts

### 2. Time System Fundamentals
- **Reference meridian**: 168°58'30"W (between Diomede Islands) 
- **Day boundary**: Mean solar noon at reference meridian = 00:44:06 UTC
- **Year boundary**: Exact vernal equinox instants (not calendar years)
- **Day subdivision**: 1000 miliDies (86.4 seconds each)
- **mikroDies extension**: 1/1000th of miliDies (0.0864 seconds) for ultra-precise timing
- **Dies**: Universal day unit, same for everyone regardless of location
- **miliDies**: 1/1000th of a Dies (one thousandth of universal day)

### 3. Key Components

#### AstroYear Class (`core/astro_time_core.py`)
```python
# Represents one astronomical year between equinox instants
ay = AstroYear(current_equinox, next_equinox)
reading = ay.reading(datetime_utc)  # -> AstroReading(dies, miliDies, mikroDies)
```

#### VSOP87D Dynamic Precision System
```python
# Configurable astronomical precision
lon = solar_longitude_from_datetime(dt, max_error_arcsec=1.0)  # High precision
lon = solar_longitude_from_datetime(dt)  # Default precision
```

## Application Entry Points

### Desktop Applications (Root Directory)
- **`astronomical_watch_desktop.py`**: Main desktop app with widget+normal mode
- **`astronomical_watch_widget_only.py`**: Widget-only borderless display
- **`main.py`**: Alternative entry point for full desktop experience

### CLI Tools
- **`cli/awatch.py`**: Simple CLI printing DDD.mmm format
- **Package entry points** in `pyproject.toml`:
  - `astronomical-watch`: Desktop GUI via `astronomical_watch.ui.main:main`
  - `awatch`: Alternative CLI entry point (same target)

### Launch Scripts
- **Linux**: `run_astronomical_watch.sh`, `startup_widget.sh`, `setup_autostart_linux.sh`
- **Windows**: `run_astronomical_watch.bat`, `startup_widget.bat`, `install_autostart.bat` (automatic installer)
  - `install_autostart_windows.ps1` - PowerShell version with full automation
  - `WINDOWS_AUTOSTART_GUIDE.md` - Complete Windows autostart documentation

## Development Patterns

### Testing Philosophy
- Tests use `AstroYear` directly rather than mocking astronomical calculations
- Precision tests compare different accuracy levels (see `test_vsop87d_system.py`)
- UI tests marked with `@pytest.mark.ui` (require display)
- Test data includes reference ephemeris in `tests/data/equinox_reference.json`

### Module Organization
```
core/          # Time calculations, equinox solving, VSOP87 coefficients
ui/            # Tkinter widgets with sky-based gradients (widget.py, normal_mode.py)
solar/         # Lightweight solar position algorithms  
net/           # Network services for equinox data and NTP time sync
offline/       # Caching and offline operation
routes/        # Web API routes
services/      # Business logic services
scripts/       # VSOP87 coefficient generation tools
translate/     # Multilingual explanation cards (20+ languages)
```

### Configuration Management
- Use `pyproject.toml` for all package configuration
- CLI entry points use `astronomical_watch.ui.main:main` (desktop GUI)
- Optional dependencies in `[project.optional-dependencies]`
- Test markers: `ui: tests requiring a display / tkinter`

### UI Architecture Pattern
```python
# All UI components use gradient.py for sky-themed backgrounds
from .gradient import calculate_sky_gradient
from .widget import create_widget
from .normal_mode import create_normal_mode

# Theme calculation based on solar altitude from VSOP87 data
# Widget mode: 180x110 borderless always-on display
# Normal mode: Full tabbed interface with explanations
```

### Dynamic Coefficient Loading
The system loads VSOP87 coefficients on-demand based on precision requirements:
```python
# Trigger coefficient file search/loading in scripts/vsop87_coefficients/
coeffs = _get_coefficients(max_error_arcsec)
# Generated files follow pattern: vsop87_*.py
```

## Critical Development Workflows

### Running the Application
```bash
# Desktop application
python astronomical_watch_desktop.py

# Widget only (borderless overlay)
python astronomical_watch_widget_only.py

# CLI current time
python cli/awatch.py
```

### Testing with Different UI Modes
```bash
# All tests
python -m pytest

# Skip UI tests (no display required)
python -m pytest -m "not ui"

# Test specific precision systems
python -m pytest tests/test_vsop87d_system.py -v
```

### Adding New Astronomical Algorithms
1. Implement in `core/` with frozen interface constants
2. Add precision parameter: `max_error_arcsec: Optional[float] = None`
3. Test against published ephemeris data (NASA/USNO)
4. Update VSOP87D integration if needed

### UI Development
- All UI components use `gradient.py` for sky-themed backgrounds
- Theme calculation based on solar altitude from VSOP87 data
- Widget supports drag-and-drop repositioning with double-click to open normal mode
- Widget defaults to `always_on_top = False` for normal window behavior (user can enable via right-click menu)
- Language support via `translate/` modules (20+ languages)

### Generating VSOP87 Coefficient Files
```bash
cd src/astronomical_watch/scripts/
python generate_vsop87.py --auto-upgrade --target-arcsec 1.0
```

## Integration Points

### Equinox Calculation Chain
`solar.py` → `vsop87_earth.py` → `timebase.py` → `equinox.py` → `astro_time_core.py`

### UI Data Flow
`AstroYear.reading()` → `gradient.py` (solar altitude) → `widget.py`/`normal_mode.py`

### Desktop Application Architecture
```python
# Main app coordinates Widget and Normal Mode windows
app = AstronomicalWatchApp()
app.show_widget()  # Borderless floating display
# Double-click widget opens Normal Mode with full interface
```

## Project-Specific Conventions

### Time Handling
- All internal calculations use UTC datetime objects with timezone awareness
- Julian Day calculations use Terrestrial Time (TT) for astronomical precision
- ΔT conversion handled in `timebase.py`
- Constants defined in `astro_time_core.py` with frozen interface
- **NTP time synchronization** (`net/time_sync.py`) for maximum precision:
  - Automatic sync every 60 minutes when enabled
  - Typical accuracy: ±5-50ms
  - Graceful fallback to system time if network unavailable
  - Use `_get_current_utc_time()` in UI code for NTP-aware time

### Error Propagation
- VSOP87 errors specified in arcseconds, automatically converted to radians
- Conservative error bounds computed for truncated coefficient series
- Fallback to default coefficients if high-precision files unavailable

### Multilingual Support
- Translation cards in `translate/` directory for 20+ languages
- Naming pattern: `explanation_{language_code}_card.py`
- Each provides localized explanations of the astronomical time system

### File Structure Patterns
- Root-level Python files are desktop application launchers
- `src/astronomical_watch/` contains the package structure
- Tests mirror the `src/` structure
- Scripts and data files in respective subdirectories

## Testing Patterns

### Core Algorithm Testing
```python
# Tests use real AstroYear calculations
ay = AstroYear(equinox_datetime)
reading = ay.reading(test_datetime)
assert reading.dies == expected_dies
assert reading.miliDies == expected_milides  # Note: attribute is miliDies (capital D)
```

**IMPORTANT**: The actual attribute name is `miliDies` (capital D). Some older tests incorrectly use `milidan` or `milidies` - these are bugs and should be fixed. Similarly, constants are `MILIDES_PER_DAY` and `SECONDS_PER_MILIDES`, not "MILLIDAN".

### UI Testing Requirements
- Mark UI tests with `@pytest.mark.ui`
- UI tests require a display environment
- Test both widget and normal mode interfaces

## Common Pitfalls
- Don't modify core algorithm interfaces without license consideration
- Always pass timezone-aware UTC datetimes to core functions
- VSOP87 time parameter is millennia since J2000, not centuries
- Day boundaries at 00:44:06 UTC, not midnight
- Equinox resets dies to 0 even if mid-Dies
- **Attribute naming**: Use `miliDies` (capital D), not `milidan` or `milidies`
- **Constant naming**: Use `MILIDES_PER_DAY` and `SECONDS_PER_MILIDES`, not "MILLIDAN" variants
- Desktop launchers are in root directory, not in `src/`
- Both CLI entry points (`astronomical-watch` and `awatch`) point to the same GUI target
