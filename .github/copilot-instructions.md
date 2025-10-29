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
- **Day boundary**: Mean solar noon at reference meridian = 23:15:54 UTC  
- **Year boundary**: Exact vernal equinox instants (not calendar years)
- **Day subdivision**: 1000 miliDies (86.4 seconds each)
- **Dies**: Universal day unit, same for everyone regardless of location
- **miliDies**: 1/1000th of a Dies (one thousandth of universal day)

### 3. Key Components

#### AstroYear Class (`core/astro_time_core.py`)
```python
# Represents one astronomical year between equinox instants
ay = AstroYear(current_equinox, next_equinox)
reading = ay.reading(datetime_utc)  # -> AstroReading(day_index, milliDies)
```

#### VSOP87D Dynamic Precision System
```python
# Configurable astronomical precision
lon = solar_longitude_from_datetime(dt, max_error_arcsec=1.0)  # High precision
lon = solar_longitude_from_datetime(dt)  # Default precision
```

## Development Patterns

### Testing Philosophy
- Tests use `AstroYear` directly rather than mocking astronomical calculations
- Precision tests compare different accuracy levels (see `test_vsop87d_system.py`)
- UI tests marked with `@pytest.mark.ui` (require display)

### Module Organization
```
core/          # Time calculations, equinox solving, VSOP87 coefficients
ui/            # Tkinter widgets with sky-based gradients
web/           # FastAPI PWA with offline support  
solar/         # Lightweight solar position algorithms
scripts/       # VSOP87 coefficient generation tools
```

### Configuration Management
- Use `pyproject.toml` for all package configuration
- CLI entry point: `astronomical-watch = "core.cli:main"`
- Optional dependencies in `[project.optional-dependencies]`

### Dynamic Coefficient Loading
The system loads VSOP87 coefficients on-demand based on precision requirements:
```python
# Trigger coefficient file search/loading
coeffs = _get_coefficients(max_error_arcsec)
# Files follow pattern: scripts/vsop87_coefficients/vsop87_*.py
```

## Critical Development Workflows

### Adding New Astronomical Algorithms
1. Implement in `core/` with frozen interface constants
2. Add precision parameter: `max_error_arcsec: Optional[float] = None`
3. Test against published ephemeris data (NASA/USNO)
4. Update VSOP87D integration if needed

### UI Development  
- All UI components use `gradient.py` for sky-themed backgrounds
- Theme calculation based on solar altitude from VSOP87 data
- Widget mode: Compact always-on display
- Normal mode: Full tabbed interface

### Testing Precision
```bash
python demo_vsop87d.py  # Test different precision levels
python -m pytest tests/test_vsop87d_system.py  # VSOP87 system tests
```

### Generating Coefficient Files
```bash
cd scripts/
python generate_vsop87.py --auto-upgrade --target-arcsec 1.0
```

## Integration Points

### Equinox Calculation Chain
`solar.py` → `vsop87_earth.py` → `timebase.py` → `equinox.py` → `astro_time_core.py`

### UI Data Flow
`AstroYear.reading()` → `gradient.py` (solar altitude) → `widget.py`/`normal_mode.py`

### Web API
FastAPI serves static PWA + JSON endpoints for astronomical time data

## Project-Specific Conventions

### Time Handling
- All internal calculations use UTC datetime objects with timezone awareness
- Julian Day calculations use Terrestrial Time (TT) for astronomical precision
- ΔT conversion handled in `timebase.py`

### Error Propagation
- VSOP87 errors specified in arcseconds, automatically converted to radians
- Conservative error bounds computed for truncated coefficient series
- Fallback to default coefficients if high-precision files unavailable

### CLI Interface
```bash
awatch                           # Current time in DDD.mmm format (Dies.miliDies)
awatch --max-error-arcsec 5      # Higher precision calculations
```

## Common Pitfalls
- Don't modify core algorithm interfaces without license consideration
- Always pass timezone-aware UTC datetimes to core functions
- VSOP87 time parameter is millennia since J2000, not centuries
- Day boundaries at 23:15:54 UTC, not midnight
- Equinox resets day_index to 0 even if mid-Dies