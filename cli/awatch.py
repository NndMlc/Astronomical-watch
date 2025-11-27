#!/usr/bin/env python
"""CLI tool (MIT licensed) printing astronomical time as DDD.mmm"""
from __future__ import annotations
import sys
import os
from datetime import datetime, timezone

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_dir = os.path.join(project_root, "src")
sys.path.insert(0, src_dir)

from astronomical_watch.core.astro_time_core import AstroYear
from astronomical_watch.core.equinox import compute_vernal_equinox

def main():
    try:
        now = datetime.now(timezone.utc)
        current_year = now.year
        
        # Get current equinox
        equinox = compute_vernal_equinox(current_year)
        if now < equinox:
            equinox = compute_vernal_equinox(current_year - 1)
            
        # Calculate astronomical time
        astro_year = AstroYear(equinox)
        reading = astro_year.reading(now)
        
        print(f"{reading.dies:03d}.{reading.miliDies:03d}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
