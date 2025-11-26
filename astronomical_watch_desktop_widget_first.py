#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astronomical Watch Desktop Application - Widget First
Shows widget immediately, with option for full application
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
        print("⚠️  Warning: Python 3.6+ recommended")
        return version.major >= 3
    return True

def main():
    """Launch desktop application with widget first approach."""
    print("=" * 50)
    print(" ASTRONOMICAL WATCH DESKTOP")
    print("=" * 50)
    print()
    print("Widget-first astronomical timekeeping system")
    print("- Dies.miliDies.mikroDies format")
    print("- Based on vernal equinox cycles")
    print("- Universal reference meridian")
    print()
    
    if not check_python_version():
        print("Some features may not work with older Python")
        print()
    
    try:
        import tkinter as tk
        from astronomical_watch.ui.widget import AstronomicalWidgetMode
        from astronomical_watch.ui.main import main as ui_main
        
        print("🚀 Starting floating widget...")
        
        # Create root window 
        root = tk.Tk()
        root.withdraw()  # Hide initially
        
        # Set application icon if available
        icon_path = os.path.join(current_dir, "icons", "astronomical_watch.ico")
        if os.path.exists(icon_path):
            try:
                root.iconbitmap(icon_path)
                print(f"✅ Icon loaded: {icon_path}")
            except tk.TclError:
                print(f"⚠️  Icon file couldn't be loaded: {icon_path}")
        
        # Create widget first
        def on_widget_double_click():
            """Open full application when widget is double-clicked."""
            print("🔄 Opening full application...")
            # This will be handled by the widget internally
            pass
        
        widget = AstronomicalWidgetMode(master=None, on_click_callback=on_widget_double_click)
        widget.start_updates()
        
        print("✅ Floating widget active!")
        print("📍 Position: Always on top")
        print("🖱️  Double-click widget: Open full app")
        print("🖱️  Right-click widget: Context menu")
        print("🖱️  Drag widget: Reposition")
        print("⚡ Updates: Every 86ms")
        print()
        print("Widget shows current astronomical time:")
        print("- DDD: Dies (days since vernal equinox)")
        print("- mmm: miliDies (thousandths of a Dies)")
        print("- Progress bar: mikroDies (0-999)")
        print()
        print("Press Ctrl+C to exit or use widget menu")
        
        # Keep application running
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print()
        print("Troubleshooting:")
        print("- Ensure tkinter is installed")
        print("- Try: python -m tkinter")
        return 1
        
    except Exception as e:
        print(f"❌ Application error: {e}")
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
        print("\n👋 Application closed by user")
        exit(0)