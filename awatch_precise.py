#!/usr/bin/env python3
"""
Astronomical Watch - Tačniji algoritam
Koristi referentni meridijan 168°58'30"W za dan početak
"""
from datetime import datetime, timezone, timedelta
import math

def compute_simple_equinox(year: int) -> datetime:
    """Aproksimativno izračunavanje prolećne ravnodnevnice - poboljšano"""
    # Tačniji datumi za poznate godine
    base_dates = {
        2023: datetime(2023, 3, 20, 21, 24, 20, tzinfo=timezone.utc),  # tačniji
        2024: datetime(2024, 3, 20, 3, 6, 28, tzinfo=timezone.utc),   # tačniji
        2025: datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc),   # tačniji
    }
    
    if year in base_dates:
        return base_dates[year]
    
    # Za ostale godine, linearno ekstrapolišemo
    # Tropska godina ≈ 365.24219 dana
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
    """
    Nađi prvi 'mean solar noon' na referentnom meridijanu nakon ravnodnevnice
    Referentni meridijan: 168°58'30"W = -168.975°
    Mean solar noon na tom meridijanu = 23:15:54 UTC
    """
    # Konstantno UTC vreme za mean solar noon na referentnom meridijanu
    NOON_UTC_HOUR = 23
    NOON_UTC_MINUTE = 15
    NOON_UTC_SECOND = 54
    
    eq_date = equinox.date()
    
    # Kandidat za noon na dan ravnodnevnice
    noon_candidate = datetime(
        eq_date.year, eq_date.month, eq_date.day,
        NOON_UTC_HOUR, NOON_UTC_MINUTE, NOON_UTC_SECOND,
        tzinfo=timezone.utc
    )
    
    # Ako je noon >= ravnodnevnica, to je prvi noon
    if noon_candidate >= equinox:
        return noon_candidate
    
    # Inače, sledeći dan
    return noon_candidate + timedelta(days=1)

def astronomical_time_precise() -> tuple[int, int, float]:
    """Vraća precizno astronomsko vreme kao (day_index, mili_dies, milidi_fraction)"""
    now = datetime.now(timezone.utc)
    year = now.year
    
    current_equinox = compute_simple_equinox(year)
    
    # Ako je pre ravnodnevnice trenutne godine, koristi prethodnu
    if now < current_equinox:
        year -= 1
        current_equinox = compute_simple_equinox(year)
    
    # Nađi prvi noon nakon ravnodnevnice (početak Dana 0)
    first_noon = first_noon_after_equinox(current_equinox)
    
    # Ako je vreme pre prvog noon-a, dan_index = 0
    if now < first_noon:
        # Računaj milidijes od ravnodnevnice
        elapsed_from_eq = now - current_equinox
        total_seconds = elapsed_from_eq.total_seconds()
        
        # Koliko sekundi u danu ima (može biti kraći ako je ravnodnevnica u toku dana)
        day_seconds = (first_noon - current_equinox).total_seconds()
        
        if day_seconds > 0:
            mili_dies = int((total_seconds / day_seconds) * 1000)
            milidi_fraction = ((total_seconds / day_seconds) * 1000) % 1
        else:
            mili_dies = 0
            milidi_fraction = 0.0
            
        return 0, min(mili_dies, 999), milidi_fraction
    
    # Inače, računaj od prvog noon-a
    elapsed_from_first_noon = now - first_noon
    total_seconds = elapsed_from_first_noon.total_seconds()
    
    # Koliko punih dana je prošlo
    day_index = int(total_seconds // 86400) + 1  # +1 jer je Dan 0 bio pre prvog noon-a
    
    # Ostatak sekundi u trenutnom danu
    remainder_seconds = total_seconds % 86400
    
    # miliDies (0-999)
    mili_dies = int((remainder_seconds / 86400) * 1000)
    
    # Frakcija unutar trenutnog miliDies-a za progres bar
    milidi_seconds = remainder_seconds % 86.4  # 86.4 sekunde = 1 miliDies
    milidi_fraction = milidi_seconds / 86.4  # 0.0 - 1.0
    
    return day_index, mili_dies, milidi_fraction

def astronomical_time_display() -> str:
    """Vraća formatovano astronomsko vreme"""
    day_index, mili_dies, _ = astronomical_time_precise()
    return f"{day_index:03d}.{mili_dies:03d}"

def main():
    """Glavna funkcija CLI"""
    try:
        result = astronomical_time_display()
        print(result)
        
        # Debug info
        day_index, mili_dies, milidi_fraction = astronomical_time_precise()
        now = datetime.now(timezone.utc)
        current_equinox = compute_simple_equinox(now.year if now >= compute_simple_equinox(now.year) else now.year - 1)
        first_noon = first_noon_after_equinox(current_equinox)
        
        print(f"Debug:")
        print(f"  Trenutno UTC: {now}")
        print(f"  Ravnodnevnica: {current_equinox}")
        print(f"  Prvi noon: {first_noon}")
        print(f"  Dan {day_index}, miliDies {mili_dies}")
        print(f"  Napredak miliDies-a: {milidi_fraction:.3f} ({milidi_fraction*100:.1f}%)")
        
    except Exception as e:
        print(f"Greška: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())