"""
Test ΔT values from Espenak & Meeus polynomials.
Validates against expected values for selected years.
"""
import unittest
from astro.timescales import delta_t_espenak_meeus


class TestTimescalesDeltaT(unittest.TestCase):
    """Test ΔT calculations."""
    
    def test_delta_t_1980(self):
        """Test ΔT for 1980."""
        delta_t = delta_t_espenak_meeus(1980.0)
        # Expected value around 50.5 seconds
        self.assertAlmostEqual(delta_t, 50.5, delta=2.0)
    
    def test_delta_t_2000(self):
        """Test ΔT for 2000."""
        delta_t = delta_t_espenak_meeus(2000.0)
        # Expected value around 63.8 seconds
        self.assertAlmostEqual(delta_t, 63.8, delta=1.0)
    
    def test_delta_t_2025(self):
        """Test ΔT for 2025."""
        delta_t = delta_t_espenak_meeus(2025.0)
        # Expected value using polynomial: 62.92 + 0.32217*25 + 0.005589*25^2
        expected = 62.92 + 0.32217 * 25 + 0.005589 * 25 * 25
        self.assertAlmostEqual(delta_t, expected, delta=0.1)
    
    def test_delta_t_ranges(self):
        """Test ΔT for different time periods."""
        # Modern era (2005-2050)
        delta_t_2020 = delta_t_espenak_meeus(2020.0)
        self.assertTrue(60.0 < delta_t_2020 < 80.0)
        
        # Historical period (1900-1920)
        delta_t_1910 = delta_t_espenak_meeus(1910.0)
        self.assertTrue(-5.0 < delta_t_1910 < 20.0)
        
        # Earlier historical period (1800-1860) 
        delta_t_1830 = delta_t_espenak_meeus(1830.0)
        self.assertTrue(5.0 < delta_t_1830 < 25.0)
    
    def test_delta_t_continuity(self):
        """Test that ΔT is reasonably continuous across boundaries."""
        # Test around year 2000 boundary (1986-2005 vs 2005-2050)
        delta_t_2004 = delta_t_espenak_meeus(2004.9)
        delta_t_2005 = delta_t_espenak_meeus(2005.1)
        
        # Should be close (within 5 seconds)
        diff = abs(delta_t_2005 - delta_t_2004)
        self.assertLess(diff, 5.0)
        
        # Test around 1986 boundary
        delta_t_1985 = delta_t_espenak_meeus(1985.9)
        delta_t_1986 = delta_t_espenak_meeus(1986.1)
        
        # Should be reasonably close (within 10 seconds)
        diff = abs(delta_t_1986 - delta_t_1985)
        self.assertLess(diff, 10.0)
    
    def test_delta_t_monotonicity_modern(self):
        """Test that ΔT generally increases in modern era."""
        # In the modern era (1900-2050), ΔT should generally increase
        years = [1980, 1990, 2000, 2010, 2020, 2030]
        delta_ts = [delta_t_espenak_meeus(year) for year in years]
        
        # Check that the trend is generally increasing
        # (allowing for some small decreases due to polynomial fitting)
        overall_increase = delta_ts[-1] - delta_ts[0]
        self.assertGreater(overall_increase, 10.0)  # Should increase by at least 10s over 50 years


if __name__ == '__main__':
    unittest.main()