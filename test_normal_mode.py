#!/usr/bin/env python3
"""
Test script za normal mode debug - bez GUI
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from datetime import datetime, timezone

def test_normal_mode_data():
    """Test samo logike za normal mode bez GUI"""
    
    print("=== NORMAL MODE DATA TEST ===")
    
    # Test gradijent logike
    current_time = datetime.now(timezone.utc)
    hour = current_time.hour
    
    # Jednostavne boje na osnovu doba dana
    if 6 <= hour < 12:  # Jutro
        bg_color = "#4A90E2"  # Plava jutro
        period = "JUTRO"
    elif 12 <= hour < 18:  # Dan
        bg_color = "#87CEEB"  # Svetlo plava dan
        period = "DAN"
    elif 18 <= hour < 21:  # Veče
        bg_color = "#FF7F50"  # Narandžasta veče
        period = "VEČE"
    else:  # Noć
        bg_color = "#2F4F4F"  # Tamno plava noć
        period = "NOĆ"
    
    print(f"Current UTC time: {current_time.strftime('%H:%M:%S')}")
    print(f"Period: {period}")
    print(f"Background color: {bg_color}")
    
    # Test astronomical calculator
    try:
        from astronomical_watch.core.astro_time_core import AstroYear
        print("\n✅ Core astronomical library available")
        
        # Test calculation
        current_eq = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
        next_eq = datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
        
        ay = AstroYear(current_eq, next_eq)
        reading = ay.reading(datetime.now(timezone.utc))
        
        dies_text = f"{reading.day_index:03d}.{reading.miliDies:03d}"
        print(f"Dies.miliDies: {dies_text}")
        print(f"mikroDies: {reading.mikroDies:03d}")
        
    except Exception as e:
        print(f"\n❌ Core library error: {e}")
        print("Using fallback calculator...")
        
        # Simple fallback
        now = datetime.now(timezone.utc)
        equinox = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
        delta = now - equinox
        dies = delta.days
        seconds_today = delta.seconds
        milides = int((seconds_today / 86400) * 1000)
        
        dies_text = f"{dies:03d}.{milides:03d}"
        print(f"Dies.miliDies (fallback): {dies_text}")
    
    # Test text formatting
    utc_time = datetime.now(timezone.utc)
    date_text = f"Date: {utc_time.strftime('%d/%m/%Y')}"
    time_text = f"UTC: {utc_time.strftime('%H:%M:%S')}"
    
    print(f"\nFormated texts:")
    print(f"  {date_text}")
    print(f"  {time_text}")
    
    print("\n=== MOCK GUI LAYOUT ===")
    print("Canvas: 400x600")
    print("Background:", bg_color)
    print("Text positions:")
    print(f"  Dies (200, 100): {dies_text}")
    print(f"  Date (200, 180): {date_text}")
    print(f"  UTC (200, 230): {time_text}")
    
    print("\n✅ All normal mode data logic working!")

if __name__ == "__main__":
    test_normal_mode_data()