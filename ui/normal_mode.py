"""
Normal Mode for Astronomical Watch
Full-featured interface with the same dynamic sky gradient background as Widget Mode.
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timezone
from typing import Optional
from .gradient import get_sky_theme, create_gradient_colors


class AstronomicalNormalMode:
    """
    Full-featured Normal Mode with dynamic sky gradient background.
    Uses the same background logic as Widget Mode.
    """
    
    def __init__(self, master: tk.Widget = None):
        self.master = master or tk.Tk()
        self.current_theme = None
        
        # Create main window if we're the root
        if master is None:
            self.master.title("Astronomical Watch - Normal Mode")
            self.master.geometry("400x300")
            self.master.minsize(350, 250)
        
        self._create_widgets()
        self._apply_theme()
    
    def _create_widgets(self) -> None:
        """Create the normal mode interface components."""
        # Background canvas for gradient (same as widget)
        self.bg_canvas = tk.Canvas(
            self.master,
            highlightthickness=0,
            bd=0
        )
        self.bg_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Main content frame - use create_window for layout
        self.main_frame = tk.Frame(self.bg_canvas, bg='', bd=0)
        self.canvas_window = self.bg_canvas.create_window(
            0, 0, anchor=tk.NW, window=self.main_frame
        )
        
        # Title label
        self.title_label = tk.Label(
            self.main_frame,
            text="Astronomical Watch",
            font=("Arial", 16, "bold"),
            bg='',
            bd=0
        )
        self.title_label.pack(pady=10)
        
        # Create notebook for tabs (future i18n and content)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Current time tab
        self._create_time_tab()
        
        # Settings tab (placeholder)
        self._create_settings_tab()
        
        # Status bar
        self.status_frame = tk.Frame(self.main_frame, bg='', bd=0)
        self.status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            font=("Arial", 9),
            bg='',
            bd=0
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Handle canvas resize
        self.bg_canvas.bind('<Configure>', self._on_canvas_configure)
    
    def _create_time_tab(self) -> None:
        """Create the current time display tab."""
        time_frame = tk.Frame(self.notebook, bg='')
        self.notebook.add(time_frame, text="Current Time")
        
        # Large time display
        self.large_time_label = tk.Label(
            time_frame,
            text="2024eq:123.456",
            font=("Arial", 24, "bold"),
            bg='',
            bd=0
        )
        self.large_time_label.pack(pady=20)
        
        # Detailed info frame
        info_frame = tk.Frame(time_frame, bg='')
        info_frame.pack(expand=True, fill=tk.BOTH, padx=20)
        
        # Day information
        self.day_info_label = tk.Label(
            info_frame,
            text="Day 123 of astronomical year 2024",
            font=("Arial", 12),
            bg='',
            bd=0
        )
        self.day_info_label.pack(pady=5)
        
        # Time breakdown
        self.time_breakdown_label = tk.Label(
            info_frame,
            text="Milli-day: 456 (45.6% through day)",
            font=("Arial", 10),
            bg='',
            bd=0
        )
        self.time_breakdown_label.pack(pady=2)
        
        # Solar info
        self.solar_info_label = tk.Label(
            info_frame,
            text="Solar altitude: ~23° (day time)",
            font=("Arial", 10),
            bg='',
            bd=0
        )
        self.solar_info_label.pack(pady=2)
        
        # Progress bar for day
        tk.Label(info_frame, text="Day Progress:", font=("Arial", 9), bg='').pack(anchor=tk.W, pady=(10, 0))
        self.day_progress = ttk.Progressbar(
            info_frame,
            mode='determinate',
            length=300
        )
        self.day_progress.pack(pady=5)
        
        # Year progress
        tk.Label(info_frame, text="Year Progress:", font=("Arial", 9), bg='').pack(anchor=tk.W, pady=(10, 0))
        self.year_progress = ttk.Progressbar(
            info_frame,
            mode='determinate',
            length=300
        )
        self.year_progress.pack(pady=5)
    
    def _create_settings_tab(self) -> None:
        """Create the settings tab (placeholder for future features)."""
        settings_frame = tk.Frame(self.notebook, bg='')
        self.notebook.add(settings_frame, text="Settings")
        
        tk.Label(
            settings_frame,
            text="Settings (Future Enhancement)",
            font=("Arial", 14, "bold"),
            bg=''
        ).pack(pady=20)
        
        tk.Label(
            settings_frame,
            text="• Timezone selection\n• Display format options\n• Theme preferences\n• i18n language selection",
            font=("Arial", 10),
            bg='',
            justify=tk.LEFT
        ).pack(pady=10)
    
    def _on_canvas_configure(self, event) -> None:
        """Handle canvas resize to maintain gradient and content."""
        # Update canvas window size
        self.bg_canvas.itemconfig(
            self.canvas_window,
            width=event.width,
            height=event.height
        )
        # Redraw gradient
        self._draw_gradient()
    
    def _draw_gradient(self) -> None:
        """Draw the vertical gradient background (same logic as widget)."""
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
        
        # Create gradient colors (same as widget)
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
        """Apply current sky theme (same logic as widget)."""
        theme = get_sky_theme(dt)
        
        if theme != self.current_theme:
            self.current_theme = theme
            
            # Update text colors (adaptive text color logic)
            text_color = theme.text_hex
            
            # Update all text elements
            text_widgets = [
                self.title_label,
                self.large_time_label,
                self.day_info_label,
                self.time_breakdown_label,
                self.solar_info_label,
                self.status_label
            ]
            
            for widget in text_widgets:
                widget.config(fg=text_color)
            
            # Make frames transparent to show gradient
            transparent_frames = [
                self.main_frame,
                self.status_frame
            ]
            
            for frame in transparent_frames:
                frame.config(bg='')
            
            # Redraw gradient background
            self._draw_gradient()
    
    def update_display(self, dt: datetime = None) -> None:
        """Update the display and refresh theme if needed."""
        if dt is None:
            dt = datetime.now(timezone.utc)
        
        # Update theme (which may have changed with time)
        self._apply_theme(dt)
        
        # Update time displays (simplified astronomical format)
        day_of_year = dt.timetuple().tm_yday
        hour_fraction = (dt.hour * 3600 + dt.minute * 60 + dt.second) / 86400
        milli_day = int(hour_fraction * 1000)
        
        time_str = f"{dt.year}eq:{day_of_year:03d}.{milli_day:03d}"
        self.large_time_label.config(text=time_str)
        
        # Update detailed information
        self.day_info_label.config(text=f"Day {day_of_year} of astronomical year {dt.year}")
        self.time_breakdown_label.config(text=f"Milli-day: {milli_day} ({milli_day/10:.1f}% through day)")
        
        # Solar altitude info (using our gradient helper)
        from .gradient import get_solar_altitude_approximation
        altitude = get_solar_altitude_approximation(dt)
        altitude_desc = "day time" if altitude > 0 else "night time"
        self.solar_info_label.config(text=f"Solar altitude: ~{altitude:.0f}° ({altitude_desc})")
        
        # Update progress bars
        self.day_progress['value'] = milli_day / 10  # Scale to 0-100
        days_in_year = 366 if dt.year % 4 == 0 else 365  # Simple leap year check
        self.year_progress['value'] = (day_of_year / days_in_year) * 100
        
        # Update status
        self.status_label.config(text=f"Last updated: {dt.strftime('%H:%M:%S UTC')}")
    
    def start_updates(self, interval_ms: int = 1000) -> None:
        """Start automatic time updates."""
        def update():
            self.update_display()
            self.master.after(interval_ms, update)
        
        update()


def create_normal_mode(master: tk.Widget = None) -> AstronomicalNormalMode:
    """Factory function to create an AstronomicalNormalMode."""
    return AstronomicalNormalMode(master)


def demo_normal_mode():
    """Standalone demo of normal mode."""
    root = tk.Tk()
    
    normal_mode = create_normal_mode(root)
    normal_mode.start_updates()
    
    root.mainloop()


if __name__ == "__main__":
    demo_normal_mode()


__all__ = ['AstronomicalNormalMode', 'create_normal_mode']