"""

astronomical_watch.py - Main astronomical watch module

Provides core functions for astronomical time calculations, including
vernal equinox computation and astronomical time reading.
"""
from __future__ import annotations

import math
from datetime import datetime, timezone, timedelta
from typing import Union

from core.solar import solar_longitude_from_datetime


def compute_vernal_equinox(year: int) -> datetime:
    """
    Compute the vernal equinox instant for a given year using iterative solar longitude calculation.

    The vernal equinox occurs when the apparent solar longitude equals 0° (mod 360°).
    Uses Newton-Raphson iteration to find the root.

    Args:
        year: The year for which to compute the vernal equinox

    Returns:
        datetime: The vernal equinox instant in UTC timezone
    """
    # Initial guess: March 20 at noon UTC (typical equinox date)
    initial_guess = datetime(year, 3, 20, 12, 0, 0, tzinfo=timezone.utc)

    # Newton-Raphson iteration to find when solar longitude = 0
    current_dt = initial_guess

    for _ in range(10):  # Maximum 10 iterations should be enough
        # Calculate solar longitude at current time
        longitude = solar_longitude_from_datetime(current_dt)

        # Normalize longitude to [-pi, pi] for easier root finding
        if longitude > math.pi:
            longitude -= 2 * math.pi

        # If we're close enough to zero, we're done
        if abs(longitude) < 1e-8:  # About 0.2 arcseconds
            break

        # Calculate derivative (approximate rate of solar longitude change)
        # The sun moves roughly 0.9856 degrees per day = 0.01720 radians per day
        dt_step = timedelta(hours=1)
        longitude_plus = solar_longitude_from_datetime(current_dt + dt_step)
        if longitude_plus > math.pi:
            longitude_plus -= 2 * math.pi

        derivative = (longitude_plus - longitude) / (dt_step.total_seconds() / 86400.0)  # rad/day

        if abs(derivative) < 1e-10:
            break  # Avoid division by zero

        # Newton-Raphson step: x_{n+1} = x_n - f(x_n) / f'(x_n)
        correction_days = -longitude / derivative
        current_dt = current_dt + timedelta(days=correction_days)

    return current_dt


def astronomical_now(utc_time: Union[datetime, None] = None) -> dict:
    """
    Get the current astronomical time reading.

    Args:
        utc_time: UTC datetime to convert, or None for current time

    Returns:
        dict: Astronomical time information including equinox epoch, day index, etc.
    """
    if utc_time is None:
        utc_time = datetime.now(timezone.utc)

    if utc_time.tzinfo is None:
        utc_time = utc_time.replace(tzinfo=timezone.utc)

    # Determine the appropriate equinox year
    year = utc_time.year
    current_equinox = compute_vernal_equinox(year)

    if utc_time < current_equinox:
        # Use previous year's equinox
        year -= 1
        current_equinox = compute_vernal_equinox(year)
        next_equinox = compute_vernal_equinox(year + 1)
    else:
        next_equinox = compute_vernal_equinox(year + 1)

    # Calculate day index and milli-day
    elapsed = utc_time - current_equinox
    total_seconds = elapsed.total_seconds()

    day_index = int(total_seconds // 86400)
    remainder_seconds = total_seconds % 86400
    milli_day = int((remainder_seconds / 86400) * 1000)

    return {
        'equinox_epoch': current_equinox,
        'next_equinox': next_equinox,
        'day_index': day_index,
        'milli_day': milli_day,
        'raw_fraction': total_seconds / (next_equinox - current_equinox).total_seconds(),
        'year': year,
        'timestamp': f"{year}eq:{day_index:03d}.{milli_day:03d}"
    }


__all__ = ['compute_vernal_equinox', 'astronomical_now']
=======
Astronomical Watch - Main module
Provides basic astronomical calculations including equinox computation.
"""
from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Optional

# Import core modules
from core.timebase import timescales_from_datetime
from core.solar import solar_longitude_from_datetime

def compute_vernal_equinox(year: int) -> datetime:
    """
    Compute the vernal equinox datetime for a given year.
    
    This is a simplified implementation that will be improved with VSOP87D.
    Currently uses an approximate calculation.
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
        except:
            continue
    
    return best_dt


__all__ = ['compute_vernal_equinox']
