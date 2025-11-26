from astronomical_watch import astronomical_time, compute_vernal_equinox

def test_basic_conversion():
    eq = compute_vernal_equinox(2025)
    dt = eq.replace(hour=min(eq.hour + 6, 23))
    dies, miliDies = astronomical_time(dt)
    assert dies in (0, 1)
    assert 0 <= miliDies <= 999
