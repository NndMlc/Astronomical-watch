"""
vsop87_earth.py
Trunkirani (DEMO) VSOP87 koeficijenti za heliocentričku longitudu Zemlje.
Za ozbiljnu tačnost treba dodati kompletne serije L0..L5.
"""
import math
from typing import Sequence

L0: Sequence[tuple[float, float, float]] = [
    (175347046.0, 0.0, 0.0),
    (3341656.0, 4.6692568, 6283.07585),
    (34894.0, 4.62610, 12566.15170),
    (3497.0, 2.7441, 5753.3849),
    (3418.0, 2.8289, 3.5231),
]

def series_sum(terms: Sequence[tuple[float, float, float]], t: float) -> float:
    s = 0.0
    for A, B, C in terms:
        s += A * math.cos(B + C * t)
    return s

def earth_heliocentric_longitude(t: float) -> float:
    L = series_sum(L0, t)
    L /= 1e8
    return L % (2 * math.pi)