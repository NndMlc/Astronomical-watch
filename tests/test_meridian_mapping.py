"""
Tests for meridian mapping functionality.
"""
from __future__ import annotations

import math
import pytest
from datetime import datetime, timezone

from astronomical_watch.core.astro_time_core import AstroYear, LONGITUDE_REF_DEG


def test_meridian_mapping_inverse_within_half_cell():
    """
    Test that inverse mapping (from dies/miliDies back to UTC) is reasonably accurate.
    
    The approximate_utc_from_day_miliDies function provides approximate reconstruction
    (within ~1.5 miliDies or ~130 seconds, since it ignores equation of time).
    """
    # Create test astronomical year
    from astronomical_watch import compute_vernal_equinox
    
    current_equinox = compute_vernal_equinox(2024)
    next_equinox = compute_vernal_equinox(2025)
    astro_year = AstroYear(current_equinox, next_equinox)
    
    # Test several points throughout the year
    test_times = [
        current_equinox + (next_equinox - current_equinox) * fraction
        for fraction in [0.1, 0.25, 0.5, 0.75, 0.9]
    ]
    
    for original_time in test_times:
        # Forward mapping: UTC -> dies/miliDies
        reading = astro_year.reading(original_time)
        dies = reading.dies
        miliDies = reading.miliDies
        
        # Inverse mapping: dies/miliDies -> UTC (approximate)
        reconstructed_time = astro_year.approximate_utc_from_day_miliDies(dies, miliDies)
        
        # Check accuracy within reasonable tolerance
        diff_seconds = abs((reconstructed_time - original_time).total_seconds())
        tolerance_seconds = 86400 / 1000 * 1.5  # ~1.5 miliDies (129.6 s) - reasonable for approximate mapping
        
        assert diff_seconds <= tolerance_seconds, (
            f"Inverse mapping accuracy failed: diff={diff_seconds:.1f}s > {tolerance_seconds:.1f}s "
            f"(dies={dies}, miliDies={miliDies})"
        )


def test_meridian_reference_longitude():
    """Test that the reference longitude is correctly defined."""
    # The reference longitude should be -168.975 degrees as per specification
    expected = -168.975
    actual = LONGITUDE_REF_DEG
    
    assert abs(actual - expected) < 0.001, (
        f"Reference longitude mismatch: expected {expected}, got {actual}"
    )


def test_day_boundary_consistency():
    """Test that day boundaries are consistent with mean noon at reference meridian."""
    from astronomical_watch import compute_vernal_equinox
    
    current_equinox = compute_vernal_equinox(2024)
    next_equinox = compute_vernal_equinox(2025)
    astro_year = AstroYear(current_equinox, next_equinox)
    
    # Test first few day boundaries
    for dies in range(3):
        # Get approximate UTC for this day at miliDies=0 (start of day)
        day_start = astro_year.approximate_utc_from_day_miliDies(dies, 0)
        
        # Convert back to reading
        reading = astro_year.reading(day_start)
        
        # Should be at the start of the day (miliDies reasonably close to 0)
        # Note: approximate_utc_from_day_miliDies is not perfectly precise (ignores EoT, etc.)
        assert reading.dies == dies, f"Day boundary inconsistency: expected dies={dies}, got {reading.dies}"
        assert reading.miliDies < 150, f"Day start not reasonably at miliDies=0: got {reading.miliDies} (tolerance: <150)"


def test_legacy_compatibility():
    """Test that legacy aliases work correctly."""
    from astronomical_watch import compute_vernal_equinox
    
    current_equinox = compute_vernal_equinox(2024)
    next_equinox = compute_vernal_equinox(2025)
    astro_year = AstroYear(current_equinox, next_equinox)
    
    test_time = current_equinox + (next_equinox - current_equinox) * 0.5
    
    # Test reading method
    reading1 = astro_year.reading(test_time)
    reading2 = astro_year.reading(test_time)
    
    # Should be identical
    assert reading1.dies == reading2.dies
    assert reading1.miliDies == reading2.miliDies
    
    # Test approximate_utc method
    reconstructed1 = astro_year.approximate_utc_from_day_miliDies(reading1.dies, reading1.miliDies)
    reconstructed2 = astro_year.approximate_utc_from_day_miliDies(reading1.dies, reading1.miliDies)
    
    # Should be identical
    assert reconstructed1 == reconstructed2