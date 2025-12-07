"""Settings Card for Astronomical Watch

Provides configuration options for widget behavior, display preferences,
and application information.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
import platform
from datetime import datetime, timezone
from .gradient import get_sky_theme, create_gradient_colors
from .theme_manager import get_shared_theme
from .translations import TRANSLATIONS

def tr(key: str, lang: str = "en") -> str:
    """Simple translation function."""
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS.get("en", {}).get(key, key))


class SettingsCard(tk.Toplevel):
    """Settings window with gradient background."""
    
    def __init__(self, master=None, lang="en", widget_ref=None):
        super().__init__(master)
        self.lang = lang
        self.widget_ref = widget_ref  # Reference to widget for applying settings
        
        self.title("Settings — Astronomical Watch")
        self.geometry("400x700")
        self.minsize(380, 650)
        
        # Remove window decorations (minimize/maximize buttons)
        self.overrideredirect(True)
        
        # Get sky theme for gradient
        self.theme = get_shared_theme()
        
        # Create canvas for gradient background
        self.canvas = tk.Canvas(self, width=400, height=700, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._draw_gradient()
        
        # Colors from theme
        self.text_color = self.theme.text_color
        self.bg_color = self.theme.bottom_color
        
        # Load current settings
        self.settings = self._load_settings()
        
        # Create UI
        self._make_widgets()
        
        # Setup drag functionality
        self._setup_dragging()
        
    def _draw_gradient(self):
        """Draw gradient background on canvas."""
        width = 400
        height = 700
        
        # Create gradient colors
        colors = create_gradient_colors(self.theme, steps=height)
        
        # Draw gradient as horizontal lines
        for i, color in enumerate(colors):
            self.canvas.create_line(0, i, width, i, fill=color, width=1)
    
    def _setup_dragging(self):
        """Setup window dragging functionality on background elements."""
        self._drag_data = {"x": 0, "y": 0}
        
        def start_drag(event):
            self._drag_data["x"] = event.x_root
            self._drag_data["y"] = event.y_root
            
        def do_drag(event):
            deltax = event.x_root - self._drag_data["x"]
            deltay = event.y_root - self._drag_data["y"]
            
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            
            self.geometry(f"+{x}+{y}")
            
            self._drag_data["x"] = event.x_root
            self._drag_data["y"] = event.y_root
        
        # Bind to canvas background
        self.canvas.bind("<Button-1>", start_drag)
        self.canvas.bind("<B1-Motion>", do_drag)
    
    def _load_settings(self):
        """Load settings from config file."""
        config_path = os.path.expanduser("~/.astronomical_watch_config.json")
        default_settings = {
            "widget_position": {"x": None, "y": None},
            "always_on_top": False,
            "load_on_startup": True,
            "transparent_background": False,
            "language": "en"
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
            except:
                pass
        
        return default_settings
    
    def _save_settings(self):
        """Save settings to config file."""
        config_path = os.path.expanduser("~/.astronomical_watch_config.json")
        try:
            with open(config_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            return False
    
    def _make_widgets(self):
        """Create all settings widgets."""
        # Main container
        outer_frame = tk.Frame(self, bg=self.bg_color)
        outer_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # === Top: Title with close button (fixed) ===
        title_frame = tk.Frame(outer_frame, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title = tk.Label(
            title_frame,
            text=tr("settings_title", self.lang),
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(side=tk.LEFT)
        
        close_btn = tk.Button(
            title_frame,
            text="✕",
            command=self.destroy,
            bg="#FF5252",
            fg="white",
            font=("Arial", 14, "bold"),
            width=3,
            relief=tk.FLAT
        )
        close_btn.pack(side=tk.RIGHT)
        
        # === Middle: Scrollable content ===
        scroll_container = tk.Frame(outer_frame, bg=self.bg_color)
        scroll_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create canvas for scrolling
        canvas = tk.Canvas(scroll_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        
        # Scrollable frame inside canvas
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Content frame (this will be scrollable)
        main_frame = tk.Frame(scrollable_frame, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # === Widget Settings Section ===
        self._create_section(main_frame, tr("widget_settings", self.lang))
        
        widget_frame = tk.Frame(main_frame, bg=self.bg_color)
        widget_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Always on top checkbox
        self.always_on_top_var = tk.BooleanVar(value=self.settings["always_on_top"])
        always_on_top_cb = tk.Checkbutton(
            widget_frame,
            text=tr("always_on_top", self.lang),
            variable=self.always_on_top_var,
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor="white",
            activebackground=self.bg_color,
            font=("Arial", 10)
        )
        always_on_top_cb.pack(anchor="w", pady=2)
        
        # Load on startup checkbox
        self.load_on_startup_var = tk.BooleanVar(value=self.settings["load_on_startup"])
        load_on_startup_cb = tk.Checkbutton(
            widget_frame,
            text=tr("load_on_startup", self.lang),
            variable=self.load_on_startup_var,
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor="white",
            activebackground=self.bg_color,
            font=("Arial", 10)
        )
        load_on_startup_cb.pack(anchor="w", pady=2)
        
        # Transparent background checkbox - Windows only
        if platform.system() == "Windows":
            self.transparent_var = tk.BooleanVar(value=self.settings.get("transparent_background", False))
            transparent_checkbutton = tk.Checkbutton(
                widget_frame,
                text=tr("transparent_bg", self.lang),
                variable=self.transparent_var,
                command=self._update_transparency_live,
                bg=self.bg_color,
                fg=self.text_color,
                selectcolor="white",
                activebackground=self.bg_color,
                font=("Arial", 10)
            )
            transparent_checkbutton.pack(anchor="w", pady=5)
        else:
            # Linux/macOS: Feature not available
            self.transparent_var = tk.BooleanVar(value=False)
        
        # === Info Section ===
        self._create_section(main_frame, tr("app_info", self.lang))
        
        info_frame = tk.Frame(main_frame, bg=self.bg_color)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Version
        self._add_info_row(info_frame, tr("version", self.lang), "1.0.0 (2025-12)")
        
        # Python
        self._add_info_row(info_frame, tr("python", self.lang), f"{sys.version.split()[0]}")
        
        # OS
        self._add_info_row(info_frame, tr("os", self.lang), f"{platform.system()} {platform.release()}")
        
        # Timezone
        import time
        tz_name = time.tzname[0]
        self._add_info_row(info_frame, tr("system_timezone", self.lang), tz_name)
        
        # === License & Credits Section ===
        self._create_section(main_frame, tr("license_credits", self.lang))
        
        license_frame = tk.Frame(main_frame, bg=self.bg_color)
        license_frame.pack(fill=tk.X, pady=(0, 15))
        
        license_text = tk.Label(
            license_frame,
            text=tr("license_text", self.lang),
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        license_text.pack(anchor="w")
        
        # === Data & Privacy Section ===
        self._create_section(main_frame, tr("data_privacy", self.lang))
        
        privacy_frame = tk.Frame(main_frame, bg=self.bg_color)
        privacy_frame.pack(fill=tk.X, pady=(0, 15))
        
        privacy_text = tk.Label(
            privacy_frame,
            text=tr("privacy_text", self.lang),
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        privacy_text.pack(anchor="w")
        
        # === Bottom: Action Buttons (fixed) ===
        button_frame = tk.Frame(outer_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Save & Close (centered)
        save_btn = tk.Button(
            button_frame,
            text=tr("save_close", self.lang),
            command=self._save_and_close,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=30,
            pady=10
        )
        save_btn.pack(expand=True)
    
    def _create_section(self, parent, title):
        """Create a section header."""
        section_frame = tk.Frame(parent, bg=self.bg_color)
        section_frame.pack(fill=tk.X, pady=(15, 5))
        
        label = tk.Label(
            section_frame,
            text=title,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 12, "bold")
        )
        label.pack(anchor="w")
        
        # Separator line
        separator = tk.Frame(parent, height=1, bg="#555555")
        separator.pack(fill=tk.X, pady=(0, 10))
    
    def _add_info_row(self, parent, label_text, value_text):
        """Add an info row with label and value."""
        row = tk.Frame(parent, bg=self.bg_color)
        row.pack(fill=tk.X, pady=2)
        
        label = tk.Label(
            row,
            text=label_text,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 9, "bold"),
            width=20,
            anchor="w"
        )
        label.pack(side=tk.LEFT)
        
        value = tk.Label(
            row,
            text=value_text,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 9)
        )
        value.pack(side=tk.LEFT)
    
    def _update_transparency_live(self):
        """Update transparency setting and apply to widget immediately."""
        transparent = self.transparent_var.get()
        
        # Apply to widget in real-time
        if self.widget_ref and hasattr(self.widget_ref, 'set_transparent_mode'):
            try:
                self.widget_ref.set_transparent_mode(transparent)
            except Exception as e:
                print(f"⚠️ Could not update widget transparency: {e}")
                pass
    
    def _export_settings(self):
        """Export settings to a JSON file."""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Settings"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.settings, f, indent=2)
                messagebox.showinfo("Success", f"Settings exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export settings:\n{e}")
    
    def _reset_to_defaults(self):
        """Reset all settings to defaults."""
        result = messagebox.askyesno(
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?\n\n"
            "This action cannot be undone."
        )
        
        if result:
            self.settings = {
                "widget_position": {"x": None, "y": None},
                "always_on_top": False,
                "load_on_startup": False,
                "transparent_background": False,
                "language": "en"
            }
            
            # Update UI
            self.always_on_top_var.set(False)
            self.load_on_startup_var.set(False)
            self.transparent_var.set(False)
            
            messagebox.showinfo("Reset Complete", "Settings have been reset to defaults.")
    
    def _save_and_close(self):
        """Save settings and close window."""
        # Update settings from UI
        self.settings["always_on_top"] = self.always_on_top_var.get()
        self.settings["load_on_startup"] = self.load_on_startup_var.get()
        self.settings["transparent_background"] = self.transparent_var.get()
        
        # Save to file
        if self._save_settings():
            # Apply settings to widget if reference exists
            if self.widget_ref and hasattr(self.widget_ref, 'apply_settings'):
                self.widget_ref.apply_settings(self.settings)
            
            # Destroy window without showing message box (it blocks)
            self.destroy()
            print("✅ Settings saved and applied")


def create_settings_card(master=None, lang="en", widget_ref=None):
    """Factory function to create SettingsCard instance."""
    return SettingsCard(master, lang, widget_ref)
