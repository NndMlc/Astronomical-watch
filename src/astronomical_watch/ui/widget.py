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
        self.master.geometry("140x70")
        self.master.minsize(140, 70)
        
        # Remove title bar (navbar with minimize/maximize/close buttons)
        self.master.overrideredirect(True)
        
        # Add drag support since there's no title bar
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._drag_moved = False
        
        # Always on top state
        self._always_on_top = True
        self.master.attributes('-topmost', True)
        
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
        """Create minimalistic UI elements - only numbers and progress bar."""
        # Main frame with margins
        self.frame = tk.Frame(self.master, bd=0, relief='flat')
        self.frame.pack(fill="both", expand=True, padx=8, pady=5)
        
        # Main time display (Dies.miliDies) using Canvas for outlined text
        self.time_canvas = tk.Canvas(
            self.frame,
            height=35,
            highlightthickness=0,
            bd=0
        )
        self.time_canvas.pack(pady=(0, 2))
        
        # Progress bar for mikroDies (0-999)
        self.progress_frame = tk.Frame(self.frame)
        self.progress_frame.pack(fill="x")
        
        self.progress_canvas = tk.Canvas(
            self.progress_frame,
            height=6,
            bg="gray25",
            highlightthickness=0
        )
        self.progress_canvas.pack(fill="x")
        
        # Create context menu
        self._create_context_menu()
        
    def _create_context_menu(self):
        """Create right-click context menu."""
        self.context_menu = tk.Menu(self.master, tearoff=0)
        
        # Always on top toggle
        self.context_menu.add_checkbutton(
            label="Always on top",
            variable=tk.BooleanVar(value=self._always_on_top),
            command=self._toggle_always_on_top
        )
        
        self.context_menu.add_separator()
        
        # Exit option
        self.context_menu.add_command(
            label="Exit",
            command=self._exit_widget
        )
        
    def _toggle_always_on_top(self):
        """Toggle always on top setting."""
        self._always_on_top = not self._always_on_top
        self.master.attributes('-topmost', self._always_on_top)
        
    def _exit_widget(self):
        """Exit the widget application."""
        self.stop_updates()
        self.master.quit()
        self.master.destroy()
        
    def _show_context_menu(self, event):
        """Show context menu on right click."""
        try:
            # Update the checkbutton state
            self.context_menu.entryconfig(0, variable=tk.BooleanVar(value=self._always_on_top))
            self.context_menu.tk_popup(event.x_root, event.y_root)
        except tk.TclError:
            pass  # Menu was dismissed
        
    def _bind_click_events(self):
        """Bind interaction events to all widgets."""
        def on_drag_start(event):
            self._drag_start_x = event.x_root
            self._drag_start_y = event.y_root
            self._drag_moved = False
            
        def on_drag(event):
            # Calculate distance moved
            dx = abs(event.x_root - self._drag_start_x)
            dy = abs(event.y_root - self._drag_start_y)
            
            if dx > 3 or dy > 3:  # Only start dragging after small movement threshold
                self._drag_moved = True
                x = self.master.winfo_x() + (event.x_root - self._drag_start_x)
                y = self.master.winfo_y() + (event.y_root - self._drag_start_y)
                self.master.geometry(f"+{x}+{y}")
                self._drag_start_x = event.x_root
                self._drag_start_y = event.y_root
                
        def on_double_click(event):
            # Double click to open Normal Mode (prevents accidental activation)
            if not self._drag_moved and self.on_click_callback:
                self.on_click_callback()
        
        # Bind events to all widgets for full-area interaction
        # Single click + drag = move widget
        # Double click = open Normal Mode
        # Interactive widgets (only canvas and frame for minimalistic design)
        widgets_for_interaction = [
            self.master, self.frame, self.canvas
        ]
        
        for widget in widgets_for_interaction:
            widget.bind("<ButtonPress-1>", on_drag_start)
            widget.bind("<B1-Motion>", on_drag)
            widget.bind("<Double-Button-1>", on_double_click)
            widget.bind("<Button-3>", lambda e: self._show_context_menu(e))  # Right click
            
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
        self.time_canvas.configure(bg=bg_color)
        self.labels_frame.configure(bg=bg_color)
        self.dies_label.configure(bg=bg_color, fg="lightgray")
        self.milidies_label.configure(bg=bg_color, fg="lightgray")
        self.progress_frame.configure(bg=bg_color)
        
        # Redraw time display with current background
        self._draw_time_display()
        
    def _draw_time_display(self):
        """Draw time text with black outline on canvas for better visibility."""
        try:
            # Clear canvas
            self.time_canvas.delete("all")
            
            # Get canvas dimensions
            canvas_width = self.time_canvas.winfo_width()
            canvas_height = self.time_canvas.winfo_height()
            
            if canvas_width <= 1:  # Not yet rendered
                self.master.after(10, self._draw_time_display)
                return
            
            # Current time text
            time_str = f"{self.day_index:03d}.{self.milliDies:03d}"
            
            # Font configuration
            try:
                font_spec = ("DejaVu Sans Mono", 28, "bold")
            except:
                font_spec = ("Courier New", 28, "bold")
            
            # Center position
            x_center = canvas_width // 2
            y_center = canvas_height // 2
            
            # Draw black outline (multiple offset positions)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:  # Skip center
                        self.time_canvas.create_text(
                            x_center + dx, y_center + dy,
                            text=time_str,
                            font=font_spec,
                            fill="black",
                            anchor="center"
                        )
            
            # Draw white text on top
            self.time_canvas.create_text(
                x_center, y_center,
                text=time_str,
                font=font_spec,
                fill="white",
                anchor="center"
            )
            
        except Exception as e:
            print(f"Time display drawing error: {e}")
        
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
            
            # Update progress bar for mikroDies (0-999)
            self._update_progress_bar()
            
            # Update theme (this will redraw time display)
            self._apply_theme()
            
        except Exception as e:
            print(f"Widget update error: {e}")
            # Fallback display
            self.day_index = 0
            self.milliDies = 0
            self.microDies = 0
            self._draw_time_display()
            
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
                    fill="#9ACD32", outline=""  # YellowGreen - high visibility on all sky gradients
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
        # Schedule next update in 86.4 ms (one mikroDies duration)
        self.update_job = self.master.after(86, self.start_updates)  # 86.4ms ≈ 86ms
        
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