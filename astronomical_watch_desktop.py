#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astronomical Watch Desktop Application
"""
import sys
import os

# Add source directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

def main():
    """Launch the desktop application."""
    try:
        # Set application icon if available
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        
        icon_path = os.path.join(current_dir, "icons", "astronomical_watch.ico")
        if os.path.exists(icon_path):
            try:
                root.iconbitmap(icon_path)
            except Exception as e:
                print(f"Could not load icon: {e}")
                # Continue without icon
        
        from astronomical_watch.ui.main import main as ui_main
        ui_main()
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())