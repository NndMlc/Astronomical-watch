"""
VSOP87 trunkirani model za Zemlju: L, B, R (primer, lako proširivo).
Za punu tačnost popuniti sve tabele L0..L5, B0..B5, R0..R5 iz zvanične tablice.
Sve vrednosti u radijanima (L, B) i AU (R).
"""
import math

# Trunkirane serije (samo nekoliko termina, za demonstraciju)
L0 = [
    (175347046.0, 0, 0),
    (3341656.0, 4.6692568, 6283.07585),
    (34894.0, 4.6261, 12566.1517),   
    (3497.0, 2.7441, 5753.3849),
    (3418.0, 2.8289, 3.5231),
]
L1 = [
    (628331966747.0, 0, 0),
    (206059.0, 2.678235, 6283.07585),
]
L2, L3, L4, L5 = [], [], [], []
B0 = [
    (280.0, 3.199, 84334.662),
    (102.0, 5.422, 5507.553),
]
B1, B2, B3, B4, B5 = [], [], [], [], []
R0 = [
    (100013989.0, 0, 0),
    (1670700.0, 3.0984635, 6283.07585),
    (13956.0, 3.05525, 12566.1517),
]
R1 = [
    (103019.0, 1.107490, 6283.07585),
    (1721.0, 1.0644, 12566.1517),
]
R2, R3, R4, R5 = [], [], [], []

def _sum(terms, t):
    return sum(A * math.cos(B + C * t) for A, B, C in terms)

def _eval(series, t):
    return sum(_sum(group, t) * t**n for n, group in enumerate(series))

def _t(jd):
    return (jd - 2451545.0) / 365250.0

def earth_heliocentric_longitude(t):
    return (_eval([L0, L1, L2, L3, L4, L5], t) / 1e8) % (2 * math.pi)

def earth_heliocentric_latitude(t):
    return _eval([B0, B1, B2, B3, B4, B5], t) / 1e8

def earth_radius_vector(t):
    return _eval([R0, R1, R2, R3, R4, R5], t) / 1e8

def earth_heliocentric_position(jd):
    t = _t(jd)
    return (
        earth_heliocentric_longitude(t),
        earth_heliocentric_latitude(t),
        earth_radius_vector(t),
    )
    
