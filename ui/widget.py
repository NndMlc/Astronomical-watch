"""
Widget Mode for Astronomical Watch
Provides a compact widget with dynamic sky gradient background and full-area click activation.
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timezone
from typing import Callable, Optional
from .gradient import get_sky_theme, create_gradient_colors


class AstronomicalWidget:
    """
    A compact widget showing astronomical time with dynamic sky gradient background.
    Entire widget area is clickable to open Normal Mode.
    """
    
    def __init__(self, master: tk.Widget = None, on_click: Callable = None):
        self.master = master or tk.Tk()
        self.on_click_callback = on_click or self._default_click_handler
        self.current_theme = None
        
        # Create main window if we're the root
        if master is None:
            self.master.title("Astronomical Watch - Widget")
            self.master.geometry("200x80")
            self.master.resizable(False, False)
        
        self._create_widgets()
        self._setup_bindings()
        self._apply_theme()
    
    def _create_widgets(self) -> None:
        """Create the widget components."""
        # Background canvas for gradient
        self.bg_canvas = tk.Canvas(
            self.master,
            highlightthickness=0,
            bd=0
        )
        self.bg_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Overlay frame to hold content - use create_window for layout
        self.overlay_frame = tk.Frame(self.bg_canvas, bg='', bd=0)
        self.canvas_window = self.bg_canvas.create_window(
            0, 0, anchor=tk.NW, window=self.overlay_frame
        )
        
        # Time display label
        self.time_label = tk.Label(
            self.overlay_frame,
            text="2024eq:123.456",
            font=("Arial", 12, "bold"),
            bg='',  # Transparent background
            bd=0
        )
        self.time_label.pack(pady=10)
        
        # Progress bar for day fraction
        self.progress = ttk.Progressbar(
            self.overlay_frame,
            mode='determinate',
            length=150
        )
        self.progress['value'] = 45.6  # Example value
        self.progress.pack(pady=5)
        
        # Status label
        self.status_label = tk.Label(
            self.overlay_frame,
            text="Day 123 of astronomical year",
            font=("Arial", 8),
            bg='',  # Transparent background
            bd=0
        )
        self.status_label.pack()
    
    def _setup_bindings(self) -> None:
        """Set up click bindings for full widget activation."""
        # Bind click events to all components for full activation
        widgets_to_bind = [
            self.master,         # Root window
            self.bg_canvas,      # Background canvas
            self.overlay_frame,  # Overlay frame
            self.time_label,     # Time label
            self.status_label    # Status label
        ]
        
        for widget in widgets_to_bind:
            widget.bind("<Button-1>", self._handle_click)
            widget.bind("<Double-Button-1>", self._handle_click)
        
        # Progress bar needs special handling
        self.progress.bind("<Button-1>", self._handle_click)
        
        # Handle canvas resize
        self.bg_canvas.bind('<Configure>', self._on_canvas_configure)
    
    def _on_canvas_configure(self, event) -> None:
        """Handle canvas resize to maintain gradient."""
        # Update canvas window size
        self.bg_canvas.itemconfig(
            self.canvas_window,
            width=event.width,
            height=event.height
        )
        # Redraw gradient
        self._draw_gradient()
    
    def _handle_click(self, event) -> None:
        """Handle click events - call the callback to open Normal Mode."""
        if self.on_click_callback:
            self.on_click_callback()
    
    def _default_click_handler(self) -> None:
        """Default click handler - shows a message."""
        print("Widget clicked - would open Normal Mode")
        # In real implementation, this would open the Normal Mode window
    
    def _draw_gradient(self) -> None:
        """Draw the vertical gradient background."""
        if not self.current_theme:
            return
            
        # Clear existing gradient
        self.bg_canvas.delete("gradient")
        
        # Get canvas dimensions
        canvas_width = self.bg_canvas.winfo_width()
        canvas_height = self.bg_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not yet sized
            self.master.after(50, self._draw_gradient)
            return
        
        # Create gradient colors
        num_steps = max(50, canvas_height // 2)  # Smooth gradient
        gradient_colors = create_gradient_colors(self.current_theme, num_steps)
        
        # Draw gradient as horizontal lines
        step_height = canvas_height / len(gradient_colors)
        
        for i, color in enumerate(gradient_colors):
            y1 = i * step_height
            y2 = (i + 1) * step_height
            
            self.bg_canvas.create_rectangle(
                0, y1, canvas_width, y2,
                fill=color, outline=color,
                tags="gradient"
            )
    
    def _apply_theme(self, dt: datetime = None) -> None:
        """Apply current sky theme to the widget."""
        theme = get_sky_theme(dt)
        
        if theme != self.current_theme:
            self.current_theme = theme
            
            # Update text colors
            text_color = theme.text_hex
            self.time_label.config(fg=text_color)
            self.status_label.config(fg=text_color)
            
            # Make overlay frame transparent  
            self.overlay_frame.config(bg='')
            self.time_label.config(bg='')
            self.status_label.config(bg='')
            
            # Redraw gradient background
            self._draw_gradient()
    
    def update_time_display(self, dt: datetime = None) -> None:
        """Update the time display and refresh theme if needed."""
        if dt is None:
            dt = datetime.now(timezone.utc)
        
        # Update theme (which may have changed with time)
        self._apply_theme(dt)
        
        # Update time display (simplified astronomical format)
        day_of_year = dt.timetuple().tm_yday
        hour_fraction = (dt.hour * 3600 + dt.minute * 60 + dt.second) / 86400
        milli_day = int(hour_fraction * 1000)
        
        time_str = f"{dt.year}eq:{day_of_year:03d}.{milli_day:03d}"
        self.time_label.config(text=time_str)
        
        # Update status
        status_str = f"Day {day_of_year} of astronomical year"
        self.status_label.config(text=status_str)
        
        # Update progress bar
        self.progress['value'] = milli_day / 10  # Scale to 0-100
    
    def set_click_handler(self, callback: Callable) -> None:
        """Set the callback function for widget clicks."""
        self.on_click_callback = callback
    
    def start_updates(self, interval_ms: int = 1000) -> None:
        """Start automatic time updates."""
        def update():
            self.update_time_display()
            self.master.after(interval_ms, update)
        
        update()


def create_widget(master: tk.Widget = None, on_click: Callable = None) -> AstronomicalWidget:
    """Factory function to create an AstronomicalWidget."""
    return AstronomicalWidget(master, on_click)


def demo_widget():
    """Standalone demo of the widget."""
    root = tk.Tk()
    root.title("Astronomical Widget Demo")
    root.geometry("250x120")
    
    def click_handler():
        print("Widget clicked! Opening Normal Mode...")
        # In real app, would open normal mode window
    
    widget = create_widget(root, click_handler)
    widget.start_updates()
    
    root.mainloop()


if __name__ == "__main__":
    demo_widget()


__all__ = ['AstronomicalWidget', 'create_widget']