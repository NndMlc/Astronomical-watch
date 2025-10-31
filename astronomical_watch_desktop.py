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
        from astronomical_watch.ui.main import main as ui_main
        ui_main()
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())