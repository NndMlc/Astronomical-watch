from astronomical_watch import compute_vernal_equinox

def test_equinox_basic_range():
    eq = compute_vernal_equinox(2025)
    assert eq.month == 3
    assert 18 <= eq.day <= 22
