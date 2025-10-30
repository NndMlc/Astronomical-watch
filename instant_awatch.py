# -*- coding: utf-8 -*-
"""
INSTANT Astronomical Watch for Windows
NO tkinter - NO dependencies - JUST WORKS!
Copy this file to Windows and run: python instant_awatch.py
"""
import time
import os
from datetime import datetime, timezone

def astro_time():
    now = datetime.now(timezone.utc)
    
    # Equinox 2025 reference
    eq = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
    
    # Seconds since equinox
    secs = (now - eq).total_seconds()
    
    # Day boundary (23:15:54 UTC)
    boundary = 23*3600 + 15*60 + 54
    adj_secs = secs + boundary
    
    # Convert to components
    total_days = adj_secs / 86400.0
    dies = max(0, int(total_days))
    day_frac = total_days - dies
    
    # miliDies (1/1000 day)
    milides_total = day_frac * 1000.0
    milides = int(milides_total)
    mili_frac = milides_total - milides
    
    # mikroDies (1/1000 miliDies)
    mikro = int(mili_frac * 1000.0)
    
    return dies, milides, mikro, now

def main():
    print("ASTRONOMICAL WATCH - Windows Console")
    print("mikroDies Precision | Press Ctrl+C to exit")
    print()
    
    try:
        while True:
            dies, milides, mikro, utc = astro_time()
            
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("=" * 50)
            print("   ASTRONOMICAL WATCH - MIKRODIET PRECISION")
            print("=" * 50)
            print()
            print(f"  TIME: {dies:03d}.{milides:03d}.{mikro:03d}")
            print("  Dies . miliDies . mikroDies")
            print()
            print(f"  UTC:       {utc.strftime('%H:%M:%S')}")
            print(f"  Dies:      {dies}")
            print(f"  miliDies:  {milides}")
            print(f"  mikroDies: {mikro}")
            print()
            
            # Simple progress
            mili_prog = "#" * (milides // 40) + "-" * (25 - milides // 40)
            mikro_prog = "#" * (mikro // 40) + "-" * (25 - mikro // 40)
            
            print(f"  miliDies  [{mili_prog}] {milides/10:.1f}%")
            print(f"  mikroDies [{mikro_prog}] {mikro/10:.1f}%")
            print()
            print("  Press Ctrl+C to stop")
            print("=" * 50)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nAstronomical Watch stopped!")

if __name__ == "__main__":
    main()