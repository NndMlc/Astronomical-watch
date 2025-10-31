"""
Astronomical Watch Widget - Small corner display
"""
from __future__ import annotations
import tkinter as tk
from datetime import datetime, timezone
from typing import Optional, Callable
from .gradient import get_sky_theme
from .translations import tr

from src.astronomical_watch.core.astro_time_core import AstroYear

class AstronomicalWidgetMode:
    def __init__(self, master: tk.Widget = None, on_click_callback: Optional[Callable] = None):
        self.master = master or tk.Tk()
        self.master.title("Astronomical Watch - Widget")
        self.master.geometry("160x90")
        self.master.minsize(160, 90)
        
        # Store callback for click events
        self.on_click_callback = on_click_callback
        
        # Current time values
        self.day_index = 0
        self.milliDies = 0
        self.microDies = 0
        
        # Current language for title
        self.current_language = "en"
        
        # Update job reference
        self.update_job = None
        
        self._create_widgets()
        self._apply_theme()
        
        # Bind click event to entire widget
        self._bind_click_events()
        
    def _create_widgets(self):
        """Create the main UI elements."""
        # Main frame with margins
        self.frame = tk.Frame(self.master, bd=0, relief='flat')
        self.frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Title label
        self.title_label = tk.Label(
            self.frame,
            text=tr("title", self.current_language),
            font=("Arial", 9),
            fg="white"
        )
        self.title_label.pack()
        
        # Main time display (Dies.miliDies)
        try:
            # Try DejaVu Sans Mono first, fallback to Courier New
            time_font = ("DejaVu Sans Mono", 28, "bold")
        except:
            time_font = ("Courier New", 28, "bold")
            
        self.time_label = tk.Label(
            self.frame,
            text="000.000",
            font=time_font,
            fg="white",
            relief="solid",
            bd=1
        )
        self.time_label.pack(pady=(2, 0))
        
        # Format label
        self.format_label = tk.Label(
            self.frame,
            text="Dies . miliDies",
            font=("Arial", 8),
            fg="lightgray"
        )
        self.format_label.pack()
        
        # Progress bar for mikroDies (0-999)
        self.progress_frame = tk.Frame(self.frame)
        self.progress_frame.pack(pady=(1, 0), fill="x")
        
        self.progress_canvas = tk.Canvas(
            self.progress_frame,
            height=6,
            bg="gray25",
            highlightthickness=0
        )
        self.progress_canvas.pack(fill="x")
        
        # MikroDies label
        self.micro_label = tk.Label(
            self.frame,
            text="mikroDies: 000",
            font=("Arial", 8),
            fg="lightgray"
        )
        self.micro_label.pack()
        
    def _bind_click_events(self):
        """Bind click events to all widgets."""
        def on_click(event=None):
            if self.on_click_callback:
                self.on_click_callback()
        
        # Bind to all widgets for full-area click activation
        self.master.bind("<Button-1>", on_click)
        self.frame.bind("<Button-1>", on_click)
        self.title_label.bind("<Button-1>", on_click)
        self.time_label.bind("<Button-1>", on_click)
        self.format_label.bind("<Button-1>", on_click)
        self.progress_frame.bind("<Button-1>", on_click)
        self.progress_canvas.bind("<Button-1>", on_click)
        self.micro_label.bind("<Button-1>", on_click)
            
    def _apply_theme(self):
        """Apply sky gradient theme based on current time."""
        now_utc = datetime.now(timezone.utc)
        theme = get_sky_theme(now_utc)
        
        # Use top color for widget background (could also blend top/bottom)
        bg_color = theme.top_color
        text_color = theme.text_color
        
        self.master.configure(bg=bg_color)
        self.frame.configure(bg=bg_color)
        
        # Update all label backgrounds and text colors to match
        self.title_label.configure(bg=bg_color, fg=text_color)
        self.time_label.configure(bg=bg_color, fg=text_color, highlightbackground="black")
        self.format_label.configure(bg=bg_color, fg="lightgray")
        self.progress_frame.configure(bg=bg_color)
        self.micro_label.configure(bg=bg_color, fg="lightgray")
        
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
            self.microDies = reading.mikroDies  # Use the real mikroDies from AstroYear
            
            # Update title with current language
            self.title_label.config(text=tr("title", self.current_language))
            
            # Update main time display (Dies.miliDies)
            time_str = f"{self.day_index:03d}.{self.milliDies:03d}"
            self.time_label.config(text=time_str)
            
            # Update mikroDies label
            self.micro_label.config(text=f"mikroDies: {self.microDies:03d}")
            
            # Update progress bar for mikroDies (0-999)
            self._update_progress_bar()
            
            # Update theme
            self._apply_theme()
            
        except Exception as e:
            print(f"Widget update error: {e}")
            # Fallback display
            self.time_label.config(text="ERR.000")
            self.micro_label.config(text="mikroDies: 000")
            
    def _update_progress_bar(self):
        """Update the mikroDies progress bar."""
        try:
            # Clear canvas
            self.progress_canvas.delete("all")
            
            # Get canvas dimensions
            canvas_width = self.progress_canvas.winfo_width()
            canvas_height = self.progress_canvas.winfo_height()
            
            if canvas_width <= 1:  # Not yet rendered
                self.master.after(10, self._update_progress_bar)
                return
            
            # Calculate progress (0-999 mikroDies)
            progress = self.microDies / 999.0  # 0.0 to 1.0
            
            # Draw background
            self.progress_canvas.create_rectangle(
                0, 0, canvas_width, canvas_height,
                fill="gray25", outline=""
            )
            
            # Draw progress bar
            if progress > 0:
                progress_width = int(canvas_width * progress)
                self.progress_canvas.create_rectangle(
                    0, 0, progress_width, canvas_height,
                    fill="lightblue", outline=""
                )
                
        except Exception as e:
            print(f"Progress bar update error: {e}")
            
    def set_language(self, language: str):
        """Update widget language."""
        self.current_language = language
        # Force immediate update to reflect language change
        self._update_display()
            
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