"""
Astronomical Watch Widget - Small corner display
"""
from __future__ import annotations
import tkinter as tk
from datetime import datetime, timezone
from typing import Optional, Callable
import random
import math
from .gradient import get_sky_theme
from .translations import tr

from src.astronomical_watch.core.astro_time_core import AstroYear

class AstronomicalWidgetMode:
    def __init__(self, master: tk.Widget = None, on_click_callback: Optional[Callable] = None):
        self.master = master or tk.Tk()
        self.master.title("Astronomical Watch - Widget")
        self.master.geometry("140x70")
        self.master.minsize(140, 70)
        
        # Set icon if available
        self._set_icon()
        
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
        self.dies = 0
        self.miliDies = 0
        self.mikroDies = 0
        
        # Current language for title
        self.current_language = "en"
        
        # Update job reference
        self.update_job = None
        
        # Fireworks state
        self.fireworks_active = False
        self.fireworks_particles = []
        self.fireworks_job = None
        
        self._create_widgets()
        self._apply_theme()
        
        # Load and apply settings
        self._load_and_apply_settings()
        
        # Bind click event to entire widget
        self._bind_click_events()
        
    def _create_widgets(self):
        """Create minimalistic UI elements - only numbers and progress bar."""
        # Main frame with minimal padding
        self.frame = tk.Frame(self.master, bd=0, relief='flat')
        self.frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Single canvas for everything (time display + progress bar)
        self.canvas = tk.Canvas(
            self.frame,
            width=136,  # Fit in 140px widget width
            height=66,  # Fit in 70px widget height
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Create context menu
        self._create_context_menu()
        
    def _set_icon(self):
        """Set application icon if available."""
        import os
        try:
            # Get the root directory of the project
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
            icon_path = os.path.join(project_root, "icons", "astronomical_watch.ico")
            
            if os.path.exists(icon_path):
                self.master.iconbitmap(icon_path)
            else:
                # Try alternative icon formats
                for icon_file in ["astronomical_watch.png", "astronomical_watch.gif", "icon.ico", "icon.png"]:
                    alt_path = os.path.join(project_root, "icons", icon_file)
                    if os.path.exists(alt_path):
                        # For PNG files, we need to use PhotoImage
                        if alt_path.endswith('.png'):
                            img = tk.PhotoImage(file=alt_path)
                            self.master.iconphoto(True, img)
                        else:
                            self.master.iconbitmap(alt_path)
                        break
        except Exception:
            # Ignore icon errors - not critical for functionality
            pass
        
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
        
        self.master.configure(bg=bg_color)
        self.frame.configure(bg=bg_color)
        
        # Update canvas background
        self.canvas.configure(bg=bg_color)
        
        # Redraw time display with current background
        self._draw_time_display()
        
    def _draw_time_display(self):
        """Draw time text with black outline on canvas for better visibility."""
        try:
            # Clear canvas
            self.canvas.delete("all")
            
            # Get canvas dimensions
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1:  # Not yet rendered
                self.master.after(10, self._draw_time_display)
                return
            
            # Current time text
            time_str = f"{self.dies:03d}.{self.miliDies:03d}"
            
            # Font configuration for smaller widget
            try:
                font_spec = ("DejaVu Sans Mono", 16, "bold")
            except:
                font_spec = ("Courier New", 16, "bold")
            
            # Position for time text (upper part of canvas)
            x_center = canvas_width // 2
            y_time = 20  # Upper position for time
            
            # Draw black outline (multiple offset positions)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:  # Skip center
                        self.canvas.create_text(
                            x_center + dx, y_time + dy,
                            text=time_str,
                            font=font_spec,
                            fill="black",
                            anchor="center"
                        )
            
            # Draw white text on top
            self.canvas.create_text(
                x_center, y_time,
                text=time_str,
                font=font_spec,
                fill="white",
                anchor="center"
            )
            
            # Show countdown if < 11 dies remaining
            if hasattr(self, 'remaining_dies') and self.remaining_dies < 11:
                countdown_str = tr("countdown_label", self.current_language, 
                                  dies=self.remaining_dies, milidies=self.remaining_milidies)
                countdown_font = ("Arial", 8)
                y_countdown = 38
                
                # Draw countdown with outline
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            self.canvas.create_text(
                                x_center + dx, y_countdown + dy,
                                text=countdown_str,
                                font=countdown_font,
                                fill="black",
                                anchor="center"
                            )
                
                self.canvas.create_text(
                    x_center, y_countdown,
                    text=countdown_str,
                    font=countdown_font,
                    fill="#FFD700",  # Gold color for countdown
                    anchor="center"
                )
            
            # Draw progress bar in lower part
            self._draw_progress_bar()
            
        except Exception as e:
            print(f"Time display drawing error: {e}")
            
    def _draw_progress_bar(self):
        """Draw mikroDies progress bar on canvas."""
        try:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Progress bar dimensions
            bar_width = canvas_width - 20  # 10px margins
            bar_height = 8
            bar_x = 10
            bar_y = canvas_height - 20  # Near bottom
            
            # Calculate progress (0-999 mikroDies)
            progress = self.mikroDies / 999.0
            
            # Draw background bar (dark gray)
            self.canvas.create_rectangle(
                bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                fill="gray20", outline="gray40"
            )
            
            # Draw progress bar (YellowGreen)
            progress_width = int(bar_width * progress)
            if progress_width > 0:
                self.canvas.create_rectangle(
                    bar_x, bar_y, bar_x + progress_width, bar_y + bar_height,
                    fill="#9ACD32", outline=""
                )
                
        except Exception as e:
            print(f"Progress bar drawing error: {e}")
        
    def _update_display(self):
        """Update the astronomical time display."""
        try:
            from ..core.equinox import compute_vernal_equinox
            
            # Get current time
            now_utc = datetime.now(timezone.utc)
            
            # Use computed equinox values
            current_year = now_utc.year
            current_equinox = compute_vernal_equinox(current_year)
            next_equinox = compute_vernal_equinox(current_year + 1)
            
            # Check if we're before this year's equinox
            if now_utc < current_equinox:
                current_equinox = compute_vernal_equinox(current_year - 1)
                next_equinox = compute_vernal_equinox(current_year)
            
            # Create AstroYear and get reading
            astro_year = AstroYear(current_equinox, next_equinox)
            reading = astro_year.reading(now_utc)
            
            # Update display values
            self.dies = reading.dies
            self.miliDies = reading.miliDies
            self.mikroDies = reading.mikroDies
            
            # Calculate countdown to next equinox
            year_length_seconds = (next_equinox - current_equinox).total_seconds()
            year_length_dies = int(year_length_seconds / 86400.0)
            
            self.remaining_dies = year_length_dies - self.dies
            self.remaining_milidies = 1000 - self.miliDies
            
            if self.remaining_milidies == 1000:
                self.remaining_milidies = 0
                self.remaining_dies += 1
            
            # Check for equinox moment (Dies 000, miliDies 000-005)
            if self.dies == 0 and self.miliDies < 5 and not self.fireworks_active:
                self._start_fireworks()
            elif self.dies > 0 and self.fireworks_active:
                self._stop_fireworks()
            
            # Update theme (this will redraw time display)
            self._apply_theme()
            
        except Exception as e:
            print(f"Widget update error: {e}")
            # Fallback display
            self.dies = 0
            self.miliDies = 0
            self.mikroDies = 0
            self.remaining_dies = 999
            self.remaining_milidies = 999
            self._draw_time_display()
    
    def _start_fireworks(self):
        """Start fireworks animation for equinox celebration"""
        print("🎆 Starting fireworks animation in widget!")
        self.fireworks_active = True
        self.fireworks_particles = []
        self._animate_fireworks()
    
    def _stop_fireworks(self):
        """Stop fireworks animation"""
        if self.fireworks_job:
            self.master.after_cancel(self.fireworks_job)
            self.fireworks_job = None
        self.fireworks_active = False
        self.fireworks_particles = []
    
    def _create_firework(self):
        """Create a new firework burst"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Random starting position
        x = random.randint(20, canvas_width - 20)
        y = random.randint(20, canvas_height - 40)
        
        # Random color
        colors = ["#FFD700", "#FF6347", "#00FF00", "#00BFFF", "#FF69B4", "#FFA500", "#FFFF00"]
        color = random.choice(colors)
        
        # Create particles radiating outward
        num_particles = 15
        for i in range(num_particles):
            angle = (2 * math.pi * i) / num_particles
            speed = random.uniform(1.5, 3.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            self.fireworks_particles.append({
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'color': color,
                'life': 30,  # frames
                'size': 3
            })
    
    def _animate_fireworks(self):
        """Animate fireworks particles"""
        if not self.fireworks_active:
            return
        
        # Create new firework occasionally
        if random.random() < 0.15:  # 15% chance per frame
            self._create_firework()
        
        # Update and draw particles
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Update particles
        for particle in self.fireworks_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.15  # Gravity
            particle['life'] -= 1
            
            # Remove dead particles
            if particle['life'] <= 0 or particle['y'] > canvas_height:
                self.fireworks_particles.remove(particle)
        
        # Redraw display with particles
        self._draw_time_display()
        
        # Draw fireworks particles on top
        for particle in self.fireworks_particles:
            alpha = particle['life'] / 30.0
            size = max(1, int(particle['size'] * alpha))
            self.canvas.create_oval(
                particle['x'] - size, particle['y'] - size,
                particle['x'] + size, particle['y'] + size,
                fill=particle['color'],
                outline=""
            )
        
        # Schedule next frame
        self.fireworks_job = self.master.after(50, self._animate_fireworks)  # ~20 FPS
            
    def set_language(self, language: str):
        """Update widget language."""
        self.current_language = language
        # Force immediate update to reflect language change
        self._update_display()
    
    def _load_and_apply_settings(self):
        """Load settings from config file and apply them."""
        import json
        import os
        
        config_path = os.path.expanduser("~/.astronomical_watch_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    settings = json.load(f)
                    self.apply_settings(settings)
            except Exception as e:
                print(f"⚠️ Failed to load settings: {e}")
    
    def apply_settings(self, settings: dict):
        """Apply settings to widget.
        
        Args:
            settings: Dictionary with keys:
                - always_on_top: bool
                - opacity: int (50-100)
                - widget_position: dict with x, y (or None for center)
        """
        # Always on top
        if "always_on_top" in settings:
            self._always_on_top = settings["always_on_top"]
            self.master.attributes('-topmost', self._always_on_top)
        
        # Opacity (convert percentage to 0.0-1.0)
        if "opacity" in settings:
            opacity_value = settings["opacity"] / 100.0
            self.master.attributes('-alpha', opacity_value)
        
        # Position
        if "widget_position" in settings:
            pos = settings["widget_position"]
            if pos.get("x") is not None and pos.get("y") is not None:
                self.master.geometry(f"+{pos['x']}+{pos['y']}")
            # If None, leave at current position (already centered by default)
        
        print(f"✅ Applied settings to widget")
            
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