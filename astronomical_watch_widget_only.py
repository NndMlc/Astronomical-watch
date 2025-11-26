#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astronomical Watch Widget - Direct Launch
Automatically shows the floating widget on desktop
"""
import sys
import os

# Add source directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

def check_python_version():
    """Check Python version compatibility."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("⚠️  Warning: Python 3.6+ recommended for full compatibility")
        return False
    return True

def main():
    """Launch widget directly."""
    print("=" * 50)
    print(" ASTRONOMICAL WATCH DESKTOP WIDGET")
    print("=" * 50)
    print()
    
    if not check_python_version():
        print("⚠️  Some features may not work with older Python versions")
        print()
    
    print("Starting floating widget...")
    print()
    print("Widget features:")
    print("- 140x70 borderless overlay")
    print("- Dies.miliDies astronomical time")
    print("- YellowGreen progress bar")
    print("- Right-click for menu")
    print("- Double-click for Normal Mode")
    print("- Drag to move")
    print()
    
    try:
        import tkinter as tk
        from astronomical_watch.ui.widget import AstronomicalWidgetMode
        
        # Create root window (hidden)
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        # Set application icon if available
        icon_path = os.path.join(current_dir, "icons", "astronomical_watch.ico")
        if os.path.exists(icon_path):
            try:
                root.iconbitmap(icon_path)
                print(f"✅ Icon loaded: {icon_path}")
            except tk.TclError:
                print(f"⚠️  Icon file exists but couldn't be loaded: {icon_path}")
        else:
            print(f"ℹ️  No icon found at: {icon_path}")
        
        # Create and show widget
        widget = AstronomicalWidgetMode(master=None)
        widget.start_updates()
        
        print("✅ Widget started successfully!")
        print("🖱️  Right-click widget for options")
        print("⚡ Updates every 86ms (1 mikroDies)")
        print()
        print("Press Ctrl+C to exit or right-click widget → Exit")
        
        # Start main loop
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print()
        print("Troubleshooting:")
        print("- Make sure tkinter is installed")
        print("- Try: sudo apt-get install python3-tk")
        print("- Or: python -m tkinter")
        return 1
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Troubleshooting tips:")
        print("- Make sure Python 3.6+ is installed")
        print("- Check that tkinter is available")
        print("- Try running: python -m tkinter")
        return 1
        
    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n👋 Widget closed by user")
        exit(0)