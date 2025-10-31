"""
Main application demonstrating Widget and Normal Mode integration.
Shows full click activation and consistent gradient backgrounds.
"""
from __future__ import annotations
import tkinter as tk
from .widget import create_widget
from .normal_mode import create_normal_mode


class AstronomicalWatchApp:
    """Main application managing Widget and Normal Mode windows."""
    
    def __init__(self):
        self.widget_root = None
        self.normal_root = None
        self.widget = None
        self.normal_mode = None
    
    def show_widget(self):
        """Show the widget window."""
        if self.widget_root is None:
            self.widget_root = tk.Tk()
            self.widget_root.protocol("WM_DELETE_WINDOW", self.on_widget_close)
            
            # Create widget with click handler to open normal mode
            self.widget = create_widget(self.widget_root, self.open_normal_mode)
            self.widget.start_updates()
    
    def open_normal_mode(self):
        """Open Normal Mode window (triggered by widget click)."""
        print("Opening Normal Mode from widget click...")
        
        if self.normal_root is None:
            self.normal_root = tk.Toplevel()
            self.normal_root.protocol("WM_DELETE_WINDOW", self.on_normal_close)
            
            self.normal_mode = create_normal_mode(self.normal_root)
            self.normal_mode.start_updates()
        else:
            # Bring to front if already open
            self.normal_root.deiconify()
            self.normal_root.lift()
            self.normal_root.focus_force()
    
    def on_widget_close(self):
        """Handle widget window close."""
        if self.normal_root:
            self.normal_root.destroy()
            self.normal_root = None
            self.normal_mode = None
        
        self.widget_root.destroy()
        self.widget_root = None
        self.widget = None
    
    def on_normal_close(self):
        """Handle normal mode window close."""
        self.normal_root.destroy()
        self.normal_root = None
        self.normal_mode = None
    
    def run(self):
        """Start the application."""
        self.show_widget()
        
        if self.widget_root:
            self.widget_root.mainloop()


def main():
    """Main entry point."""
    app = AstronomicalWatchApp()
    app.run()


if __name__ == "__main__":
    main()