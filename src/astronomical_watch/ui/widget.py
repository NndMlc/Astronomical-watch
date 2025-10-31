"""
Astronomical Watch Widget - Small corner display
"""
from __future__ import annotations
import tkinter as tk
from datetime import datetime, timezone
from typing import Optional, Callable
from .gradient import get_sky_theme

from src.astronomical_watch.core.astro_time_core import AstroYear

class AstronomicalWidgetMode:
    def __init__(self, master: tk.Widget = None, on_click_callback: Optional[Callable] = None):
        self.master = master or tk.Tk()
        self.master.title("Astronomical Watch - Widget")
        self.master.geometry("210x140")
        self.master.minsize(160, 120)
        
        # Store callback for click events
        self.on_click_callback = on_click_callback
        
        # Current time values
        self.day_index = 0
        self.milliDies = 0
        
        # Update job reference
        self.update_job = None
        
        self._create_widgets()
        self._apply_theme()
        
        # Bind click event to entire widget
        self._bind_click_events()
        
    def _create_widgets(self):
        """Create the main UI elements."""
        # Main frame
        self.frame = tk.Frame(self.master, bd=0, relief='flat')
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Time display
        self.time_label = tk.Label(
            self.frame,
            text="000·000",
            font=("Courier New", 20, "bold"),
            fg="white"
        )
        self.time_label.pack(expand=True)
        
        # Small info label
        self.info_label = tk.Label(
            self.frame,
            text="Astronomical Time",
            font=("Arial", 8),
            fg="lightgray"
        )
        self.info_label.pack()
        
    def _bind_click_events(self):
        """Bind click events to all widgets."""
        def on_click(event=None):
            if self.on_click_callback:
                self.on_click_callback()
                
        # Bind to all widgets
        for widget in [self.master, self.frame, self.time_label, self.info_label]:
            widget.bind("<Button-1>", on_click)
            
    def _apply_theme(self):
        """Apply sky gradient theme based on current time."""
        now_utc = datetime.now(timezone.utc)
        theme = get_sky_theme(now_utc)
        
        # Use top color for widget background (could also blend top/bottom)
        bg_color = theme.top_color
        text_color = theme.text_color
        
        self.master.configure(bg=bg_color)
        self.frame.configure(bg=bg_color)
        
        # Update label backgrounds and text colors to match
        self.time_label.configure(bg=bg_color, fg=text_color)
        self.info_label.configure(bg=bg_color, fg="lightgray")
        
    def _update_display(self):
        """Update the astronomical time display."""
        try:
            # Get current time
            now_utc = datetime.now(timezone.utc)
            
            # Use hardcoded equinox values for now
            current_equinox = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
            next_equinox = datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
            
            # Create AstroYear and get reading
            astro_year = AstroYear(current_equinox, next_equinox)
            reading = astro_year.reading(now_utc)
            
            # Update display values
            self.day_index = reading.day_index
            self.milliDies = reading.miliDies
            
            # Update UI
            time_str = f"{self.day_index:03d}·{self.milliDies:03d}"
            self.time_label.config(text=time_str)
            
            # Update theme
            self._apply_theme()
            
        except Exception as e:
            print(f"Widget update error: {e}")
            # Fallback display
            self.time_label.config(text="ERR·000")
            
    def start_updates(self):
        """Start the periodic update cycle."""
        self._update_display()
        # Schedule next update in 1 second
        self.update_job = self.master.after(1000, self.start_updates)
        
    def stop_updates(self):
        """Stop the periodic updates."""
        if self.update_job:
            self.master.after_cancel(self.update_job)
            self.update_job = None

def create_widget(master: tk.Widget = None, on_click_callback: Optional[Callable] = None) -> AstronomicalWidgetMode:
    """Factory function to create widget instance."""
    return AstronomicalWidgetMode(master, on_click_callback)

if __name__ == "__main__":
    # Test the widget
    root = tk.Tk()
    widget = create_widget(root)
    widget.start_updates()
    root.mainloop()