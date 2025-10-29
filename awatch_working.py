#!/usr/bin/env python3
"""
Astronomical Watch - Funkcionalni CLI
Koristi osnovnu logiku za računanje astronomskog vremena u DDD.mmm formatu
"""
from datetime import datetime, timezone, timedelta
import math

def compute_simple_equinox(year: int) -> datetime:
    """Aproksimativno izračunavanje prolećne ravnodnevnice"""
    # Koristi poznate datume za neke godine kao aproksimaciju
    base_dates = {
        2023: datetime(2023, 3, 20, 21, 24, tzinfo=timezone.utc),
        2024: datetime(2024, 3, 20, 3, 6, tzinfo=timezone.utc),
        2025: datetime(2025, 3, 20, 9, 1, tzinfo=timezone.utc),
    }
    
    if year in base_dates:
        return base_dates[year]
    
    # Za ostale godine, koristi aproksimaciju (20. mart oko podneva)
    return datetime(year, 3, 20, 12, 0, tzinfo=timezone.utc)

def astronomical_time_now() -> str:
    """Vraća trenutno astronomsko vreme u DDD.mmm formatu"""
    now = datetime.now(timezone.utc)
    year = now.year
    
    # Nađi trenutnu ravnodnevnicu
    current_equinox = compute_simple_equinox(year)
    
    # Ako je vreme pre ravnodnevnice, koristi prethodnu godinu
    if now < current_equinox:
        year -= 1
        current_equinox = compute_simple_equinox(year)
    
    # Izračunaj broj dana od ravnodnevnice
    elapsed = now - current_equinox
    total_seconds = elapsed.total_seconds()
    
    # Dan indeks (Dies)
    day_index = int(total_seconds // 86400)
    
    # Ostatak sekundi u trenutnom danu
    remainder_seconds = total_seconds % 86400
    
    # miliDies (hiljaditine dela dana)
    mili_dies = int((remainder_seconds / 86400) * 1000)
    
    return f"{day_index:03d}.{mili_dies:03d}"

def main():
    """Glavna funkcija CLI"""
    try:
        result = astronomical_time_now()
        print(result)
    except Exception as e:
        print(f"Greška: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())