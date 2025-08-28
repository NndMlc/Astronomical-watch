#!/usr/bin/env python3
"""
Simple launcher to test the UI components.
"""
import sys
import os

# Add the root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_widget():
    """Test the widget UI."""
    print("Testing Widget UI...")
    from ui.widget import create_widget, AstronomicalWidget
    import tkinter as tk
    
    root = tk.Tk()
    root.title("Widget Test")
    root.geometry("250x120")
    
    def click_handler():
        print("Widget clicked! This would open Normal Mode.")
        # Test by showing current theme
        from ui.gradient import get_sky_theme
        theme = get_sky_theme()
        print(f"Current theme: {theme.top_color} -> {theme.bottom_color}")
    
    widget = create_widget(root, click_handler)
    widget.start_updates()
    
    # Run for a few seconds then close
    root.after(3000, lambda: root.quit())  # Close after 3 seconds
    
    try:
        root.mainloop()
        print("Widget test completed successfully!")
        return True
    except Exception as e:
        print(f"Widget test failed: {e}")
        return False

def test_normal_mode():
    """Test the normal mode UI."""
    print("Testing Normal Mode UI...")
    from ui.normal_mode import create_normal_mode
    import tkinter as tk
    
    root = tk.Tk()
    
    normal_mode = create_normal_mode(root)
    normal_mode.start_updates()
    
    # Run for a few seconds then close
    root.after(3000, lambda: root.quit())  # Close after 3 seconds
    
    try:
        root.mainloop()
        print("Normal Mode test completed successfully!")
        return True
    except Exception as e:
        print(f"Normal Mode test failed: {e}")
        return False

def test_integration():
    """Test widget to normal mode integration."""
    print("Testing Widget -> Normal Mode integration...")
    from ui.main import AstronomicalWatchApp
    
    app = AstronomicalWatchApp()
    app.show_widget()
    
    # Simulate widget click after 1 second
    if app.widget_root:
        app.widget_root.after(1000, app.open_normal_mode)
        # Close everything after 3 seconds
        app.widget_root.after(3000, app.widget_root.quit)
        
        try:
            app.widget_root.mainloop()
            print("Integration test completed successfully!")
            return True
        except Exception as e:
            print(f"Integration test failed: {e}")
            return False
    return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = "widget"
    
    if test_type == "widget":
        success = test_widget()
    elif test_type == "normal":
        success = test_normal_mode()
    elif test_type == "integration":
        success = test_integration()
    else:
        print(f"Unknown test type: {test_type}")
        print("Usage: python test_ui.py [widget|normal|integration]")
        success = False
    
    sys.exit(0 if success else 1)