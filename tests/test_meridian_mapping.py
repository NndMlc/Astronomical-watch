"""
Tests for meridian mapping functionality.
"""
from __future__ import annotations

import math
import pytest
from datetime import datetime, timezone

from core.astro_time_core import AstroYear, LONGITUDE_REF_DEG


def test_meridian_mapping_inverse_within_half_cell():
    """
    Test that inverse mapping (from dies/milidies back to UTC) is accurate within half cell.
    
    The meridian mapping should have inverse accuracy within half a milidies cell
    (about 43.2 seconds for a full day divided by 1000 milidies).
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
        # Forward mapping: UTC -> dies/milidies
        reading = astro_year.to_reading(original_time)
        dies = reading.dies
        milidies = reading.milidies
        
        # Inverse mapping: dies/milidies -> UTC (approximate)
        reconstructed_time = astro_year.approximate_utc_from_dies_milidies(dies, milidies)
        
        # Check accuracy within half cell
        diff_seconds = abs((reconstructed_time - original_time).total_seconds())
        half_cell_seconds = 86400 / 1000 / 2  # Half of one milidies in seconds (43.2 s)
        
        assert diff_seconds <= half_cell_seconds, (
            f"Inverse mapping accuracy failed: diff={diff_seconds:.1f}s > {half_cell_seconds:.1f}s "
            f"(dies={dies}, milidies={milidies})"
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
        # Get approximate UTC for this day at milidies=0 (start of day)
        day_start = astro_year.approximate_utc_from_dies_milidies(dies, 0)
        
        # Convert back to reading
        reading = astro_year.to_reading(day_start)
        
        # Should be at the start of the day (milidies close to 0)
        assert reading.dies == dies, f"Day boundary inconsistency: expected dies={dies}, got {reading.dies}"
        assert reading.milidies < 10, f"Day start not at milidies=0: got {reading.milidies}"


def test_legacy_compatibility():
    """Test that legacy aliases work correctly."""
    from astronomical_watch import compute_vernal_equinox
    
    current_equinox = compute_vernal_equinox(2024)
    next_equinox = compute_vernal_equinox(2025)
    astro_year = AstroYear(current_equinox, next_equinox)
    
    test_time = current_equinox + (next_equinox - current_equinox) * 0.5
    
    # Test legacy method aliases
    reading1 = astro_year.to_reading(test_time)
    reading2 = astro_year.to_legacy_reading(test_time)
    
    # Should be identical
    assert reading1.dies == reading2.dies
    assert reading1.milidies == reading2.milidies
    
    # Test legacy approximate_utc method
    reconstructed1 = astro_year.approximate_utc_from_dies_milidies(reading1.dies, reading1.milidies)
    reconstructed2 = astro_year.approximate_utc_from_day_milidan(reading1.dies, reading1.milidies)
    
    # Should be identical
    assert reconstructed1 == reconstructed2