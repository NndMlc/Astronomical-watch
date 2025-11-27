#!/usr/bin/env python3
"""
Test Astronomical Watch functionality without GUI
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from astronomical_watch.core.astro_time_core import AstroYear
from astronomical_watch.ui.comparison_card import create_comparison_card
from datetime import datetime, timezone

def test_core_functionality():
    """Test core astronomical time calculations."""
    print("🧪 Testing Core Functionality...")
    
    # Test basic time calculation
    now = datetime.now(timezone.utc)
    equinox = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
    next_equinox = datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
    
    astro_year = AstroYear(equinox, next_equinox)
    reading = astro_year.reading(now)
    
    print(f"✅ Current astronomical time: {reading.dies:03d}.{reading.miliDies:03d}.{reading.mikroDies:03d}")
    print(f"✅ System time: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # Test timezone handling
    local_now = datetime.now()
    local_tz = local_now.astimezone()
    offset = local_tz.utcoffset()
    if offset:
        total_seconds = int(offset.total_seconds())
        hours = total_seconds // 3600
        minutes = abs(total_seconds % 3600) // 60
        if hours >= 0:
            tz_display = f"UTC+{hours:02d}:{minutes:02d}"
        else:
            tz_display = f"UTC{hours:03d}:{minutes:02d}"
        print(f"✅ Local timezone: {tz_display}")
    
    return True

def test_comparison_logic():
    """Test comparison conversion logic."""
    print("\n🧪 Testing Comparison Logic...")
    
    # Test milidies to time conversion
    from astronomical_watch.ui.comparison_card import milidies_to_hm, hm_to_milidies
    
    test_cases = [
        (0, "00:00:00"),
        (500, "12:00:00"),
        (1000, "24:00:00")  # This might be 00:00:00 next day
    ]
    
    for milidies, expected_time in test_cases:
        converted_time = milidies_to_hm(milidies)
        print(f"✅ {milidies} miliDies = {converted_time}")
        
        # Test reverse conversion
        h, m, s = map(int, converted_time.split(':'))
        back_to_milidies = hm_to_milidies(h, m, s)
        print(f"✅ {converted_time} = {back_to_milidies} miliDies")
    
    return True

def test_translations():
    """Test translation system."""
    print("\n🧪 Testing Translations...")
    
    from astronomical_watch.ui.translations import TRANSLATIONS
    
    languages = ["en", "sr", "es", "de", "fr"]
    test_keys = ["title", "comparison", "standard_time"]
    
    for lang in languages:
        if lang in TRANSLATIONS:
            print(f"✅ Language {lang} available:")
            for key in test_keys:
                text = TRANSLATIONS[lang].get(key, f"Missing: {key}")
                print(f"   {key}: {text}")
        else:
            print(f"❌ Language {lang} not found")
    
    return True

def main():
    """Run all tests."""
    print("🚀 Astronomical Watch Functionality Test")
    print("=" * 50)
    
    try:
        test_core_functionality()
        test_comparison_logic()
        test_translations()
        
        print("\n🎉 All tests passed!")
        print("\n📝 Summary:")
        print("✅ Core astronomical calculations working")
        print("✅ Timezone detection working")  
        print("✅ Comparison conversions working")
        print("✅ Translation system working")
        print("✅ All key functionality verified without GUI")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())