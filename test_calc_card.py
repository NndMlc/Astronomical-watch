#!/usr/bin/env python3
"""Test calculation card directly"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Starting calculation card test...")

try:
    import tkinter as tk
    print("✓ Tkinter imported")
    
    from astronomical_watch.ui.calculation_card import CalculationCard
    print("✓ CalculationCard imported")
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    print("✓ Root window created")
    
    card = CalculationCard(master=root, lang="en")
    print("✓ CalculationCard instantiated")
    
    # Wait a bit for location to load
    root.after(2000, lambda: print("⏰ 2 seconds passed"))
    root.after(3000, root.quit)  # Exit after 3 seconds
    
    print("Starting mainloop...")
    root.mainloop()
    
    print("✓ Test completed successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
