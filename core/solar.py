"""
solar.py
Osnovne heliocentričke geometrijske pozicije (demonstracija).
Korišćen je trunkirani VSOP87 (samo longituda iz vsop87_earth) + jednostavna korekcija nutacije
za geometrijsku sunčevu longitudu. Ovo NIJE fizički kompletno.

Updated to support configurable VSOP87D precision via max_error_arcsec parameter.
"""
from __future__ import annotations
import math
from datetime import datetime
from typing import Optional
from .timebase import timescales_from_datetime, J2000
from .vsop87_earth import earth_heliocentric_longitude
from .nutation import nutation_simple, mean_obliquity

TAU = 2 * math.pi

def centuries_since_j2000(jd: float) -> float:
    return (jd - J2000) / 36525.0

def apparent_solar_longitude(jd: float, max_error_arcsec: Optional[float] = None) -> float:
    """
    Vraća aproksimativnu prividnu ekliptičku longitudu Sunca (rad),
    koristeći trunkiranu heliocentričku longitudu Zemlje i dodavanje π (geocentrički).
    Dodaje i nutacionu korekciju dpsi * cos(eps).
    
    Args:
        jd: Julian Day (TT)
        max_error_arcsec: Maximum acceptable error in arcseconds for VSOP87 calculation.
                         If None, uses default precision from current vsop87_earth module.
                         If specified, will use on-demand loading of appropriate coefficients.
    """
    t = centuries_since_j2000(jd)
    
    # Get Earth's heliocentric longitude 
    # If max_error_arcsec is specified, this will eventually trigger dynamic loading
    L_earth = earth_heliocentric_longitude(t / 10.0, max_error_arcsec=max_error_arcsec)
    
    # Convert to geocentric solar longitude
    L = (L_earth + math.pi) % TAU
    
    # Apply nutation correction
    nut = nutation_simple(jd)
    L_app = (L + nut.dpsi * math.cos(nut.eps)) % TAU
    
    return L_app

def solar_longitude_from_datetime(dt: datetime, max_error_arcsec: Optional[float] = None) -> float:
    """
    Compute apparent solar longitude from datetime with optional precision control.
    
    Args:
        dt: Datetime object
        max_error_arcsec: Maximum acceptable error in arcseconds
    """
    ts = timescales_from_datetime(dt)
    return apparent_solar_longitude(ts.jd_tt, max_error_arcsec=max_error_arcsec)

__all__ = ["apparent_solar_longitude", "solar_longitude_from_datetime"]