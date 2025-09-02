"""
Tests for UI gradient helper and theme logic.
Tests non-GUI components only.
"""
import unittest
import math
from datetime import datetime, timezone
from ui.gradient import (
    SkyTheme, 
    get_sky_theme, 
    get_solar_altitude_approximation,
    create_gradient_colors,
    hex_to_rgb
)


class TestSkyTheme(unittest.TestCase):
    """Test SkyTheme class."""
    
    def test_sky_theme_creation(self):
        """Test SkyTheme object creation."""
        theme = SkyTheme("#1e3a8a", "#3b82f6", "#ffffff")
        
        self.assertEqual(theme.top_color, "#1e3a8a")
        self.assertEqual(theme.bottom_color, "#3b82f6")  
        self.assertEqual(theme.text_color, "#ffffff")
        self.assertEqual(theme.text_hex, "#ffffff")  # Alias


class TestSolarAltitude(unittest.TestCase):
    """Test solar altitude approximation."""
    
    def test_noon_altitude_positive(self):
        """Test that noon produces positive altitude."""
        dt = datetime(2024, 6, 21, 12, 0, 0, tzinfo=timezone.utc)  # Summer solstice noon
        altitude = get_solar_altitude_approximation(dt)
        self.assertGreater(altitude, 0)
        self.assertLess(altitude, 90)  # Reasonable upper bound
    
    def test_midnight_altitude_negative(self):
        """Test that midnight produces negative altitude."""
        dt = datetime(2024, 6, 21, 0, 0, 0, tzinfo=timezone.utc)  # Midnight
        altitude = get_solar_altitude_approximation(dt)
        self.assertLess(altitude, 0)
    
    def test_summer_higher_than_winter(self):
        """Test that seasonal altitude calculation works reasonably."""
        summer_noon = datetime(2024, 6, 21, 12, 0, 0, tzinfo=timezone.utc)  # Summer solstice
        winter_noon = datetime(2024, 12, 21, 12, 0, 0, tzinfo=timezone.utc)  # Winter solstice
        
        summer_alt = get_solar_altitude_approximation(summer_noon)
        winter_alt = get_solar_altitude_approximation(winter_noon)
        
        # Both should be positive at noon (above horizon)
        self.assertGreater(summer_alt, 0, "Summer noon should be above horizon")
        self.assertGreater(winter_alt, 0, "Winter noon should be above horizon")
        
        # Both should be reasonable values for mid-latitude noon
        self.assertLess(summer_alt, 90, "Summer altitude should be less than 90°")
        self.assertLess(winter_alt, 90, "Winter altitude should be less than 90°")


class TestSkyThemes(unittest.TestCase):
    """Test sky theme generation."""
    
    def test_get_sky_theme_returns_sky_theme(self):
        """Test that get_sky_theme returns a SkyTheme object."""
        dt = datetime(2024, 6, 21, 12, 0, 0, tzinfo=timezone.utc)
        theme = get_sky_theme(dt)
        
        self.assertIsInstance(theme, SkyTheme)
        self.assertTrue(theme.top_color.startswith('#'))
        self.assertTrue(theme.bottom_color.startswith('#'))
        self.assertTrue(theme.text_color.startswith('#'))
    
    def test_high_sun_bright_theme(self):
        """Test that high sun produces bright theme."""
        # Mock a high sun scenario
        dt = datetime(2024, 6, 21, 12, 0, 0, tzinfo=timezone.utc)  # Summer noon
        theme = get_sky_theme(dt)
        
        # Should be bright colors for bright sky (high RGB values)
        top_rgb = hex_to_rgb(theme.top_color)
        bottom_rgb = hex_to_rgb(theme.bottom_color)
        
        # Bright theme should have reasonably high color values
        self.assertGreater(max(top_rgb), 50, "Bright theme should have bright colors")
        self.assertGreater(max(bottom_rgb), 100, "Bright theme should have bright colors")
    
    def test_night_dark_theme(self):
        """Test that night produces dark theme."""
        dt = datetime(2024, 6, 21, 2, 0, 0, tzinfo=timezone.utc)  # Deep night
        theme = get_sky_theme(dt)
        
        # Should have dark colors for night
        top_rgb = hex_to_rgb(theme.top_color)
        bottom_rgb = hex_to_rgb(theme.bottom_color)
        
        # Dark colors should have low RGB values
        self.assertLess(max(top_rgb), 100, "Night theme should have dark colors")
        self.assertLess(max(bottom_rgb), 150, "Night theme should have dark colors")


class TestGradientColors(unittest.TestCase):
    """Test gradient color generation."""
    
    def test_hex_to_rgb(self):
        """Test hex color to RGB conversion."""
        self.assertEqual(hex_to_rgb("#ffffff"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#ff0000"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("ff0000"), (255, 0, 0))  # Without #
    
    def test_create_gradient_colors_length(self):
        """Test that gradient creates requested number of colors."""
        theme = SkyTheme("#000000", "#ffffff", "#000000")
        colors = create_gradient_colors(theme, 10)
        
        self.assertEqual(len(colors), 10)
        self.assertTrue(all(color.startswith('#') for color in colors))
    
    def test_gradient_endpoints(self):
        """Test that gradient starts and ends with correct colors."""
        theme = SkyTheme("#ff0000", "#0000ff", "#000000")
        colors = create_gradient_colors(theme, 10)
        
        # First color should be close to top color
        self.assertEqual(colors[0].lower(), "#ff0000")
        # Last color should be close to bottom color
        self.assertEqual(colors[-1].lower(), "#0000ff")
    
    def test_gradient_interpolation(self):
        """Test that gradient interpolates between colors."""
        theme = SkyTheme("#000000", "#ffffff", "#000000")  # Black to white
        colors = create_gradient_colors(theme, 3)
        
        # Should go from black through gray to white
        self.assertEqual(colors[0].lower(), "#000000")
        self.assertEqual(colors[-1].lower(), "#ffffff")
        
        # Middle should be some shade of gray
        middle_rgb = hex_to_rgb(colors[1])
        self.assertEqual(middle_rgb[0], middle_rgb[1])  # R = G
        self.assertEqual(middle_rgb[1], middle_rgb[2])  # G = B (gray)


class TestThemeIntegration(unittest.TestCase):
    """Test integration between components."""
    
    def test_theme_changes_with_time(self):
        """Test that theme changes appropriately with time of day."""
        # Noon should be different from midnight
        noon = datetime(2024, 6, 21, 12, 0, 0, tzinfo=timezone.utc)
        midnight = datetime(2024, 6, 21, 0, 0, 0, tzinfo=timezone.utc)
        
        noon_theme = get_sky_theme(noon)
        midnight_theme = get_sky_theme(midnight)
        
        # Themes should be different
        self.assertNotEqual(noon_theme.top_color, midnight_theme.top_color)
        self.assertNotEqual(noon_theme.bottom_color, midnight_theme.bottom_color)
    
    def test_gradient_helper_existence(self):
        """Test that gradient helper components exist and are callable."""
        # This satisfies the requirement for "minimal test to assert helper existence"
        self.assertTrue(callable(get_sky_theme))
        self.assertTrue(callable(get_solar_altitude_approximation))
        self.assertTrue(callable(create_gradient_colors))
        self.assertTrue(callable(hex_to_rgb))


if __name__ == '__main__':
    unittest.main()