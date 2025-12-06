# Astronomical Watch

Desktop application for astronomical timekeeping using Dies.miliDies format.

## Overview
Represents UTC time as `DDD.mmm` where:
- `DDD` = Dies (universal day index since vernal equinox)
- `mmm` = miliDies (thousandths of current Dies)
- Ultra-precise mikroDies subdivision (1/1000th of miliDies)

## Quick Start

### Download & Run
```bash
# Download the project
git clone https://github.com/NndMlc/Astronomical-watch.git
cd Astronomical-watch

# Run desktop application
python astronomical_watch_desktop.py
```

### What You Get
- **Widget Mode**: 180×110 borderless floating display
- **Normal Mode**: Full-featured tabbed interface with 4 cards
- **28 Languages**: Complete multilingual support (including RTL)
- **Real-time Updates**: 86ms intervals (1 mikroDies)

### Usage
- **Drag widget**: Move the floating display anywhere
- **Double-click widget**: Open Normal Mode
- **Language selector**: Choose from 28 languages
- **4 Interactive Cards**: Standard Time, Explanation, Comparison, Settings

## Features
- ⏰ **Real-time Display**: Dies.miliDies.mikroDies format
- 🌍 **28 Languages**: Full localization (en, sr, es, zh, ar, pt, fr, de, ru, ja, hi, fa, id, sw, ha, tr, el, pl, it, nl, ro, he, bn, ku, zu, vi, ko, ur)
- 🎨 **Sky Themes**: Background changes with solar position  
- 📱 **Borderless Widget**: Floating overlay without title bar
- 🔄 **Ultra-fast Updates**: Every 86ms (1 mikroDies)
- 📅 **Calendar View**: Interactive calendar with Dies display
- 🔄 **Time Converter**: Convert between standard and astronomical time
- ⚙️ **Settings Card**: Widget preferences and app information
- 📚 **Educational**: Built-in explanations in 28 languages

## Architecture

The application consists of:
- **Core astronomical calculations** (`src/astronomical_watch/core/`) - Frozen implementation
- **UI components** (`src/astronomical_watch/ui/`) - Widget and Normal Mode interfaces  
- **Translation system** (`src/astronomical_watch/translate/`) - 28 language files
- **Desktop launchers** (root directory) - Easy-to-use entry points

## Platform Support (Summary)

| Layer | Linux | macOS | Windows | Web (PWA) | Native Mobile |
|-------|-------|-------|---------|-----------|---------------|
| CLI | Yes | Yes | Yes | Via server API | Future |
| Tkinter GUI | Yes | Yes | Yes | No | Future |
| REST API | Initial | Initial | Initial | Yes (FastAPI) | Via API |
| PWA Frontend | – | – | – | Yes | Add to Home Screen |
| Native App | – | – | – | – | Evaluating |

See `README_PLATFORM_NOTES.md` for detailed roadmap and platform notes.

## Web / PWA Quick Start (Initial Version)

After adding web components (already included now):

```
pip install fastapi uvicorn
python -m web.app
# or: uvicorn web.app:app --reload
```

Open http://127.0.0.1:8000/ and “Install” / “Add to Home Screen” in supported browsers.
Offline behavior: static shell loads; live JSON data requires connectivity.

---

## English

Astronomical-watch is an experimental timekeeping system that replaces the conventional calendar/time-of-day representation with one based on recurring astronomical phenomena:

1. Year boundary: moment of the (northern) vernal equinox.
2. Day index: counted from 0 up to 365 (or 366) across the interval between two consecutive vernal equinox instants.
3. Sub‑day unit: each day is divided into 1000 equal parts (000–999).  
   - One milli‑day = 86.4 seconds.
4. Day boundary: at (mean) astronomical noon at a fixed reference meridian located midway between Little Diomede Island (USA) and Big Diomede Island (Russia): 168° 58′ 30″ W.
5. Transition rules:
   - When the sub‑day counter rolls over 999 → 000, the day index increments.
   - When the vernal equinox occurs, the year day index resets to 0 regardless of the previous count (even if not yet at 365/366).
6. Required astronomy:
   - Precise calculation of vernal equinox instants (Meeus algorithms / solar apparent longitude = 0°).
   - Equation of Time (EoT) to relate apparent vs. mean solar time (for defining “mean astronomical noon” and optionally refining the start of day).

### Rationale

The tropical year (interval between two vernal equinoxes) has a relatively stable length (~365.2422 mean solar days). Using its natural boundaries avoids the Gregorian leap day machinery. Expressi...

### Core Quantities

