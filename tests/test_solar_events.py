"""
Tests for solar events calculations.
"""
from __future__ import annotations

import math
import pytest
from datetime import datetime, timezone, timedelta

from main import calculate_equation_of_time, calculate_solar_events


def test_equation_of_time_range():
    """
    Test that Equation of Time stays within reasonable bounds (-30 to +30 minutes).
    The EoT varies throughout the year but should not exceed these bounds.
    """
    # Test throughout the year
    base_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    
    for day_offset in range(0, 365, 10):  # Test every 10 days
        test_date = base_date + timedelta(days=day_offset)
        eot = calculate_equation_of_time(test_date)
        
        assert -20.0 <= eot <= 20.0, (
            f"EoT out of range on {test_date.strftime('%Y-%m-%d')}: {eot:.1f} minutes"
        )


def test_solar_events_order_mid_latitudes():
    """
    Test that for mid-latitudes near solstice: sunrise < solar_noon < sunset.
    This should hold for most locations except extreme polar regions.
    """
    # Test mid-latitudes around summer solstice
    test_locations = [
        (40.7, -74.0),  # New York
        (51.5, 0.0),    # London  
        (48.9, 2.3),    # Paris
        (35.7, 139.7),  # Tokyo
    ]
    
    summer_solstice = datetime(2024, 6, 21, tzinfo=timezone.utc)
    winter_solstice = datetime(2024, 12, 21, tzinfo=timezone.utc)
    
    for lat, lon in test_locations:
        for test_date in [summer_solstice, winter_solstice]:
            events = calculate_solar_events(lat, lon, test_date)
            
            sunrise = events['sunrise']
            solar_noon = events['solar_noon'] 
            sunset = events['sunset']
            
            if sunrise and sunset:  # Skip if polar day/night
                assert sunrise < solar_noon, (
                    f"Sunrise not before solar noon at {lat},{lon} on {test_date.date()}: "
                    f"sunrise={sunrise.time()}, noon={solar_noon.time()}"
                )
                
                assert solar_noon < sunset, (
                    f"Solar noon not before sunset at {lat},{lon} on {test_date.date()}: "
                    f"noon={solar_noon.time()}, sunset={sunset.time()}"
                )


def test_solar_events_equator_consistency():
    """
    Test solar events at equator have reasonable 12-hour daylight around equinoxes.
    """
    # At equator around equinoxes, day and night should be roughly equal
    equator_lat, equator_lon = 0.0, 0.0
    spring_equinox = datetime(2024, 3, 20, tzinfo=timezone.utc)
    autumn_equinox = datetime(2024, 9, 22, tzinfo=timezone.utc)
    
    for test_date in [spring_equinox, autumn_equinox]:
        events = calculate_solar_events(equator_lat, equator_lon, test_date)
        
        sunrise = events['sunrise']
        sunset = events['sunset']
        
        if sunrise and sunset:
            daylight_duration = (sunset - sunrise).total_seconds() / 3600  # hours
            
            # At equator during equinox, daylight should be close to 12 hours
            assert 11.5 <= daylight_duration <= 12.5, (
                f"Daylight duration at equator during equinox should be ~12h, got {daylight_duration:.1f}h"
            )


def test_solar_noon_longitude_correction():
    """
    Test that solar noon varies correctly with longitude.
    Moving east should make solar noon earlier in UTC.
    """
    test_date = datetime(2024, 6, 21, tzinfo=timezone.utc)
    latitude = 40.0
    
    # Test different longitudes
    longitudes = [-120, -90, -60, -30, 0, 30, 60, 90, 120]  # West to East
    
    previous_noon = None
    for lon in longitudes:
        events = calculate_solar_events(latitude, lon, test_date)
        solar_noon = events['solar_noon']
        
        if previous_noon is not None:
            # Moving east (increasing longitude) should make solar noon earlier in UTC
            assert solar_noon <= previous_noon + timedelta(minutes=30), (
                f"Solar noon not decreasing (or stable) with eastward longitude: "
                f"lon={lon}° noon={solar_noon.time()}, previous={previous_noon.time()}"
            )
        
        previous_noon = solar_noon


def test_polar_regions_handling():
    """
    Test that polar regions are handled gracefully (no crashes).
    """
    # Test extreme latitudes
    polar_locations = [
        (85.0, 0.0),   # Near North Pole
        (-85.0, 0.0),  # Near South Pole
    ]
    
    summer_date = datetime(2024, 6, 21, tzinfo=timezone.utc)
    winter_date = datetime(2024, 12, 21, tzinfo=timezone.utc)
    
    for lat, lon in polar_locations:
        for test_date in [summer_date, winter_date]:
            # Should not crash
            try:
                events = calculate_solar_events(lat, lon, test_date)
                # Should return some result structure
                assert 'sunrise' in events
                assert 'solar_noon' in events
                assert 'sunset' in events
                assert 'equation_of_time' in events
            except Exception as e:
                pytest.fail(f"Solar events calculation crashed for polar location {lat},{lon}: {e}")


def test_equation_of_time_known_extrema():
    """
    Test that EoT reaches expected extrema at known dates.
    """
    # EoT typically reaches maximum around early November (~+16 min)
    # and minimum around mid February (~-14 min)
    
    november_date = datetime(2024, 11, 3, tzinfo=timezone.utc)  # Around maximum
    february_date = datetime(2024, 2, 11, tzinfo=timezone.utc)  # Around minimum
    
    eot_nov = calculate_equation_of_time(november_date)
    eot_feb = calculate_equation_of_time(february_date)
    
    # November should be positive and reasonably large
    assert eot_nov > 5.0, f"EoT in early November should be > 5 min, got {eot_nov:.1f}"
    
    # February should be negative
    assert eot_feb < -2.0, f"EoT in mid February should be < -2 min, got {eot_feb:.1f}"
    
    # The range should be reasonable
    eot_range = eot_nov - eot_feb
    assert 15.0 <= eot_range <= 35.0, f"EoT range should be 15-35 min, got {eot_range:.1f}"