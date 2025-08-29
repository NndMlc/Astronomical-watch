"""
Basic tests for equinox precision functionality.
Tests analytic results, internet fetch fallback, and precision comparison.
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from services.equinox_service import (
    get_vernal_equinox, get_vernal_equinox_datetime, check_all_methods,
    compare_methods, clear_cache
)
from solar.equinox_precise import compute_vernal_equinox_precise, validate_equinox_solution
from astronomical_watch import compute_vernal_equinox


class TestEquinoxPrecisionBasic(unittest.TestCase):
    """Basic tests for precise equinox functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Clear cache before each test
        clear_cache()
    
    def test_analytic_result_in_march_window(self):
        """Test that analytic result falls in expected March window (18-22)."""
        for year in [2023, 2024, 2025]:
            with self.subTest(year=year):
                dt = compute_vernal_equinox_precise(year)
                
                # Should be in March
                self.assertEqual(dt.month, 3)
                
                # Should be in reasonable day range
                self.assertGreaterEqual(dt.day, 18)
                self.assertLessEqual(dt.day, 22)
                
                # Should be in UTC
                self.assertEqual(dt.tzinfo, timezone.utc)
    
    def test_analytic_solution_validation(self):
        """Test that analytic solutions are astronomically valid."""
        for year in [2024, 2025]:
            with self.subTest(year=year):
                dt = compute_vernal_equinox_precise(year)
                
                # Should pass validation with tight tolerance
                self.assertTrue(validate_equinox_solution(dt, tolerance_deg=0.01))
    
    def test_analytic_differs_from_approx(self):
        """Test that analytic result differs from approx by >20 seconds."""
        for year in [2023, 2024, 2025]:
            with self.subTest(year=year):
                dt_precise = compute_vernal_equinox_precise(year)
                dt_approx = compute_vernal_equinox(year)
                
                diff_seconds = abs((dt_precise - dt_approx).total_seconds())
                
                # Should differ by more than 20 seconds (showing improvement)
                self.assertGreater(diff_seconds, 20.0)
                
                # But should not differ by more than 3 hours (sanity check)
                self.assertLess(diff_seconds, 3 * 3600.0)
    
    @patch('services.equinox_service.fetch_equinox_datetime')
    @patch('services.equinox_service.is_fetch_configured')
    def test_internet_fetch_fallback_to_analytic(self, mock_configured, mock_fetch):
        """Test internet fetch fallback path chooses analytic."""
        # Mock internet fetch as configured but failing
        mock_configured.return_value = True
        mock_fetch.return_value = None  # Simulate fetch failure
        
        result = get_vernal_equinox(2024, prefer_order=("internet", "analytic", "approx"))
        
        # Should fall back to analytic
        self.assertEqual(result["precision"], "analytic")
        self.assertFalse(result["cached"])
        
        # Should have reasonable uncertainty
        self.assertLess(result["uncertainty_s"], 60.0)  # Better than 1 minute
    
    @patch('services.equinox_service.fetch_equinox_datetime')
    @patch('services.equinox_service.is_fetch_configured')  
    def test_internet_method_when_available(self, mock_configured, mock_fetch):
        """Test internet method when mock data is available."""
        # Mock internet fetch as successful
        mock_configured.return_value = True
        mock_dt = datetime(2024, 3, 20, 3, 6, 14, tzinfo=timezone.utc)
        mock_fetch.return_value = mock_dt
        
        result = get_vernal_equinox(2024, prefer_order=("internet", "analytic", "approx"))
        
        # Should use internet result
        self.assertEqual(result["precision"], "internet") 
        self.assertEqual(result["datetime"], mock_dt)
    
    def test_service_facade_datetime_extraction(self):
        """Test that service facade properly extracts datetime."""
        dt = get_vernal_equinox_datetime(2024, prefer_order=("analytic", "approx"))
        
        # Should return datetime object
        self.assertIsInstance(dt, datetime)
        self.assertEqual(dt.tzinfo, timezone.utc)
        self.assertEqual(dt.month, 3)
    
    def test_analytic_method_repeatability(self):
        """Test that analytic method gives consistent results."""
        # Run multiple times
        results = []
        for _ in range(3):
            dt = compute_vernal_equinox_precise(2024)
            results.append(dt)
        
        # All results should be identical (within 1 second tolerance)
        for i in range(1, len(results)):
            diff_sec = abs((results[i] - results[0]).total_seconds())
            self.assertLess(diff_sec, 2.0)  # Stable to < 2s tolerance
    
    def test_service_comparison_functionality(self):
        """Test service method comparison functionality."""
        comparison = compare_methods(2024)
        
        self.assertIn("successful_methods", comparison)
        self.assertIn("results", comparison)
        
        # Should have at least analytic and approx methods working
        results = comparison["results"]
        self.assertTrue(results["analytic"]["success"])
        self.assertTrue(results["approx"]["success"])
    
    def test_cache_functionality_basic(self):
        """Test basic cache functionality."""
        year = 2024
        
        # First call - should not be cached
        result1 = get_vernal_equinox(year, prefer_order=("analytic", "approx"))
        self.assertFalse(result1["cached"])
        
        # Second call - should be cached
        result2 = get_vernal_equinox(year, prefer_order=("analytic", "approx"))
        self.assertTrue(result2["cached"])
        
        # Results should be identical
        self.assertEqual(result1["utc"], result2["utc"])
        self.assertEqual(result1["precision"], result2["precision"])
    
    def test_prefer_order_respected(self):
        """Test that preference order is respected."""
        # Force approx method first
        result = get_vernal_equinox(2024, prefer_order=("approx", "analytic"))
        self.assertEqual(result["precision"], "approx")
        
        clear_cache()
        
        # Force analytic method first
        result = get_vernal_equinox(2024, prefer_order=("analytic", "approx"))
        self.assertEqual(result["precision"], "analytic")
    
    @patch('services.equinox_service.is_fetch_configured')
    def test_no_network_required(self, mock_configured):
        """Test that tests can run without network access."""
        # Mock network as not configured
        mock_configured.return_value = False
        
        # Should still work with analytic + approx
        result = get_vernal_equinox(2024, prefer_order=("internet", "analytic", "approx"))
        
        # Should fall back to analytic (skipping internet)
        self.assertEqual(result["precision"], "analytic")


if __name__ == '__main__':
    unittest.main()
