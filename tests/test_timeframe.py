from astronomical_watch import astronomical_time, compute_vernal_equinox

def test_basic_conversion():
    eq = compute_vernal_equinox(2025)
    dt = eq.replace(hour=min(eq.hour + 6, 23))
    day_index, milli = astronomical_time(dt)
    assert day_index in (0, 1)
    assert 0 <= milli <= 999
