"""
solar.py
Osnovne heliocentričke geometrijske pozicije (demonstracija).
Korišćen je trunkirani VSOP87 (samo longituda iz vsop87_earth) + jednostavna korekcija nutacije
za geometrijsku sunčevu longitudu. Ovo NIJE fizički kompletno.
"""
from __future__ import annotations
import math
from datetime import datetime
from .timebase import timescales_from_datetime, J2000
from .vsop87_earth import earth_heliocentric_longitude
from .nutation import nutation_simple, mean_obliquity

TAU = 2 * math.pi

def centuries_since_j2000(jd: float) -> float:
    return (jd - J2000) / 36525.0

def apparent_solar_longitude(jd: float) -> float:
    """
    Vraća aproksimativnu prividnu ekliptičku longitudu Sunca (rad),
    koristeći trunkiranu heliocentričku longitudu Zemlje i dodavanje π (geocentrički).
    Dodaje i nutacionu korekciju dpsi * cos(eps).
    """
    t = centuries_since_j2000(jd)
    L_earth = earth_heliocentric_longitude(t / 10.0)
    L = (L_earth + math.pi) % TAU
    nut = nutation_simple(jd)
    L_app = (L + nut.dpsi * math.cos(nut.eps)) % TAU
    return L_app

def solar_longitude_from_datetime(dt: datetime) -> float:
    ts = timescales_from_datetime(dt)
    return apparent_solar_longitude(ts.jd_tt)

__all__ = ["apparent_solar_longitude", "solar_longitude_from_datetime"]