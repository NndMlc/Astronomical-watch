"""Tests for astro_time_core module."""
from datetime import datetime, timezone, timedelta
from astronomical_watch.core.astro_time_core import (
    AstroYear,
    NOON_UTC_HOUR,
    NOON_UTC_MINUTE,
    NOON_UTC_SECOND,
    SECONDS_PER_DAY,
    MILLIDAN_PER_DAY,
    SECONDS_PER_MILLIDAN,
)

def test_equnox_reset_mid_day():
    eq = datetime(2025, 3, 20, 8, 5, tzinfo=timezone.utc)
    ay = AstroYear(eq)
    r_eq = ay.reading(eq)
    assert r_eq.dies == 0
    # milidan is some value within 0..999
    assert 0 <= r_eq.milidan < 1000

def test_first_noon_index_progression():
    eq = datetime(2025, 3, 20, 8, 5, tzinfo=timezone.utc)
    ay = AstroYear(eq)
    first_noon = ay._first_noon_after_eq
    # Pre first noon -> still day 0
    r_before = ay.reading(first_noon - timedelta(seconds=10))
    assert r_before.dies == 0
    # At first noon -> start of day 1, milidan=0
    r_noon = ay.reading(first_noon)
    assert r_noon.dies == 1
    assert r_noon.milidan == 0
    # After +1 day + 1s -> day 2
    r_next = ay.reading(first_noon + timedelta(days=1, seconds=1))
    assert r_next.day_index == 2

def test_milidan_progression():
    eq = datetime(2025, 3, 20, 8, 5, tzinfo=timezone.utc)
    ay = AstroYear(eq)
    first_noon = ay._first_noon_after_eq
    t = first_noon + timedelta(seconds=100 * SECONDS_PER_MILLIDAN)
    r = ay.reading(t)
    assert r.day_index == 1
    assert r.milidan == 100

def test_rollover_next_equinox():
    eq = datetime(2025, 3, 20, 8, 5, tzinfo=timezone.utc)
    next_eq = datetime(2026, 3, 20, 9, 0, tzinfo=timezone.utc)
    ay = AstroYear(eq, next_eq)
    # Force rollover
    after_next = next_eq + timedelta(seconds=10)
    r = ay.reading(after_next)
    assert r.dies == 0
    # Now first noon for new cycle
    first_noon_new = ay._first_noon_after_eq
    r2 = ay.reading(first_noon_new)
    assert r2.dies == 1

def test_approximate_mapping():
    eq = datetime(2025, 3, 20, 8, 5, tzinfo=timezone.utc)
    ay = AstroYear(eq)
    first_noon = ay._first_noon_after_eq
    # pick a moment in day 2
    target = first_noon + timedelta(days=1, seconds=200 * SECONDS_PER_MILLIDAN)
    r = ay.reading(target)
    assert r.day_index == 2
    approx = ay.approximate_utc_from_day_milidan(r.day_index, r.milidan)
    # Should be close (within one milidan)
    assert abs((approx - target).total_seconds()) < SECONDS_PER_MILLIDAN + 1

