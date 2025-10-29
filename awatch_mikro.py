#!/usr/bin/env python3
"""
Astronomical Watch - sa mikroDies podrškom
Prikazuje vreme u DDD.mmm.µµµ formatu
"""
from datetime import datetime, timezone, timedelta
import math

def compute_simple_equinox(year: int) -> datetime:
    """Aproksimativno izračunavanje prolećne ravnodnevnice - poboljšano"""
    base_dates = {
        2023: datetime(2023, 3, 20, 21, 24, 20, tzinfo=timezone.utc),
        2024: datetime(2024, 3, 20, 3, 6, 28, tzinfo=timezone.utc),
        2025: datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc),
    }
    
    if year in base_dates:
        return base_dates[year]
    
    tropical_year_seconds = 365.24219 * 86400
    
    if year < 2023:
        ref_year = 2023
        ref_equinox = base_dates[2023]
        years_diff = ref_year - year
        estimated_equinox = ref_equinox - timedelta(seconds=years_diff * tropical_year_seconds)
    else:
        ref_year = 2025
        ref_equinox = base_dates[2025]
        years_diff = year - ref_year
        estimated_equinox = ref_equinox + timedelta(seconds=years_diff * tropical_year_seconds)
    
    return estimated_equinox

def first_noon_after_equinox(equinox: datetime) -> datetime:
    """Nađi prvi mean solar noon na referentnom meridijanu nakon ravnodnevnice"""
    NOON_UTC_HOUR = 23
    NOON_UTC_MINUTE = 15
    NOON_UTC_SECOND = 54
    
    eq_date = equinox.date()
    
    noon_candidate = datetime(
        eq_date.year, eq_date.month, eq_date.day,
        NOON_UTC_HOUR, NOON_UTC_MINUTE, NOON_UTC_SECOND,
        tzinfo=timezone.utc
    )
    
    if noon_candidate >= equinox:
        return noon_candidate
    
    return noon_candidate + timedelta(days=1)

def astronomical_time_with_mikro() -> tuple[int, int, int, float]:
    """Vraća (day_index, mili_dies, mikro_dies, mikro_fraction)"""
    now = datetime.now(timezone.utc)
    year = now.year
    
    current_equinox = compute_simple_equinox(year)
    
    if now < current_equinox:
        year -= 1
        current_equinox = compute_simple_equinox(year)
    
    first_noon = first_noon_after_equinox(current_equinox)
    
    if now < first_noon:
        elapsed_from_eq = now - current_equinox
        total_seconds = elapsed_from_eq.total_seconds()
        
        day_seconds = (first_noon - current_equinox).total_seconds()
        
        if day_seconds > 0:
            total_mikro_dies = 1000000
            current_mikro_dies = (total_seconds / day_seconds) * total_mikro_dies
            
            mili_dies = int(current_mikro_dies // 1000)
            mikro_dies_in_current_mili = int(current_mikro_dies % 1000)
            mikro_dies_fraction = (current_mikro_dies % 1000) % 1
        else:
            mili_dies = 0
            mikro_dies_in_current_mili = 0
            mikro_dies_fraction = 0.0
            
        day_index = 0
        mili_dies = min(mili_dies, 999)
    else:
        elapsed_from_first_noon = now - first_noon
        total_seconds = elapsed_from_first_noon.total_seconds()
        
        day_index = int(total_seconds // 86400) + 1
        remainder_seconds = total_seconds % 86400
        
        mikro_dies_per_second = 1000000 / 86400
        current_mikro_dies = remainder_seconds * mikro_dies_per_second
        
        mili_dies = int(current_mikro_dies // 1000)
        mikro_dies_in_current_mili = int(current_mikro_dies % 1000)
        mikro_dies_fraction = (current_mikro_dies % 1000) % 1
    
    return day_index, mili_dies, mikro_dies_in_current_mili, mikro_dies_fraction

def main():
    """Glavna funkcija"""
    try:
        day_index, mili_dies, mikro_dies, mikro_fraction = astronomical_time_with_mikro()
        
        # Osnovni format
        basic_format = f"{day_index:03d}.{mili_dies:03d}"
        
        # Prošireni format sa mikroDies
        extended_format = f"{day_index:03d}.{mili_dies:03d}.{mikro_dies:03d}"
        
        print("Astronomical Watch sa mikroDies")
        print("=" * 40)
        print(f"Osnovno vreme:    {basic_format}")
        print(f"Sa mikroDies:     {extended_format}")
        print(f"mikroDies progres: {mikro_fraction:.3f} ({mikro_fraction*100:.1f}%)")
        print()
        print("Objašnjenje:")
        print(f"  {day_index:03d} = Dies od ravnodnevnice")
        print(f"  {mili_dies:03d} = miliDies (1/1000 Dies-a)")
        print(f"  {mikro_dies:03d} = mikroDies (1/1000 miliDies-a)")
        print()
        print("Jedinice:")
        print("  1 Dies = 1,000 miliDies = 1,000,000 mikroDies")
        print("  1 miliDies = 86.4 sekunde")
        print("  1 mikroDies = 0.0864 sekunde = 86.4 ms")
        
        now = datetime.now(timezone.utc)
        print(f"\nUTC: {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} UTC")
        
    except Exception as e:
        print(f"Greška: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())