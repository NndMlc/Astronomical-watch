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