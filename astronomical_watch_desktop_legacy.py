#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astronomical Watch Desktop Application - Legacy Python Compatible
Compatible with Python 2.7+ and 3.x
"""
import sys
import os

# Add source directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

def check_python_version():
    """Check if Python version is sufficient."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("=" * 60)
        print("ASTRONOMICAL WATCH COMPATIBILITY WARNING")
        print("=" * 60)
        print("Your Python version: {}.{}.{}".format(version.major, version.minor, version.micro))
        print("Recommended: Python 3.6 or higher")
        print("")
        print("The application may not work correctly with older Python versions.")
        print("F-string syntax requires Python 3.6+")
        print("")
        print("Please update Python from: https://python.org")
        print("=" * 60)
        
        try:
            try:
                raw_input("Press Enter to continue anyway, or Ctrl+C to exit...")
            except NameError:
                # Python 3
                input("Press Enter to continue anyway, or Ctrl+C to exit...")
        except KeyboardInterrupt:
            print("\nExiting...")
            return False
    return True

def main():
    """Launch the desktop application."""
    if not check_python_version():
        return 1
        
    try:
        from astronomical_watch.ui.main import main as ui_main
        ui_main()
    except SyntaxError as e:
        print("SYNTAX ERROR:")
        print("Error: " + str(e))
        print("")
        print("This likely means your Python version is too old.")
        print("The application requires Python 3.6+ for f-string support.")
        print("Please update Python from: https://python.org")
        return 1
    except Exception as e:
        print("Error: " + str(e))
        return 1
    return 0

if __name__ == "__main__":
    exit(main())