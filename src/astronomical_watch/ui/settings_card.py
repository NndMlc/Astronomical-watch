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


class SettingsCard(tk.Toplevel):
    """Settings window with gradient background."""
    
    def __init__(self, master=None, lang="en", widget_ref=None):
        super().__init__(master)
        self.lang = lang
        self.widget_ref = widget_ref  # Reference to widget for applying settings
        
        self.title("Settings — Astronomical Watch")
        self.geometry("650x700")
        self.minsize(600, 650)
        
        # Get sky theme for gradient
        self.theme = get_sky_theme(datetime.now(timezone.utc))
        
        # Create canvas for gradient background
        self.canvas = tk.Canvas(self, width=650, height=700, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._draw_gradient()
        
        # Colors from theme
        self.text_color = self.theme.text_color
        self.bg_color = self.theme.bottom_color
        
        # Load current settings
        self.settings = self._load_settings()
        
        # Create UI
        self._make_widgets()
        
    def _draw_gradient(self):
        """Draw gradient background on canvas."""
        width = 650
        height = 700
        
        # Create gradient colors
        colors = create_gradient_colors(self.theme, steps=height)
        
        # Draw gradient as horizontal lines
        for i, color in enumerate(colors):
            self.canvas.create_line(0, i, width, i, fill=color, width=1)
    
    def _load_settings(self):
        """Load settings from config file."""
        config_path = os.path.expanduser("~/.astronomical_watch_config.json")
        default_settings = {
            "widget_position": {"x": None, "y": None},  # None = center
            "always_on_top": False,
            "load_on_startup": False,
            "opacity": 100,
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
        # Main scrollable container
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(
            main_frame,
            text="⚙️ Settings",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(pady=(0, 20))
        
        # === Widget Settings Section ===
        self._create_section(main_frame, "Widget Settings")
        
        widget_frame = tk.Frame(main_frame, bg=self.bg_color)
        widget_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Always on top checkbox
        self.always_on_top_var = tk.BooleanVar(value=self.settings["always_on_top"])
        always_on_top_cb = tk.Checkbutton(
            widget_frame,
            text="Keep widget always on top",
            variable=self.always_on_top_var,
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor="#333333",
            activebackground=self.bg_color,
            font=("Arial", 10)
        )
        always_on_top_cb.pack(anchor="w", pady=2)
        
        # Load on startup checkbox
        self.load_on_startup_var = tk.BooleanVar(value=self.settings["load_on_startup"])
        load_on_startup_cb = tk.Checkbutton(
            widget_frame,
            text="Load widget on system startup",
            variable=self.load_on_startup_var,
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor="#333333",
            activebackground=self.bg_color,
            font=("Arial", 10)
        )
        load_on_startup_cb.pack(anchor="w", pady=2)
        
        # Opacity slider
        opacity_frame = tk.Frame(widget_frame, bg=self.bg_color)
        opacity_frame.pack(fill=tk.X, pady=(10, 5))
        
        tk.Label(
            opacity_frame,
            text="Widget Opacity:",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.opacity_var = tk.IntVar(value=self.settings["opacity"])
        self.opacity_label = tk.Label(
            opacity_frame,
            text=f"{self.settings['opacity']}%",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10, "bold")
        )
        self.opacity_label.pack(side=tk.RIGHT)
        
        opacity_slider = tk.Scale(
            widget_frame,
            from_=50,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.opacity_var,
            command=self._update_opacity_label,
            bg=self.bg_color,
            fg=self.text_color,
            highlightthickness=0,
            troughcolor="#555555"
        )
        opacity_slider.pack(fill=tk.X, pady=(0, 5))
        
        # Widget position
        position_frame = tk.Frame(widget_frame, bg=self.bg_color)
        position_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            position_frame,
            text="Widget Position:",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        reset_pos_btn = tk.Button(
            position_frame,
            text="Reset to Center",
            command=self._reset_position,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9),
            padx=10,
            pady=3
        )
        reset_pos_btn.pack(side=tk.RIGHT)
        
        # === Info Section ===
        self._create_section(main_frame, "Application Info")
        
        info_frame = tk.Frame(main_frame, bg=self.bg_color)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Version
        self._add_info_row(info_frame, "Version:", "1.0.0 (2025-12)")
        
        # Python
        self._add_info_row(info_frame, "Python:", f"{sys.version.split()[0]}")
        
        # OS
        self._add_info_row(info_frame, "Operating System:", f"{platform.system()} {platform.release()}")
        
        # Timezone
        import time
        tz_name = time.tzname[0]
        self._add_info_row(info_frame, "System Timezone:", tz_name)
        
        # === License & Credits Section ===
        self._create_section(main_frame, "License & Credits")
        
        license_frame = tk.Frame(main_frame, bg=self.bg_color)
        license_frame.pack(fill=tk.X, pady=(0, 15))
        
        license_text = tk.Label(
            license_frame,
            text="Core algorithms: Astronomical Watch Core License (restrictive)\n"
                 "UI & Application: MIT License\n\n"
                 "© 2025 Astronomical Watch Project\n"
                 "github.com/NndMlc/Astronomical-watch",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        license_text.pack(anchor="w")
        
        # === Data & Privacy Section ===
        self._create_section(main_frame, "Data & Privacy")
        
        privacy_frame = tk.Frame(main_frame, bg=self.bg_color)
        privacy_frame.pack(fill=tk.X, pady=(0, 15))
        
        privacy_text = tk.Label(
            privacy_frame,
            text="🔒 This application works entirely offline.\n"
                 "No data is collected or sent to external servers.\n"
                 "Settings are stored locally in your home directory.",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        privacy_text.pack(anchor="w")
        
        # === Action Buttons ===
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Export settings
        export_btn = tk.Button(
            button_frame,
            text="📤 Export Settings",
            command=self._export_settings,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Reset to defaults
        reset_btn = tk.Button(
            button_frame,
            text="🔄 Reset to Defaults",
            command=self._reset_to_defaults,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        )
        reset_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save & Close
        save_btn = tk.Button(
            button_frame,
            text="💾 Save & Close",
            command=self._save_and_close,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        save_btn.pack(side=tk.RIGHT)
    
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
    
    def _update_opacity_label(self, value):
        """Update opacity label when slider moves."""
        self.opacity_label.config(text=f"{int(float(value))}%")
    
    def _reset_position(self):
        """Reset widget position to center."""
        self.settings["widget_position"] = {"x": None, "y": None}
        messagebox.showinfo("Position Reset", "Widget position will be centered on next launch.")
    
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
                "opacity": 100,
                "language": "en"
            }
            
            # Update UI
            self.always_on_top_var.set(False)
            self.load_on_startup_var.set(False)
            self.opacity_var.set(100)
            
            messagebox.showinfo("Reset Complete", "Settings have been reset to defaults.")
    
    def _save_and_close(self):
        """Save settings and close window."""
        # Update settings from UI
        self.settings["always_on_top"] = self.always_on_top_var.get()
        self.settings["load_on_startup"] = self.load_on_startup_var.get()
        self.settings["opacity"] = self.opacity_var.get()
        
        # Save to file
        if self._save_settings():
            # Apply settings to widget if reference exists
            if self.widget_ref and hasattr(self.widget_ref, 'apply_settings'):
                self.widget_ref.apply_settings(self.settings)
            
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
            self.destroy()


def create_settings_card(master=None, lang="en", widget_ref=None):
    """Factory function to create SettingsCard instance."""
    return SettingsCard(master, lang, widget_ref)
