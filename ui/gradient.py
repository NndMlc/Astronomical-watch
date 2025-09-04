"""
Shared gradient helper for sky-based themes.
Computes dynamic sky gradients based on astronomical data (solar position, time, etc.)
"""
from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Tuple
from core.solar import solar_longitude_from_datetime


class SkyTheme:
    """Represents a sky theme with gradient colors and text colors."""
    
    def __init__(self, top_color: str, bottom_color: str, text_color: str):
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.text_color = text_color
        self.text_hex = text_color  # Alias for consistency with problem statement


def get_solar_altitude_approximation(dt: datetime) -> float:
    """
    Approximate solar altitude for theme computation.
    This is a simplified calculation for UI purposes.
    Returns altitude in degrees (negative = below horizon).
    """
    # Get solar longitude (position in orbit)
    solar_lon = solar_longitude_from_datetime(dt)
    
    # Convert solar longitude to seasonal factor for declination
    # Solar longitude 0 = vernal equinox, π/2 = summer solstice, π = autumnal equinox, 3π/2 = winter solstice
    # Declination varies from +23.5° (summer) to -23.5° (winter)
    declination = 23.5 * math.sin(solar_lon + math.pi/2)  # Peak at summer solstice
    
    # Get hour of day (0-24)
    hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    
    # Hour angle: 0 at solar noon, ±π at midnight
    hour_angle = (hour - 12) * 15 * math.pi / 180  # Convert hours to radians
    
    # Simplified altitude calculation (assume latitude = 45°N for demo)
    latitude = 45.0 * math.pi / 180  # 45°N in radians
    declination_rad = declination * math.pi / 180
    
    # Solar altitude formula: sin(altitude) = sin(lat) * sin(dec) + cos(lat) * cos(dec) * cos(hour_angle)
    sin_altitude = (math.sin(latitude) * math.sin(declination_rad) + 
                   math.cos(latitude) * math.cos(declination_rad) * math.cos(hour_angle))
    
    # Clamp to avoid domain errors
    sin_altitude = max(-1.0, min(1.0, sin_altitude))
    altitude_rad = math.asin(sin_altitude)
    altitude_degrees = altitude_rad * 180 / math.pi
    
    return altitude_degrees


def get_sky_theme(dt: datetime = None) -> SkyTheme:
    """
    Get current sky theme based on astronomical data.
    Returns a SkyTheme with appropriate gradient and text colors.
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    
    altitude = get_solar_altitude_approximation(dt)
    
    # Define theme colors based on solar altitude
    if altitude > 50:  # High sun - bright blue sky
        return SkyTheme(
            top_color="#1e3a8a",     # Deep blue
            bottom_color="#3b82f6",   # Bright blue
            text_color="#ffffff"      # White text
        )
    elif altitude > 20:  # Moderate sun - light blue sky  
        return SkyTheme(
            top_color="#2563eb",      # Medium blue
            bottom_color="#60a5fa",   # Light blue
            text_color="#000000"      # Black text
        )
    elif altitude > 0:   # Low sun - dawn/dusk colors
        return SkyTheme(
            top_color="#7c3aed",      # Purple
            bottom_color="#f59e0b",   # Orange/yellow
            text_color="#ffffff"      # White text
        )
    elif altitude > -10: # Civil twilight - darker
        return SkyTheme(
            top_color="#1e1b4b",      # Dark purple
            bottom_color="#7c2d12",   # Dark orange
            text_color="#ffffff"      # White text
        )
    else:  # Night - dark sky
        return SkyTheme(
            top_color="#0f172a",      # Very dark blue
            bottom_color="#1e293b",   # Dark slate
            text_color="#e2e8f0"      # Light gray text
        )


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_gradient_colors(theme: SkyTheme, steps: int = 256) -> list[str]:
    """
    Create a list of hex colors representing a gradient from top to bottom.
    Returns `steps` colors interpolated between top_color and bottom_color.
    """
    top_rgb = hex_to_rgb(theme.top_color)
    bottom_rgb = hex_to_rgb(theme.bottom_color)
    
    colors = []
    for i in range(steps):
        factor = i / (steps - 1)  # 0.0 to 1.0
        
        # Interpolate each RGB component
        r = int(top_rgb[0] + (bottom_rgb[0] - top_rgb[0]) * factor)
        g = int(top_rgb[1] + (bottom_rgb[1] - top_rgb[1]) * factor)
        b = int(top_rgb[2] + (bottom_rgb[2] - top_rgb[2]) * factor)
        
        # Convert back to hex
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        colors.append(hex_color)
    
    return colors


__all__ = [
    'SkyTheme',
    'get_sky_theme', 
    'get_solar_altitude_approximation',
    'create_gradient_colors',
    'hex_to_rgb'
]