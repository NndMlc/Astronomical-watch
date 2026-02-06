"""
# Astro Time System (Core Specification)

This document defines the invariant astronomical time abstraction used by the Astronomical Watch.

## 1. Reference Meridian
Longitude: **168° 58' 30" W** (decimal: -168.975°)

## 2. Daily Boundary (Global Noon)
Mean Solar Noon (LMST = 12h) at the reference meridian corresponds to a fixed UTC time because we adopt the *mean* (uniform) solar day and ignore Equation of Time variations.

Longitude / 15 = -11.265 hours
UTC hour for LMST=12h is: 12 + (-11.265) = 0.735 h = **00:44:06 UTC**.

Thus every astronomical day (Dies) begins at **00:44:06 UTC** globally and lasts exactly 86,400 SI seconds.

## 3. miliDies
The day is divided into 1000 equal units (miliDies):
- 1 miliDies = 86.4 seconds
- miliDies range: 0 .. 999
- At the daily boundary (00:44:06 UTC) miliDies resets 999 → 000.

Computation for any UTC timestamp *t*:
1. Determine last global noon (00:44:06 UTC) ≤ t.
2. seconds_since = t - last_noon
3. fraction = seconds_since / 86400
4. milidan = floor(fraction * 1000)

## 4. Astronomical Year & Equinox Reset
An astronomical year runs from one real vernal equinox instant to the next.
At the exact UTC instant of the vernal equinox:
- **Dies resets to 0 immediately** (even if in the middle of a day)
- **miliDies DOES NOT reset** (it continues smoothly)

The first global noon after the equinox starts Dies = 1 (miliDies = 000 at that boundary). Each subsequent global noon increments Dies.

## 5. Variable Year Length
Because the real interval between successive vernal equinoxes is ~365.24 mean solar days, the number of whole day transitions (noons) per astronomical year can vary (sometimes 365, sometimes 366). The system does *not* force a fixed length. There are two partial segments: from equinox to first noon, and from final noon to next equinox (unless equinox aligns with a noon).

## 6. Required Data at Startup
The application must know (or compute):
- previous vernal equinox UTC (current_equinox)
- next vernal equinox UTC (next_equinox)

These are passed to the core (AstroYear). The caller updates `next_equinox` when a newer prediction is available. On or after that instant the core rolls over automatically on `reading()`.

## 7. Global Uniqueness
The pair (Dies, miliDies) is identical worldwide at a given UTC instant because all calculations use a single meridian and UTC.

## 8. API Summary
- `AstroYear(current_equinox: datetime, next_equinox: Optional[datetime])`
- `reading(t: datetime) -> AstroReading` returns (Dies, miliDies, mikroDies, utc)
- `update_next_equinox(next_equinox)` to set the future equinox
- Automatic rollover when `t >= next_equinox` inside `reading()`.

## 9. Edge Cases
- If equinox occurs exactly at 00:44:06 UTC: Dies = 0 and miliDies = 0 simultaneously.
- If equinox occurs during the day: Dies becomes 0 immediately; miliDies keeps progressing until the boundary.
- Leap seconds are ignored (days are fixed 86400 s). If needed later, a higher-level adjustment layer can handle them without changing core semantics.

## 10. Reverse Approximation
`approximate_utc_from_day_miliDies(Dies, miliDies)` provides a best-effort UTC reconstruction; exact mapping for Dies=0 is ambiguous (because day 0 begins at the equinox instant, not at a noon boundary) and uses equinox + offset.

---
This core is intentionally minimal to ensure long-term stability and global consistency.
"""
