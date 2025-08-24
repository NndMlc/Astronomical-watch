
from datetime import timezone
from astronomical_watch import compute_vernal_equinox

# Provisional reference vernal equinox UTC times (high‑precision ephemerides, e.g. published astronomical almanacs)
# Source note: Values approximate (rounded to nearest minute). These are used only for coarse validation
# until a stricter tolerance & authoritative ephemeris comparison harness is integrated.
# Years chosen span multiple leap year patterns.
REFERENCE_EQUINOX_UTC = {
    2023: (3, 20, 21, 24),  # 2023-03-20 21:24 UTC
    2024: (3, 20, 3, 6),    # 2024-03-20 03:06 UTC
    2025: (3, 20, 9, 1),    # 2025-03-20 09:01 UTC
    2026: (3, 20, 14, 46),  # 2026-03-20 14:46 UTC
    2027: (3, 20, 20, 24),  # 2027-03-20 20:24 UTC
    2028: (3, 20, 2, 17),   # 2028-03-20 02:17 UTC
    2029: (3, 20, 8, 1),    # 2029-03-20 08:01 UTC
    2030: (3, 20, 13, 51),  # 2030-03-20 13:51 UTC
}

# Current simplified algorithm is low‑precision; we allow a wide window initially.
# Threshold rationale:
#   - Empirically expect error < ~2h with current approach for these years.
#   - Set MAX_ALLOWED_DIFF_SECONDS = 3h to avoid flaky CI while still catching gross regressions.
# Roadmap: tighten to 1h => 30m => 10m as algorithms improve (ΔT modeling, better solar apparent longitude series).
MAX_ALLOWED_DIFF_SECONDS = 3 * 3600  # 3 hours


def test_equinox_coarse_precision():
    for year, (month, day, hour, minute) in REFERENCE_EQUINOX_UTC.items():
        ref_ts = (compute_vernal_equinox(year).tzinfo.__class__  # just to ensure tz aware
                   )  # noqa: E501 (dummy use to satisfy linter if needed)
        eq = compute_vernal_equinox(year)
        assert eq.tzinfo is not None, "Equinox datetime must be timezone-aware (UTC)."
        assert eq.month == 3 and eq.day in (19, 20, 21), "Unexpected month/day for equinox candidate."
        # Compose reference datetime
        from datetime import datetime
        ref = datetime(year, month, day, hour, minute, tzinfo=eq.tzinfo)
        diff = abs((eq - ref).total_seconds())
        assert diff <= MAX_ALLOWED_DIFF_SECONDS, (
            f"Equinox {year} off by {diff/3600:.2f}h (> {MAX_ALLOWED_DIFF_SECONDS/3600}h)."  # noqa: E501
        )


def test_equinox_monotonic_refinement():
    # Basic property: successive iterations (recomputing) should not diverge wildly; run multiple calls and check variance
    from statistics import pstdev
    samples = [compute_vernal_equinox(2025) for _ in range(3)]
    # All samples should be identical (deterministic) with current algorithm
    seconds = [s.timestamp() for s in samples]
    assert pstdev(seconds) == 0, "Equinox computation became non-deterministic."

