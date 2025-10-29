"""
astronomical_watch.py - Main astronomical watch module.

Provides core functions for astronomical time calculations, including
vernal equinox computation (simplified) and an 'astronomical clock' reading.
"""
from __future__ import annotations

import math

from datetime import datetime, timezone

# Import core modules

from datetime import datetime, timezone, timedelta
from typing import Optional

from src.astronomical_watch.core.solar import solar_longitude_from_datetime


def compute_vernal_equinox(year: int) -> datetime:
    """
    Compute the vernal equinox instant for a given year using Newton-Raphson
    iteration on apparent solar longitude.

    The vernal equinox occurs when apparent solar longitude ≈ 0° (mod 360°).
    We normalize longitude into (-π, π] and seek the root near zero.

    Args:
        year: Gregorian year.

    Returns:
        UTC datetime of approximate equinox (precision depends on solar_longitude_from_datetime).
    """

    # Approximate date around March 20th
    approx_date = datetime(year, 3, 20, 12, 0, tzinfo=timezone.utc)
    
    # Use simple iteration to find when solar longitude is closest to 0
    best_dt = approx_date
    best_diff = float('inf')
    
    # Search within ±3 days of approximate date
    from datetime import timedelta
    for hours_offset in range(-72, 73, 1):  # Check every hour in ±3 days
        test_dt = approx_date + timedelta(hours=hours_offset)
        
        try:
            solar_lon = solar_longitude_from_datetime(test_dt)
            # Find minimum angular difference from 0
            diff = min(abs(solar_lon), abs(solar_lon - 2*math.pi))
            
            if diff < best_diff:
                best_diff = diff
                best_dt = test_dt
        except (ValueError, TypeError):
            continue
    
    return best_dt


def astronomical_now(utc_time: Optional[datetime] = None) -> dict:
    """
    Compute an astronomical 'watch' snapshot relative to the latest vernal equinox.

    Args:
        utc_time: Optional explicit UTC datetime; if None, uses current UTC.

    Returns:
        dict with:
          - equinox_epoch: datetime of current equinox epoch
          - next_equinox: datetime of next equinox
          - day_index: integer days since equinox
          - milli_day: thousandths of current civil day since last midnight boundary relative to equinox day count
          - raw_fraction: fraction of the equinox year elapsed (simple ratio)
          - year: equinox epoch year
          - timestamp: formatted string "YYYYeq:DDD.mmm"
    """
    if utc_time is None:
        utc_time = datetime.now(timezone.utc)
    elif utc_time.tzinfo is None:
        utc_time = utc_time.replace(tzinfo=timezone.utc)
    else:
        utc_time = utc_time.astimezone(timezone.utc)

    year = utc_time.year
    current_equinox = compute_vernal_equinox(year)

    if utc_time < current_equinox:
        year -= 1
        current_equinox = compute_vernal_equinox(year)
        next_equinox = compute_vernal_equinox(year + 1)
    else:
        next_equinox = compute_vernal_equinox(year + 1)

    elapsed = utc_time - current_equinox
    total_seconds = elapsed.total_seconds()

    day_index = int(total_seconds // 86400)
    remainder_seconds = total_seconds % 86400
    milli_day = int((remainder_seconds / 86400) * 1000)

    raw_fraction = total_seconds / (next_equinox - current_equinox).total_seconds()

    return {
        "equinox_epoch": current_equinox,
        "next_equinox": next_equinox,
        "day_index": day_index,
        "milli_day": milli_day,
        "raw_fraction": raw_fraction,
        "year": year,
        "timestamp": f"{year}eq:{day_index:03d}.{milli_day:03d}",
    }


__all__ = ["compute_vernal_equinox", "astronomical_now", "astronomical_time"]


def astronomical_time(utc_time: Optional[datetime] = None) -> tuple[int, int]:
    """
    Get current astronomical time as (day_index, milli_day) tuple.
    
    Args:
        utc_time: Optional UTC datetime, defaults to now
        
    Returns:
        Tuple of (day_index, milli_day)
    """
    result = astronomical_now(utc_time)
    return result["day_index"], result["milli_day"]

