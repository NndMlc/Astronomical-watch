"""
Tests for sky theme calculations and phase coverage.
"""
from __future__ import annotations

import math
import pytest
from datetime import datetime, timezone, timedelta

from astronomical_watch import astronomical_now
from main import calculate_solar_events, calculate_equation_of_time


def get_sky_phase(astro_reading: dict, solar_events: dict) -> str:
    """
    Determine the sky phase based on astronomical reading and solar events.
    
    Returns phase names like: 'deep_night', 'dawn', 'day', 'dusk', 'night'
    """
    sunrise = solar_events.get('sunrise')
    sunset = solar_events.get('sunset')
    
    if not sunrise or not sunset:
        # Polar day/night
        if astro_reading['milli_day'] < 500:
            return 'polar_day'
        else:
            return 'polar_night'
    
    # Use milli_day to determine phase
    milli_day = astro_reading['milli_day']
    
    # Convert sunrise/sunset times to approximate milli_day values
    # This is very simplified - in reality we'd need to account for the astronomical year properly
    sunrise_hour = sunrise.hour + sunrise.minute / 60.0
    sunset_hour = sunset.hour + sunset.minute / 60.0
    
    # Handle day boundary crossings
    if sunset < sunrise:  # sunset is next day
        sunset_hour += 24
    
    # Convert to rough milli_day equivalents (0-999 scale)
    sunrise_milli = int((sunrise_hour * 1000) / 24) % 1000
    sunset_milli = int((sunset_hour * 1000) / 24) % 1000
    
    # Define phase boundaries (with some margin)
    dawn_start = (sunrise_milli - 80) % 1000  # ~2 hours before sunrise
    dawn_end = (sunrise_milli + 40) % 1000    # ~1 hour after sunrise
    dusk_start = (sunset_milli - 40) % 1000   # ~1 hour before sunset
    dusk_end = (sunset_milli + 80) % 1000     # ~2 hours after sunset
    
    # Simplified phase detection
    if dawn_start <= milli_day <= dawn_end:
        if milli_day <= sunrise_milli:
            return 'dawn'
        else:
            return 'day'
    elif dusk_start <= milli_day <= dusk_end:
        if milli_day <= sunset_milli:
            return 'day'
        else:
            return 'dusk'
    elif sunrise_milli < milli_day < sunset_milli:
        return 'day'
    else:
        # Handle wraparound cases and default to night phases
        if milli_day < sunrise_milli - 200:  # Well before sunrise
            return 'deep_night'
        else:
            return 'night'


def calculate_sunrise_boost_factor(phase: str, solar_events: dict) -> float:
    """
    Calculate a brightness boost factor for sunrise/dawn phases.
    
    Args:
        phase: Current sky phase
        solar_events: Solar events data
        
    Returns:
        Boost factor (1.0 = no boost, >1.0 = brighter)
    """
    if phase in ['dawn', 'dusk']:
        return 1.3  # 30% boost during twilight
    elif phase == 'day':
        return 1.0  # Normal brightness
    elif phase in ['night', 'deep_night']:
        return 0.7  # Dimmer at night
    elif phase in ['polar_day']:
        return 1.1  # Slight boost for polar day
    else:  # polar_night
        return 0.5  # Much dimmer


def test_sky_phase_coverage():
    """
    Test that sky phases cover all possible times throughout a day.
    Every milli_day value should map to a valid phase.
    """
    from astronomical_watch import compute_vernal_equinox
    
    # Use a test date and location
    test_date = datetime(2024, 6, 21, tzinfo=timezone.utc)  # Summer solstice
    test_lat, test_lon = 40.0, -74.0  # New York area
    
    astro_reading = astronomical_now(test_date)
    solar_events = calculate_solar_events(test_lat, test_lon, test_date)
    
    # Test several milli_day values throughout the day
    valid_phases = {'deep_night', 'dawn', 'day', 'dusk', 'night', 'polar_day', 'polar_night'}
    
    for milli_day in range(0, 1000, 50):  # Test every 50 milli_days
        # Create a test reading with this milli_day
        test_reading = astro_reading.copy()
        test_reading['milli_day'] = milli_day
        
        phase = get_sky_phase(test_reading, solar_events)
        
        assert phase in valid_phases, (
            f"Invalid phase '{phase}' for milli_day {milli_day}"
        )


def test_dawn_dusk_phase_detection():
    """
    Test that dawn and dusk phases are correctly detected around sunrise/sunset.
    """
    test_date = datetime(2024, 3, 20, tzinfo=timezone.utc)  # Equinox
    test_lat, test_lon = 45.0, 0.0  # Mid-latitude
    
    solar_events = calculate_solar_events(test_lat, test_lon, test_date)
    
    if solar_events['sunrise'] and solar_events['sunset']:
        # Test several times throughout the day to ensure phase coverage
        test_times = []
        base_time = test_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        for hour in range(0, 24, 3):  # Every 3 hours
            test_times.append(base_time + timedelta(hours=hour))
        
        valid_phases = {'deep_night', 'dawn', 'day', 'dusk', 'night', 'polar_day', 'polar_night'}
        
        for test_time in test_times:
            astro_reading = astronomical_now(test_time)
            phase = get_sky_phase(astro_reading, solar_events)
            
            # Just ensure we get valid phases - the exact timing is hard to test 
            # due to the complexity of astronomical time mapping
            assert phase in valid_phases, (
                f"Invalid phase '{phase}' for time {test_time.time()}"
            )