"""
Transitional equinox precision tests.

Goals:
- Provide coarse validation for existing (low-precision) implementation.
- Prepare framework for imminent high-precision Core (VSOP87 + ΔT + nutation).
- Allow CI to show expected xfail until strict tolerance is met.

Once the new precise Core is merged, tighten by:
  1. Removing FALLBACK_TOL.
  2. Enforcing STRICT_TOL directly (≤ 60 s).
  3. Moving reference data fully to tests/data/equinox_reference.json (already supported below).
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
import pytest

from astronomical_watch import compute_vernal_equinox

# Strict target tolerance once precise implementation lands (seconds)
STRICT_TOL = 60  # 1 minute
# Temporary fallback tolerance for legacy simplistic solar algorithm (seconds)
FALLBACK_TOL = 3 * 3600  # 3 hours

# Location of external reference dataset (ISO8601 UTC strings).
DATA_FILE = Path(__file__).parent / "data" / "equinox_reference.json"

# Fallback hard-coded references (rounded to the nearest minute).
# Keep synchronized with DATA_FILE values for overlapping years.
_FALLBACK_REFERENCE = {
    2023: "2023-03-20T21:24:00Z",
    2024: "2024-03-20T03:06:00Z",
    2025: "2025-03-20T09:01:00Z",
    2026: "2026-03-20T14:46:00Z",
    2027: "2027-03-20T20:24:00Z",
    2028: "2028-03-20T02:17:00Z",
    2029: "2029-03-20T08:01:00Z",
    2030: "2030-03-20T13:51:00Z",
}


def _load_reference() -> dict[int, datetime]:
    """
    Load reference equinox datetimes (UTC) from JSON if available; otherwise fallback.

    JSON format (example):
    {
      "2023": "2023-03-20T21:24:00Z",
      "2024": "2024-03-20T03:06:00Z"
    }
    """
    data: dict[str, str]
    if DATA_FILE.is_file():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception as e:  # pragma: no cover - defensive
            pytest.fail(f"Failed to parse {DATA_FILE}: {e}")
    else:
        # Use fallback dictionary
        data = dict(_FALLBACK_REFERENCE)

    parsed: dict[int, datetime] = {}
    for year_str, iso in data.items():
        year = int(year_str)
        # Normalize 'Z' to +00:00 for fromisoformat
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        parsed[year] = dt
    return parsed


REFERENCE = _load_reference()
YEARS_UNDER_TEST = sorted(REFERENCE.keys())


@pytest.mark.parametrize("year", YEARS_UNDER_TEST)
def test_equinox_accuracy_transitional(year: int):
    ref_dt = REFERENCE[year]
    eq = compute_vernal_equinox(year)
    assert eq.tzinfo is not None, "Equinox datetime must be timezone-aware (UTC)."
    assert eq.month == 3 and eq.day in (19, 20, 21), (
        f"Unexpected month/day for equinox candidate: {eq.isoformat()}"
    )
    diff = abs((eq - ref_dt).total_seconds())

    # Pass conditions / transitional logic
    if diff <= STRICT_TOL:
        # Desired final state.
        return
    if diff <= FALLBACK_TOL:
        pytest.xfail(
            f"Legacy low-precision solar algorithm still active: diff={diff:.1f}s (> {STRICT_TOL}s target)."
        )
    pytest.fail(
        f"Equinox {year} diff={diff:.1f}s exceeds fallback tolerance {FALLBACK_TOL}s "
        f"(ref={ref_dt.isoformat()}, got={eq.isoformat()})."
    )


def test_equinox_deterministic_single_year():
    """
    Repeated calls for the same year must be bitwise-stable in time value.
    """
    year = YEARS_UNDER_TEST[0]
    samples = [compute_vernal_equinox(year) for _ in range(3)]
    timestamps = {s.timestamp() for s in samples}
    assert len(timestamps) == 1, "Equinox computation became non-deterministic."


def test_equinox_yearly_monotonic_increase():
    """
    Equinox datetimes must increase strictly by year, and spacing should be roughly one tropical year (~365.24 days).
    We allow a wide window for now: days between successive equinoxes in [365, 366).
    """
    prev_dt = None
    for y in YEARS_UNDER_TEST:
        dt = compute_vernal_equinox(y)
        if prev_dt is not None:
            delta_days = (dt - prev_dt).total_seconds() / 86400.0
            assert 365.0 <= delta_days < 366.0, (
                f"Year spacing out of expected range: {prev_dt.year}->{y} = {delta_days:.4f} days"
            )
            assert dt > prev_dt, "Equinox year sequence not strictly increasing."
        prev_dt = dt


def test_reference_dataset_consistency():
    """
    Ensure internal fallback and JSON (if both available) agree for overlapping years.
    Executes only if JSON file exists.
    """
    if not DATA_FILE.is_file():
        pytest.skip("External reference JSON not present; skipping consistency check.")
    for y, iso in _FALLBACK_REFERENCE.items():
        if y in REFERENCE:
            json_dt = REFERENCE[y]
            fb_dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
            assert json_dt == fb_dt, f"Mismatch for year {y}: JSON={json_dt} fallback={fb_dt}"
