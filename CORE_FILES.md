# Core Skeleton Files

Ovaj skeleton obuhvata:

- `core/timebase.py` – Julian Day, TT aproksimacija, ΔT stub.
- `core/vsop87_earth.py` – Trunkirani VSOP87 koeficijenti za longitudu Zemlje (DEMO).
- `core/nutation.py` – Uprošćena nutacija + srednja kosoća.
- `core/solar.py` – Prividna sunčeva longitudа (stub).
- `core/frames.py` – Konverzija ekliptičke u ekvatorijalnu koordinatu (srednja kosoća).
- `core/__init__.py` – Re-export ključnih funkcija.

## TODO (dalje faze)

1. ~~Proširiti VSOP87 (L,B,R kompletne serije) ili uvesti bolji model (ELP za Mesec kasnije).~~ ✅ **COMPLETED** - Implemented dynamic VSOP87D coefficient loading system with configurable precision
2. Implementirati IAU 2000A/2006 nutaciju i precesiju.
3. Preciznije računanje ΔT (ephemeris + istorijski fit).
4. Dodati transformacije prema ITRF / topocentričke koordinate.
5. Test pokrivenost za numeričku stabilnost i regresije.

**NEW VSOP87D System**: The skeleton now includes a complete dynamic coefficient loading system. See `VSOP87D_SYSTEM.md` for details on:
- Configurable precision via `max_error_arcsec` parameter
- Automatic coefficient file selection and loading  
- Generator script for creating custom precision levels
- Conservative error bound calculations

## Test

`tests/test_core_skeleton.py` proverava osnovne domene (raspon vrednosti, monotonost JD).