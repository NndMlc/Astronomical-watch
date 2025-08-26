"""
solar.py
Prividna ekliptička dužina Sunca i udaljenost, uz opcioni zahtev za maksimalnu grešku modela.
"""
from __future__ import annotations
import math
from datetime import datetime
from .timebase import timescales_from_datetime
from .vsop87_earth import earth_heliocentric_position
from .nutation import nutation_simple

TAU = 2 * math.pi

def apparent_solar_longitude(jd_tt: float, max_error_arcsec: float | None = None) -> float:
    L_e, B_e, R_e = earth_heliocentric_position(jd_tt, max_error_arcsec=max_error_arcsec)
    L_geo = (L_e + math.pi) % TAU
    nut = nutation_simple(jd_tt)
    return (L_geo + nut.dpsi * math.cos(nut.eps)) % TAU

def solar_longitude_and_distance_from_datetime(dt: datetime, max_error_arcsec: float | None = None):
    ts = timescales_from_datetime(dt)
    L_e, B_e, R_e = earth_heliocentric_position(ts.jd_tt, max_error_arcsec=max_error_arcsec)
    L_geo = (L_e + math.pi) % TAU
    nut = nutation_simple(ts.jd_tt)
    L_app = (L_geo + nut.dpsi * math.cos(nut.eps)) % TAU
    return L_app, R_e

def solar_longitude_from_datetime(dt: datetime, max_error_arcsec: float | None = None) -> float:
    return solar_longitude_and_distance_from_datetime(dt, max_error_arcsec)[0]

__all__ = [
    "apparent_solar_longitude",
    "solar_longitude_from_datetime",
    "solar_longitude_and_distance_from_datetime",
]