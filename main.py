"""
Main entry point for the Astronomical Watch widget.
Supports launch via `python -m main`
"""
from __future__ import annotations

import os
import json
import math
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Tuple

from astronomical_watch import astronomical_now, compute_vernal_equinox
from fastapi import FastAPI
from routes import equinox  # importuj novi modul

app = FastAPI()

app.include_router(equinox.router, prefix="/api")

def get_config_dir() -> Path:
    """Get the proper configuration directory for caching."""
    if os.name == 'nt':  # Windows
        config_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'astronomical_watch'
    else:  # Unix-like (Linux, macOS)
        config_dir = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')) / 'astronomical_watch'

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def load_or_create_equinox_cache() -> dict:
    """Load equinox cache from file or create a new one."""
    cache_file = get_config_dir() / 'equinox_cache.json'

    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                cache = json.load(f)
            print(f"Loaded equinox cache from {cache_file}")
            return cache
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load cache file {cache_file}: {e}")
            print("Creating new cache...")

    # Create new cache with current year and neighboring years
    current_year = datetime.now().year
    cache = {}

    for year in range(current_year - 1, current_year + 2):
        try:
            equinox = compute_vernal_equinox(year)
            cache[str(year)] = equinox.isoformat()
            print(f"Computed equinox for {year}: {equinox.isoformat()}")
        except Exception as e:
            print(f"Warning: Failed to compute equinox for {year}: {e}")

    # Save cache
    try:
        with open(cache_file, 'w') as f:
            json.dump(cache, f, indent=2)
        print(f"Saved equinox cache to {cache_file}")
    except IOError as e:
        print(f"Warning: Failed to save cache: {e}")

    return cache


def get_location_from_env() -> Tuple[float, float]:
    """Get location coordinates from environment variables."""
    try:
        lat = float(os.environ.get('ASTRON_WATCH_LAT', '0.0'))
        lon = float(os.environ.get('ASTRON_WATCH_LON', '0.0'))

        # Validate coordinates
        if not (-90 <= lat <= 90):
            print(f"Warning: Invalid latitude {lat}, using 0.0")
            lat = 0.0
        if not (-180 <= lon <= 180):
            print(f"Warning: Invalid longitude {lon}, using 0.0")
            lon = 0.0

        return lat, lon
    except (ValueError, TypeError):
        print("Warning: Invalid coordinates in environment variables, using (0.0, 0.0)")
        return 0.0, 0.0


def calculate_equation_of_time(dt: datetime) -> float:
    """
    Calculate the Equation of Time in minutes.
    This is a simplified calculation for demonstration.

    Args:
        dt: datetime for which to calculate EoT

    Returns:
        Equation of Time in minutes
    """
    # Get day of year
    day_of_year = dt.timetuple().tm_yday

    # More accurate simplified EoT calculation
    # Based on the traditional formula combining eccentricity and obliquity effects

    # Convert to radians based on day of year
    B = 2 * math.pi * (day_of_year - 81) / 365.0

    # EoT formula in minutes (Meeus approximation)
    eot = (9.87 * math.sin(2 * B) -
           7.53 * math.cos(B) -
           1.5 * math.sin(B))

    return eot


