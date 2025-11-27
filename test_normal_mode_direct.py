#!/usr/bin/env python3
"""
Direct test of Normal Mode to debug UI issues.
"""

import os
import sys
import tkinter as tk
from datetime import datetime, timezone

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from astronomical_watch.ui.normal_mode import create_normal_mode
from astronomical_watch.ui.gradient import get_sky_theme

def test_normal_mode():
    print("🚀 Starting Normal Mode direct test...")
    
    # Create root window
    root = tk.Tk()
    root.title("Normal Mode Direct Test")
    root.geometry("800x600")
    
    # Test theme
    theme = get_sky_theme()
    print(f"🎨 Theme test: {theme.top_color} → {theme.bottom_color}")
    
    def on_back():
        print("👈 Back button pressed")
        root.quit()
        
    def on_language():
        print("🌍 Language button pressed")
    
    try:
        # Create Normal Mode
        normal_mode = create_normal_mode(root, on_back, on_language)
        print("✅ Normal Mode created successfully")
        
        # Start main loop
        print("🔄 Starting main loop...")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error creating Normal Mode: {e}")
        import traceback
        traceback.print_exc()
    
    print("🏁 Test completed")

if __name__ == "__main__":
    test_normal_mode()