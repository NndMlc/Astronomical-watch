#!/usr/bin/env python3
"""
Jednostavan astronomical watch CLI
"""
from datetime import datetime, timezone
import math

def simple_astronomical_time():
    """Jednostavna verzija za testiranje"""
    now = datetime.now(timezone.utc)
    
    # Aproksimacija - koristimo kalendarsku godinu kao placeholder
    year = now.year
    
    # Aproksimacija prolećne ravnodnevnice (20. mart)
    equinox_approx = datetime(year, 3, 20, 12, 0, tzinfo=timezone.utc)
    
    if now < equinox_approx:
        year -= 1
        equinox_approx = datetime(year, 3, 20, 12, 0, tzinfo=timezone.utc)
    
    # Broj dana od ravnodnevnice
    elapsed = now - equinox_approx
    day_index = elapsed.days
    
    # Hiljaditini deo dana
    seconds_in_day = elapsed.seconds
    milli_dies = int((seconds_in_day / 86400) * 1000)
    
    return day_index, milli_dies

if __name__ == "__main__":
    day_index, milli_dies = simple_astronomical_time()
    print(f"{day_index:03d}.{milli_dies:03d}")