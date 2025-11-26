#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astronomical Watch Desktop Application - Integrated Legacy Support
Compatible with Python 3.6+ with fallback for older versions
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
    if version.major < 3:
        print("=" * 60)
        print("ASTRONOMICAL WATCH - PYTHON 2 NOT SUPPORTED")
        print("=" * 60)
        print("Your Python version: {}.{}.{}".format(version.major, version.minor, version.micro))
        print("Required: Python 3.6 or higher")
        print("")
        print("Python 2 is no longer supported as of January 1, 2020.")
        print("Please update Python from: https://python.org")
        print("=" * 60)
        return False
        
    if version.major == 3 and version.minor < 6:
        print("=" * 60)
        print("ASTRONOMICAL WATCH COMPATIBILITY WARNING")
        print("=" * 60)
        print("Your Python version: {}.{}.{}".format(version.major, version.minor, version.micro))
        print("Recommended: Python 3.6 or higher")
        print("")
        print("Some features may not work correctly:")
        print("- F-string syntax requires Python 3.6+")
        print("- Type hints require Python 3.5+")
        print("- Async/await improvements in 3.7+")
        print("")
        print("Please update Python from: https://python.org")
        print("=" * 60)
        
        try:
            # Use input() for Python 3 compatibility
            input("Press Enter to continue anyway, or Ctrl+C to exit...")
        except KeyboardInterrupt:
            print("\nExiting...")
            return False
    return True

def set_application_icon():
    """Set application icon if available."""
    try:
        import tkinter as tk
        icon_path = os.path.join(current_dir, "icons", "astronomical_watch.ico")
        if os.path.exists(icon_path):
            # Create hidden root for icon setting
            root = tk.Tk()
            root.withdraw()
            root.iconbitmap(icon_path)
            return root
    except Exception:
        pass
    return None

def launch_widget_mode():
    """Launch widget-only mode as fallback."""
    print("Launching widget mode...")
    try:
        from astronomical_watch.ui.widget import AstronomicalWidgetMode
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        # Set icon if available
        icon_path = os.path.join(current_dir, "icons", "astronomical_watch.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        
        widget = AstronomicalWidgetMode(master=None)
        widget.start_updates()
        
        print("✅ Widget mode started successfully!")
        print("🖱️  Right-click widget for options")
        print("🖱️  Double-click widget to attempt full mode")
        
        root.mainloop()
        return True
    except Exception as e:
        print("Widget mode failed: {}".format(str(e)))
        return False

def launch_full_application():
    """Launch the full astronomical watch application."""
    try:
        # Set icon before launching
        icon_root = set_application_icon()
        
        from astronomical_watch.ui.main import main as ui_main
        ui_main()
        
        if icon_root:
            icon_root.destroy()
        return True
    except ImportError as e:
        print("Import Error: {}".format(str(e)))
        print("Trying fallback widget mode...")
        return launch_widget_mode()
    except Exception as e:
        print("Full application failed: {}".format(str(e)))
        print("Trying fallback widget mode...")
        return launch_widget_mode()

def main():
    """Launch the desktop application with integrated architecture."""
    print("=" * 50)
    print(" ASTRONOMICAL WATCH - DESKTOP APPLICATION")
    print("=" * 50)
    print("Integrated astronomical timekeeping system")
    print("- Dies.miliDies.mikroDies format")
    print("- Vernal equinox-based calendar")
    print("- Widget and full application modes")
    print("")
    
    if not check_python_version():
        return 1
    
    print("Starting application...")
    print("")
    
    try:
        # Try full application first
        if launch_full_application():
            return 0
        else:
            print("All launch methods failed.")
            return 1
            
    except SyntaxError as e:
        print("SYNTAX ERROR:")
        print("Error: {}".format(str(e)))
        print("")
        print("This likely means your Python version is too old.")
        print("The application requires Python 3.6+ for full compatibility.")
        print("Please update Python from: https://python.org")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
        return 0
    except Exception as e:
        print("Unexpected error: {}".format(str(e)))
        print("")
        print("Troubleshooting tips:")
        print("- Ensure Python 3.6+ is installed")
        print("- Check that tkinter is available: python -m tkinter")
        print("- Try widget-only mode: python astronomical_watch_widget_only.py")
        return 1

if __name__ == "__main__":
    exit(main())