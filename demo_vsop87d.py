#!/usr/bin/env python3
"""
Demonstration of the VSOP87D Dynamic Coefficient Loading System

This script demonstrates the new precision-configurable VSOP87D system
and shows how different accuracy requirements affect the results.
"""

import sys
import os
from datetime import datetime, timezone

# Add repository to path
sys.path.insert(0, os.path.dirname(__file__))

from core.solar import solar_longitude_from_datetime, apparent_solar_longitude
from core.vsop87_earth import _find_coefficient_file
from core.timebase import timescales_from_datetime
from astronomical_watch import compute_vernal_equinox

def rad_to_arcsec(rad):
    """Convert radians to arcseconds."""
    return rad * 206264.806247096

def main():
    print("VSOP87D Dynamic Coefficient Loading System Demonstration")
    print("=" * 60)
    
    # Test date: Spring equinox 2024
    test_dt = datetime(2024, 3, 20, 12, 0, tzinfo=timezone.utc)
    print(f"Test date: {test_dt.isoformat()}")
    print()
    
    # Test different precision levels
    print("Solar Longitude with Different Precision Requirements:")
    print("-" * 55)
    
    precisions = [None, 60.0, 10.0, 5.0, 1.0, 0.1]
    results = []
    
    for precision in precisions:
        if precision is None:
            lon = solar_longitude_from_datetime(test_dt)
            desc = "Default"
        else:
            lon = solar_longitude_from_datetime(test_dt, max_error_arcsec=precision)
            desc = f"{precision:4.1f} arcsec"
        
        results.append((desc, lon))
        coeff_file = _find_coefficient_file(precision) if precision else "Built-in"
        coeff_file_name = coeff_file.name if hasattr(coeff_file, 'name') else str(coeff_file)
        
        print(f"{desc:12} | {lon:12.8f} rad | {coeff_file_name}")
    
    print()
    print("Differences from Default:")
    print("-" * 30)
    
    default_lon = results[0][1]
    for desc, lon in results[1:]:
        diff_arcsec = rad_to_arcsec(abs(lon - default_lon))
        print(f"{desc:12} | {diff_arcsec:8.3f} arcsec")
    
    print()
    
    # Test coefficient file detection
    print("Available Coefficient Files:")
    print("-" * 30)
    
    test_precisions = [100.0, 50.0, 20.0, 10.0, 5.0, 2.0, 1.0, 0.5, 0.1]
    for prec in test_precisions:
        file_path = _find_coefficient_file(prec)
        if file_path:
            print(f"{prec:6.1f} arcsec: {file_path.name}")
        else:
            print(f"{prec:6.1f} arcsec: No suitable file")
    
    print()
    
    # Test equinox computation
    print("Equinox Computation Test:")
    print("-" * 25)
    
    years = [2023, 2024, 2025]
    for year in years:
        try:
            eq = compute_vernal_equinox(year)
            print(f"{year}: {eq.isoformat()}")
        except Exception as e:
            print(f"{year}: Error - {e}")
    
    print()
    
    # Test apparent solar longitude directly
    print("Direct VSOP87 Test:")
    print("-" * 18)
    
    ts = timescales_from_datetime(test_dt)
    jd_tt = ts.jd_tt
    
    # Test with different precisions
    lon_default = apparent_solar_longitude(jd_tt)
    lon_precise = apparent_solar_longitude(jd_tt, max_error_arcsec=1.0)
    
    print(f"Default precision:  {lon_default:.8f} rad")
    print(f"1 arcsec precision: {lon_precise:.8f} rad")
    print(f"Difference:         {rad_to_arcsec(abs(lon_default - lon_precise)):.3f} arcsec")
    
    print()
    print("System test completed successfully!")

if __name__ == "__main__":
    main()