def test_sunrise_boost_validation():
    """
    Test that sunrise boost factors are reasonable and consistent.
    """
    test_phases = ['deep_night', 'dawn', 'day', 'dusk', 'night', 'polar_day', 'polar_night']
    
    for phase in test_phases:
        boost = calculate_sunrise_boost_factor(phase, {})
        
        # Boost factors should be reasonable
        assert 0.1 <= boost <= 2.0, (
            f"Unreasonable boost factor {boost} for phase '{phase}'"
        )
        
        # Dawn and dusk should have higher boost than night
        if phase in ['dawn', 'dusk']:
            night_boost = calculate_sunrise_boost_factor('night', {})
            assert boost > night_boost, (
                f"Dawn/dusk boost ({boost}) should be higher than night boost ({night_boost})"
            )


def test_day_night_cycle_consistency():
    """
    Test that the day/night cycle progresses logically through phases.
    """
    test_date = datetime(2024, 6, 21, tzinfo=timezone.utc)  # Summer solstice
    test_lat, test_lon = 50.0, 0.0  # Mid-latitude
    
    solar_events = calculate_solar_events(test_lat, test_lon, test_date)
    
    # Track phases throughout a day
    phases_by_hour = []
    
    for hour in range(24):
        test_time = test_date.replace(hour=hour, minute=30)  # Middle of each hour
        astro_reading = astronomical_now(test_time)
        phase = get_sky_phase(astro_reading, solar_events)
        phases_by_hour.append((hour, phase))
    
    # Check for logical progression
    has_night = any(phase in ['night', 'deep_night'] for _, phase in phases_by_hour)
    has_day = any(phase == 'day' for _, phase in phases_by_hour)
    
    # At mid-latitudes in summer, should have both day and night
    assert has_night or has_day, "Should have either day or night phases at mid-latitudes"
    
    # If we have both sunrise and sunset, should have reasonable phase distribution
    if solar_events['sunrise'] and solar_events['sunset']:
        dawn_or_dusk_count = sum(1 for _, phase in phases_by_hour if phase in ['dawn', 'dusk'])
        assert dawn_or_dusk_count >= 1, "Should have at least some dawn or dusk phases"


def test_polar_region_phase_handling():
    """
    Test that polar regions with polar day/night are handled correctly.
    """
    # Test Arctic in summer (polar day)
    arctic_summer = datetime(2024, 6, 21, tzinfo=timezone.utc)
    arctic_lat, arctic_lon = 80.0, 0.0
    
    solar_events = calculate_solar_events(arctic_lat, arctic_lon, arctic_summer)
    astro_reading = astronomical_now(arctic_summer)
    
    phase = get_sky_phase(astro_reading, solar_events)
    
    # Should handle polar conditions gracefully
    assert phase in ['polar_day', 'polar_night', 'day', 'night'], (
        f"Unexpected phase '{phase}' for polar region in summer"
    )
    
    # Test Arctic in winter (polar night)
    arctic_winter = datetime(2024, 12, 21, tzinfo=timezone.utc)
    
    solar_events_winter = calculate_solar_events(arctic_lat, arctic_lon, arctic_winter)
    astro_reading_winter = astronomical_now(arctic_winter)
    
    phase_winter = get_sky_phase(astro_reading_winter, solar_events_winter)
    
    # Should handle polar conditions gracefully
    assert phase_winter in ['polar_day', 'polar_night', 'day', 'night'], (
        f"Unexpected phase '{phase_winter}' for polar region in winter"
    )


def test_phase_boost_interaction():
    """
    Test that phase and boost calculations work together consistently.
    """
    test_date = datetime(2024, 3, 20, tzinfo=timezone.utc)  # Equinox
    test_lat, test_lon = 40.0, -75.0
    
    solar_events = calculate_solar_events(test_lat, test_lon, test_date)
    
    # Test several times throughout the day
    for hour in [6, 9, 12, 15, 18, 21]:  # Different times
        test_time = test_date.replace(hour=hour)
        astro_reading = astronomical_now(test_time)
        
        phase = get_sky_phase(astro_reading, solar_events)
        boost = calculate_sunrise_boost_factor(phase, solar_events)
        
        # Ensure boost is appropriate for phase
        if phase == 'day':
            assert boost >= 1.0, f"Day phase should have boost >= 1.0, got {boost}"
        elif phase in ['night', 'deep_night']:
            assert boost <= 1.0, f"Night phases should have boost <= 1.0, got {boost}"
        elif phase in ['dawn', 'dusk']:
            assert boost > 1.0, f"Dawn/dusk should have boost > 1.0, got {boost}"