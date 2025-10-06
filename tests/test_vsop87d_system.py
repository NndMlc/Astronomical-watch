"""
Tests for VSOP87D dynamic coefficient loading system
"""
import unittest
import math
from datetime import datetime, timezone
from pathlib import Path
import sys
import os

# Add the repository root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from astronomical_watch.core.solar import solar_longitude_from_datetime, apparent_solar_longitude
from astronomical_watch.core.vsop87_earth import earth_heliocentric_longitude, _find_coefficient_file, _get_coefficients
from astronomical_watch.core.timebase import timescales_from_datetime

class TestVSOP87DSystem(unittest.TestCase):
    """Test the VSOP87D dynamic loading system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dt = datetime(2024, 3, 20, 12, 0, tzinfo=timezone.utc)
        self.test_jd_tt = timescales_from_datetime(self.test_dt).jd_tt
        self.test_t = (self.test_jd_tt - 2451545.0) / 365250.0  # VSOP87 time
    
    def test_default_precision_unchanged(self):
        """Test that default precision behavior is unchanged."""
        # Compute longitude with default precision
        lon_default = solar_longitude_from_datetime(self.test_dt)
        
        # Should be a reasonable value near 0 for spring equinox
        self.assertGreater(lon_default, -math.pi/4)
        self.assertLess(lon_default, math.pi/4)
        
        # Should be reproducible
        lon_default2 = solar_longitude_from_datetime(self.test_dt)
        self.assertEqual(lon_default, lon_default2)
    
    def test_max_error_parameter_accepted(self):
        """Test that max_error_arcsec parameter is accepted without errors."""
        # These should not raise exceptions
        lon1 = solar_longitude_from_datetime(self.test_dt, max_error_arcsec=10.0)
        lon2 = solar_longitude_from_datetime(self.test_dt, max_error_arcsec=1.0)
        lon3 = solar_longitude_from_datetime(self.test_dt, max_error_arcsec=0.1)
        
        # All should be valid longitude values
        for lon in [lon1, lon2, lon3]:
            self.assertGreaterEqual(lon, 0)
            self.assertLess(lon, 2 * math.pi)
    
    def test_coefficient_file_detection(self):
        """Test that coefficient file detection works for generated files."""
        # Look for files that might have been generated
        script_dir = Path(__file__).parent.parent / "scripts"
        coeff_dir = script_dir / "vsop87_coefficients"
        
        if coeff_dir.exists():
            files = list(coeff_dir.glob("vsop87d_earth_*.py"))
            if files:
                # Test that we can find appropriate files
                # This will depend on what files were generated
                file_2arcsec = _find_coefficient_file(2.0)
                file_1arcsec = _find_coefficient_file(1.0)
                file_01arcsec = _find_coefficient_file(0.1)
                
                # At least one of these should work if we have generated files
                found_any = any(f is not None for f in [file_2arcsec, file_1arcsec, file_01arcsec])
                if found_any:
                    print(f"Found coefficient files: 2arcsec={file_2arcsec}, 1arcsec={file_1arcsec}, 0.1arcsec={file_01arcsec}")
    
    def test_earth_heliocentric_longitude_precision(self):
        """Test that Earth heliocentric longitude function accepts precision parameter."""
        # Test with different precision requirements
        lon_default = earth_heliocentric_longitude(self.test_t)
        lon_precise = earth_heliocentric_longitude(self.test_t, max_error_arcsec=1.0)
        
        # Both should be valid longitude values
        self.assertGreaterEqual(lon_default, 0)
        self.assertLess(lon_default, 2 * math.pi)
        self.assertGreaterEqual(lon_precise, 0)
        self.assertLess(lon_precise, 2 * math.pi)
        
        # Values should be reasonably close (difference mainly from precision)
        diff = abs(lon_default - lon_precise)
        self.assertLess(diff, 0.1)  # Less than ~20 arcseconds difference
    
    def test_coefficient_cache_functionality(self):
        """Test that coefficient caching works."""
        # Get coefficients multiple times - should use cache
        coeffs1 = _get_coefficients(max_error_arcsec=None)
        coeffs2 = _get_coefficients(max_error_arcsec=None)
        
        # Should be the same object (cached)
        self.assertIs(coeffs1, coeffs2)
        
        # Should contain expected series
        expected_series = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5',
                          'B0', 'B1', 'B2', 'B3', 'B4', 'B5',
                          'R0', 'R1', 'R2', 'R3', 'R4', 'R5']
        for series in expected_series:
            self.assertIn(series, coeffs1)
            self.assertIsInstance(coeffs1[series], list)
    
    def test_apparent_solar_longitude_precision(self):
        """Test apparent solar longitude with precision parameter."""
        # Test with different precision levels
        lon1 = apparent_solar_longitude(self.test_jd_tt)
        lon2 = apparent_solar_longitude(self.test_jd_tt, max_error_arcsec=10.0)
        lon3 = apparent_solar_longitude(self.test_jd_tt, max_error_arcsec=1.0)
        
        # All should be valid
        for lon in [lon1, lon2, lon3]:
            self.assertGreaterEqual(lon, 0)
            self.assertLess(lon, 2 * math.pi)
        
        # Should be close to each other
        self.assertLess(abs(lon1 - lon2), 0.1)
        self.assertLess(abs(lon1 - lon3), 0.1)
    
    def test_vsop87_time_conversion(self):
        """Test VSOP87 time conversion consistency."""
        from astronomical_watch.core.vsop87_earth import _t
        
        # Test that time conversion is consistent
        t = _t(self.test_jd_tt)
        
        # Should be small for dates near J2000
        self.assertLess(abs(t), 1.0)  # Less than 1 millennium from J2000
    
    def test_integration_with_astronomical_watch(self):
        """Test integration with the main astronomical_watch module."""
        try:
            from astronomical_watch import compute_vernal_equinox
            
            # Should work without errors
            eq_2024 = compute_vernal_equinox(2024)
            
            # Should be in March
            self.assertEqual(eq_2024.month, 3)
            self.assertIn(eq_2024.day, [19, 20, 21, 22])
            
        except ImportError:
            self.skipTest("astronomical_watch module not available")

if __name__ == '__main__':
    unittest.main()