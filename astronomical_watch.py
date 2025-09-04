"""
Astronomical Watch - Main module
Provides basic astronomical calculations including equinox computation.
"""
from __future__ import annotations
import math
from datetime import datetime, timezone

# Import core modules
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