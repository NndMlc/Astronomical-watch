import math
from datetime import datetime, timezone
from astronomical_watch.core.timebase import timescales_from_datetime
from astronomical_watch.core.solar import solar_longitude_from_datetime
from astronomical_watch.core.nutation import nutation_simple
from astronomical_watch.core.frames import ecliptic_to_equatorial

def test_julian_day_monotonic():
    dt1 = datetime(2024, 1, 1, tzinfo=timezone.utc)
    dt2 = datetime(2024, 1, 2, tzinfo=timezone.utc)
    ts1 = timescales_from_datetime(dt1)
    ts2 = timescales_from_datetime(dt2)
    assert ts2.jd_utc > ts1.jd_utc
    assert ts2.jd_tt > ts1.jd_tt

def test_solar_longitude_range():
    dt = datetime(2024, 3, 20, 12, 0, tzinfo=timezone.utc)
    lam = solar_longitude_from_datetime(dt)
    assert 0 <= lam < 2 * math.pi

def test_nutation_basic():
    dt = datetime(2024, 6, 1, tzinfo=timezone.utc)
    jd = timescales_from_datetime(dt).jd_tt
    nut = nutation_simple(jd)
    assert abs(nut.dpsi) < 0.005
    assert abs(nut.deps) < 0.005

def test_frame_conversion_identity_equator():
    dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
    jd = timescales_from_datetime(dt).jd_tt
    ra, dec = ecliptic_to_equatorial(0.0, 0.0, jd)
    assert abs(dec) < 1e-10
    assert abs(ra) < 1e-10 or abs(ra - 2*math.pi) < 1e-10