| Symbol | Meaning |
|--------|---------|
| T_eq_y | Exact UTC (or TT → then converted) instant of current year’s vernal equinox |
| T_eq_next | Exact instant of next vernal equinox |
| Y_len_days | (T_eq_next − T_eq_y) / 86400 (can be ~365.24…) |
| D_max | Integer number of full days in interval: round(T_eq_next − T_eq_y in days) → 365 or 366 |
| T_ref_meridian | Longitude λ_ref = −168° 58′ 30″ (decimal: −168.975°) |
| LMT (Local Mean Time) | UTC + λ_ref / 15 h |
| Mean noon | LMT = 12:00:00 |
| EoT | Apparent Solar Time − Mean Solar Time |
| Start of day | Mean local noon corrected per intended definition (see below) |

### Interpreting “start of day is mean astronomical noon (Equation of Time = 0)”

There are two possible interpretations; the project should clarify which to adopt:

1. Strict Mean Noon Interpretation (recommended initial implementation):
   - Start of each day occurs when Local Mean Solar Time (at λ_ref) = 12:00:00 (LMT noon).
   - EoT is computed only for optional display (showing difference to apparent solar time).

2. EoT Zero Crossing Interpretation:
   - Start of each day would be when EoT = 0 at the reference meridian (moments when apparent and mean solar time coincide). (Complication: EoT=0 occurs only ~4 times per tropical year → unsuita...
   
Because the second interpretation cannot define daily boundaries, we proceed with (1). The README keeps the original note but clarifies operational meaning.

### Time Representation

We define an astronomical timestamp:

Year_Epoch = T_eq_y (UTC)
Now = t (UTC instant)

1. If t < T_eq_y, recompute for previous equinox.
2. Compute Δt = t − T_eq_y (seconds).
3. Compute dies = floor( (t − T_eq_y − offset_to_first_noon) / 86400 ), where offset_to_first_noon aligns day 0 start to the first mean noon after the equinox (or at equinox if it falls b...
4. Compute intra_day_seconds = (t − start_of_current_day).
5. miliDies = floor( 1000 * intra_day_seconds / 86400 ). Range 000–999.
6. When miliDies rolls 999 → 000, dies increments.
7. If t ≥ T_eq_next, reset dies → 0 and recompute new frame.

Display Format (proposal):
YYYYeq:DDD.mmm
- YYYYeq: Gregorian year of the equinox starting the frame
- DDD: zero-padded dies (e.g., 000–365/366)
- mmm: miliDies (000–999)

Example: 2025eq:123.457

### Algorithms Needed

1. Vernal Equinox Time (Meeus):
   - Use Jean Meeus “Astronomical Algorithms” Chapter for solar longitude.
   - Compute apparent solar longitude λ (corrected for nutation, aberration).
   - Find root of λ(t) − 0° (mod 360) near March equinox using iterative method (e.g., Newton-Raphson with derivative from mean motion ~0.9856°/day).
   - Higher precision: Evaluate in Terrestrial Time (TT); convert to UTC:
     UTC = TT − ΔT (ΔT can be approximated; store table or polynomial).

2. Equation of Time (EoT):
   - EoT = GHA_mean_sun − GHA_apparent_sun (or classical formula combining eccentricity and obliquity terms).
   - For display and (optionally) refining mean noon vs apparent noon.

3. Reference Meridian Mean Noon:
   - LMT = UTC + λ_ref / 15.
   - Mean noon occurs when LMT = 12:00. So:
     Start-of-day candidate = floor( (UTC + λ_ref / 15h) / 24h ) * 24h − λ_ref / 15h + 12h
   - Ensure start-of-day ≥ T_eq_y for day 0. If equinox occurs after that day's noon, use next day’s noon as start-of-day.

### Handling Day Count (365 vs 366)

Because the tropical year length is ~365.2422 days:

- Compute int_days = floor( (T_eq_next − T_eq_y) / 86400 ) → usually 365.
- If fractional remainder + alignment with noon boundaries pushes number of distinct day starts to 366, then D_max=366.
- Accept that final day may have fewer miliDies units if the equinox truncates it; or, alternatively, re-scale the last day (OPTION A vs OPTION B):

Option A (simpler): Truncate final day at next equinox (last miliDies may not reach 999).  
Option B (normalized): Stretch scaling on each day to ensure full 1000 milli-days (complicates uniformity).  
We choose Option A initially.

### Precision Targets

| Quantity | Target Accuracy | Method |
|----------|-----------------|--------|
| Equinox instant | < 1 minute | VSOP87D + iteration |
| EoT | < few seconds | Standard simplified formula |
| Day boundary alignment | < 1 second | Use high-resolution time libs |

**NEW:** The implementation now includes a dynamic VSOP87D coefficient loading system that allows configurable precision. See `VSOP87D_SYSTEM.md` for details.

### VSOP87D Dynamic Precision System

The astronomical calculations now support configurable precision through the VSOP87D Earth coefficient system:

```python
from core.solar import solar_longitude_from_datetime

# Default precision
lon = solar_longitude_from_datetime(datetime_obj)

# High precision (1 arcsecond accuracy)
lon_precise = solar_longitude_from_datetime(datetime_obj, max_error_arcsec=1.0)
```

**Features:**
- On-demand coefficient loading based on accuracy requirements
- Conservative error bounds for Earth heliocentric longitude
- Automatic fallback to default coefficients
- Backward compatibility with existing code

**Generator Script:** `scripts/generate_vsop87.py` can download VSOP87D data and create coefficient files with custom precision levels.

## Implementation Status

✅ **Completed:**
- Core astronomical calculations (VSOP87D, equinox computation, Dies/miliDies/mikroDies)
- Desktop GUI application with widget and normal modes
- 28-language localization system
- Interactive calendar with Dies display
- Bidirectional time converter
- Educational explanation cards
- Settings and preferences system
- Cross-platform support (Linux, macOS, Windows)

📋 **Future Considerations:**
- Web visualization with circular dial
- Mobile applications (PWA or native)
- Additional astronomical data displays

## Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
python -m pytest tests/

# Run specific test suites
python -m pytest tests/test_astro_time_core.py -v
python -m pytest tests/test_equinox.py -v
python -m pytest tests/test_vsop87d_system.py -v
```

Test categories:
- **Core calculations**: Equinox computation, Dies/miliDies conversion
- **VSOP87D system**: Solar longitude precision and accuracy
- **UI components**: Gradient themes, widget functionality
- **Time scales**: Delta-T calculations and time conversions

---

## Srpski / Bosanski / Croatian

Astronomical-watch je eksperimentalni sistem mjerenja vremena koji zamjenjuje klasičan kalendar i sat prikazom zasnovanim na ponavljajućim astronomskim pojavama:

1. Granica godine: trenutak sjeverne proljetne (prolećne) ravnodnevnice.
2. Broj dana: broje se od 0 do 365 (ili 366) unutar intervala između dvije uzastopne proljetne ravnodnevnice.
3. Podjela dana: svaki dan se dijeli na 1000 jednakih dijelova (000–999).
   - Jedna hiljaditina dana = 86,4 sekundi.
4. Početak dana: srednje astronomsko podne na referentnom meridijanu između američkog Diomede (Little Diomede) i ruskog Diomede (Big Diomede): 168° 58′ 30″ W.
5. Pravila prelaza:
   - Kad se 999 → 000, dan se povećava za 1.
   - Kad nastupi proljetna ravnodnevnica, dan se resetuje na 0 (počinje nova astronomska godina).
6. Potrebni proračuni:
   - Tačan trenutak proljetne ravnodnevnice (Meeus).
   - Jednačina vremena (Equation of Time) za odnos prividnog i srednjeg solarnog vremena.

### Obrazloženje

Tropska godina (između ravnodnevnica) je relativno stabilna (~365,2422 dana). Korištenje njenih prirodnih granica eliminiše potrebu za gregorijanskim prestupnim pravilima na prikazu.

### Ključne veličine

(Analogno engleskom dijelu; zadržavamo simbole radi jednoznačnosti.)

### Tumačenje “početak dana je srednje astronomsko podne (Equation of Time = 0)”

Praktično ćemo uzeti da je početak dana srednje solarno podne po lokalnom srednjem vremenu referentnog meridijana (jer EoT=0 se javlja samo ~4 puta godišnje, što nije pogodno za dnevnu grani...

### Reprezentacija vremena

Format: YYYYeq:DDD.mmm (npr. 2025eq:123.457)

### Algoritmi

- Meeus za Sunce i ravnodnevnicu (solar longitude = 0°).
- Jednačina vremena standardnom formulom.

## Security Exception Summary
Urgent security patches may be temporarily distributed under strict conditions (see LICENSE.CORE §11) to remediate exploitable vulnerabilities; long-term divergence is not allowed.

See: LICENSE.CORE, LICENSE.MIT, SPEC.md, TRADEMARK_POLICY.md, CONTRIBUTING.md

## Rationale
Ensures a stable canonical definition while allowing broad ecosystem tooling.

## Roadmap
- [ ] ΔT refinement & higher precision solar terms
## Disclaimer
Not for navigation; educational / experimental.

## Contributing
Read CONTRIBUTING.md first. Contributions welcome for:
- Bug fixes and optimizations
- Extensions and integrations
- Documentation improvements
- Translation additions

## License

- **Core algorithms**: Astronomical Watch Core License v1.0 (restrictive)
- **UI & Application**: MIT License

See LICENSE.CORE and LICENSE.MIT for details.

---

**Built with Python 3.8+ • Tkinter • VSOP87D astronomical algorithms**