def calculate_solar_events(lat: float, lon: float, date: datetime) -> dict:
    """
    Calculate solar events (sunrise, solar noon, sunset) for a given location and date.
    This is a simplified calculation.

    Args:
        lat: Latitude in degrees
        lon: Longitude in degrees
        date: Date for calculation

    Returns:
        Dictionary with solar event times
    """
    # Solar declination (simplified)
    day_of_year = date.timetuple().tm_yday
    declination = 23.45 * math.sin(math.radians((360 / 365.25) * (day_of_year - 81)))
    declination_rad = math.radians(declination)
    lat_rad = math.radians(lat)

    # Hour angle for sunrise/sunset (simplified)
    try:
        cos_hour_angle = -math.tan(lat_rad) * math.tan(declination_rad)

        # Check for polar day/night
        if cos_hour_angle > 1:
            # Polar night
            return {
                'sunrise': None,
                'solar_noon': date.replace(hour=12, minute=0, second=0, microsecond=0, tzinfo=timezone.utc),
                'sunset': None,
                'equation_of_time': calculate_equation_of_time(date)
            }
        elif cos_hour_angle < -1:
            # Polar day
            return {
                'sunrise': None,
                'solar_noon': date.replace(hour=12, minute=0, second=0, microsecond=0, tzinfo=timezone.utc),
                'sunset': None,
                'equation_of_time': calculate_equation_of_time(date)
            }

        hour_angle = math.acos(cos_hour_angle)
        hour_angle_hours = math.degrees(hour_angle) / 15.0  # Convert to hours

        # Solar noon (simplified - at longitude correction)
        # This is when the sun is highest at this longitude
        solar_noon_utc = 12.0 - lon / 15.0  # Basic longitude correction

        # Create solar noon datetime
        solar_noon_day_offset = 0
        if solar_noon_utc < 0:
            solar_noon_utc += 24
            solar_noon_day_offset = -1
        elif solar_noon_utc >= 24:
            solar_noon_utc -= 24
            solar_noon_day_offset = 1

        solar_noon = (date + timedelta(days=solar_noon_day_offset)).replace(
            hour=int(solar_noon_utc),
            minute=int((solar_noon_utc % 1) * 60),
            second=0, microsecond=0, tzinfo=timezone.utc
        )

        # Sunrise and sunset relative to solar noon
        sunrise_utc = solar_noon_utc - hour_angle_hours
        sunset_utc = solar_noon_utc + hour_angle_hours

        sunrise_day_offset = solar_noon_day_offset
        sunset_day_offset = solar_noon_day_offset

        if sunrise_utc < 0:
            sunrise_utc += 24
            sunrise_day_offset -= 1
        elif sunrise_utc >= 24:
            sunrise_utc -= 24
            sunrise_day_offset += 1

        if sunset_utc < 0:
            sunset_utc += 24
            sunset_day_offset -= 1
        elif sunset_utc >= 24:
            sunset_utc -= 24
            sunset_day_offset += 1

        sunrise = (date + timedelta(days=sunrise_day_offset)).replace(
            hour=int(sunrise_utc),
            minute=int((sunrise_utc % 1) * 60),
            second=0, microsecond=0, tzinfo=timezone.utc
        )

        sunset = (date + timedelta(days=sunset_day_offset)).replace(
            hour=int(sunset_utc),
            minute=int((sunset_utc % 1) * 60),
            second=0, microsecond=0, tzinfo=timezone.utc
        )

        return {
            'sunrise': sunrise,
            'solar_noon': solar_noon,
            'sunset': sunset,
            'equation_of_time': calculate_equation_of_time(date)
        }

    except (ValueError, ZeroDivisionError):
        # Fallback for edge cases
        solar_noon = date.replace(hour=12, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
        return {
            'sunrise': solar_noon - timedelta(hours=6),
            'solar_noon': solar_noon,
            'sunset': solar_noon + timedelta(hours=6),
            'equation_of_time': calculate_equation_of_time(date)
        }


def display_astronomical_watch():
    """Display the astronomical watch information."""
    print("=" * 60)
    print("ASTRONOMICAL WATCH")
    print("=" * 60)

    # Load cache
    load_or_create_equinox_cache()

    # Get location
    lat, lon = get_location_from_env()
    print(f"\nLocation: {lat:.3f}°, {lon:.3f}° (from environment variables)")

    # Get current astronomical time
    now = datetime.now(timezone.utc)
    astro_time = astronomical_now(now)

    print(f"\nCurrent UTC time: {now.isoformat()}")
    print(f"Astronomical timestamp: {astro_time['timestamp']}")
    print(f"Equinox epoch: {astro_time['equinox_epoch'].isoformat()}")
    print(f"Day index: {astro_time['day_index']}")
    print(f"Milli-day: {astro_time['milli_day']}")
    print(f"Year progress: {astro_time['raw_fraction']:.3f}")

    # Solar events
    solar_events = calculate_solar_events(lat, lon, now.replace(hour=0, minute=0, second=0, microsecond=0))
    print(f"\n--- Solar Events (for location {lat:.1f}°, {lon:.1f}°) ---")

    if solar_events['sunrise']:
        print(f"Sunrise: {solar_events['sunrise'].strftime('%H:%M:%S UTC')}")
    else:
        print("Sunrise: N/A (polar night/day)")

    print(f"Solar noon: {solar_events['solar_noon'].strftime('%H:%M:%S UTC')}")

    if solar_events['sunset']:
        print(f"Sunset: {solar_events['sunset'].strftime('%H:%M:%S UTC')}")
    else:
        print("Sunset: N/A (polar night/day)")

    print(f"Equation of Time: {solar_events['equation_of_time']:.1f} minutes")

    print("\n" + "=" * 60)
    print("Widget running successfully!")
    print("Set ASTRON_WATCH_LAT and ASTRON_WATCH_LON environment variables for your location.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        display_astronomical_watch()
    except Exception as e:
        print(f"Error in astronomical watch: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
