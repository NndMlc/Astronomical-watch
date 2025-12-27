"""
Astronomical Watch Normal Mode - Modern UI Design

A clean, modern interface without traditional window decorations.
Features custom title bar with language selector and close button.
Main content shows astronomical time values in hierarchical layout.
"""

import tkinter as tk
from tkinter import ttk, font as tk_font
import math
import json
import os
import random
from datetime import datetime, timezone
from ..core.astro_time_core import AstroYear
from .gradient import get_sky_theme, create_gradient_colors
from .theme_manager import get_shared_theme
from .translations import TRANSLATIONS
from .comparison_card import create_comparison_card
from .settings_card import create_settings_card

# Detect available monospace font
def get_monospace_font(size=14):
    """Get the best available monospace font."""
    try:
        available_fonts = tk_font.families()
    except:
        # Fallback if no root window exists yet
        return ("DejaVu Sans Mono", size, "bold")
    
    preferred_fonts = [
        "DejaVu Sans Mono",
        "Liberation Mono", 
        "Consolas",
        "Monaco",
        "Courier New",
        "Courier"
    ]
    
    for font_name in preferred_fonts:
        if font_name in available_fonts:
            return (font_name, size, "bold")
    
    return ("monospace", size, "bold")  # Fallback

# Language options - all 20 languages from translations.py
LANGUAGES = [
    ("English", "en"),
    ("中文 (Chinese)", "zh"),
    ("हिन्दी (Hindi)", "hi"),
    ("Español", "es"),
    ("Français", "fr"),
    ("العربية (Arabic)", "ar"),
    ("বাংলা (Bengali)", "bn"),
    ("Português", "pt"),
    ("Русский (Russian)", "ru"),
    ("اردو (Urdu)", "ur"),
    ("Bahasa Indonesia", "id"),
    ("Deutsch", "de"),
    ("日本語 (Japanese)", "ja"),
    ("Kiswahili", "sw"),
    ("Türkçe", "tr"),
    ("한국어 (Korean)", "ko"),
    ("Tiếng Việt (Vietnamese)", "vi"),
    ("Italiano", "it"),
    ("فارسی (Persian)", "fa"),
    ("Polski", "pl"),
    ("Hausa", "ha"),
    ("Kurdî (Kurdish)", "ku"),
    ("Nederlands", "nl"),
    ("Română (Romanian)", "ro"),
    ("Српскохрватски (Serbo-Croatian)", "sr"),
    ("isiZulu (Zulu)", "zu"),
    ("עברית (Hebrew)", "he"),
    ("Ελληνικά (Greek)", "el")
]

def tr(key: str, lang: str = "en") -> str:
    """Simple translation function."""
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS.get("en", {}).get(key, key))


class ModernNormalMode:
    """Modern Normal Mode without window decorations."""
    
    def __init__(self, parent, on_back=None, on_language=None, widget_ref=None):
        print("🚀 ModernNormalMode.__init__ starting...")
        self.master = parent
        self.on_back = on_back
        self.on_language = on_language
        self.widget_ref = widget_ref  # Store widget reference for settings

        # Data initialization first
        self.dies = 0
        self.miliDies = 0
        self.mikroDies = 0
        # Load language from config ako postoji
        self.current_language = self._load_language_setting()
        self.lang = self.current_language  # Alias for compatibility

        # Theme state
        self.current_theme = None
        self.gradient_canvas = None
        self.shared_theme_func = None  # Function to get shared theme from widget

        # Update timer
        self._update_job = None

        # Fireworks state
        self.fireworks_active = False
        self.fireworks_particles = []
        self.fireworks_job = None

        # Active tab
        self.current_tab = "explanation"

        # Track open windows to prevent duplicates
        self.open_windows = {
            "explanation": None,
            "comparison": None,
            "settings": None
        }

        # Window configuration
        self.window_width = 480
        self.window_height = 550

        print("📐 Setting up window...")

        try:
            # Remove window decorations
            self.master.overrideredirect(True)
            print("✅ Window decorations removed")
            # Update window to ensure it's ready for geometry operations
            self.master.update_idletasks()
            # Center the window
            self._center_window()
            print("✅ Window centered")
            # Create icons
            self._create_icons()
            print("✅ Icons created")
            # Create UI
            self._create_ui()
            print("✅ UI created")
            # Apply theme once after UI is created
            self._apply_theme()
            print("✅ Theme applied")
            # Start time updates
            self.start_updates()
            print("✅ Time updates started")
            print("🎉 ModernNormalMode initialization complete!")
        except Exception as e:
            print(f"❌ ModernNormalMode initialization failed: {e}")
            import traceback
            traceback.print_exc()
            raise

    def _load_language_setting(self):
        """Load language from config file if exists, else default to 'en'."""
        config_path = os.path.expanduser("~/.astronomical_watch_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    lang = data.get("language", "en")
                    if isinstance(lang, str) and len(lang) == 2:
                        return lang
            except Exception:
                pass
        return "en"


    def _save_language_setting(self, lang_code):
        """Sačuvaj jezik u config fajl, čuvajući ostala podešavanja ako postoje."""
        config_path = os.path.expanduser("~/.astronomical_watch_config.json")
        data = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
            except Exception:
                data = {}
        data["language"] = lang_code
        try:
            with open(config_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
        
        print("📐 Setting up window...")
        
        try:
            # Remove window decorations
            self.master.overrideredirect(True)
            print("✅ Window decorations removed")
            
            # Update window to ensure it's ready for geometry operations
            self.master.update_idletasks()
            
            # Center the window
            self._center_window()
            print("✅ Window centered")
            
            # Create icons
            self._create_icons()
            print("✅ Icons created")
            
            # Create UI
            self._create_ui()
            print("✅ UI created")
            
            # Apply theme once after UI is created
            self._apply_theme()
            print("✅ Theme applied")
            
            # Start time updates
            self.start_updates()
            print("✅ Time updates started")
            
            print("🎉 ModernNormalMode initialization complete!")
            
        except Exception as e:
            print(f"❌ ModernNormalMode initialization failed: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def _center_window(self):
        """Center the window on screen."""
        try:
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            
            x = (screen_width - self.window_width) // 2
            y = (screen_height - self.window_height) // 2
            
            self.master.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
            print(f"📱 Window centered: {self.window_width}x{self.window_height} at {x},{y}")
            
        except Exception as e:
            print(f"⚠️ Could not center window, using default position: {e}")
            # Fallback to default size and position
            self.master.geometry(f"{self.window_width}x{self.window_height}")
        
    def _create_icons(self):
        """Create simple text-based icons."""
        self.icons = {
            "info": "ⓘ",
            "compare": "⇄", 
            "calc": "🧮",
            "settings": "⚙️"
        }
        
    def _get_current_theme(self):
        """Get current theme - uses shared theme for consistency."""
        return get_shared_theme()
        
    def _create_ui(self):
        """Create the modern UI layout."""
        try:
            print("🎨 Creating UI layout...")
            
            # Get initial theme colors
            theme = self._get_current_theme()
            bg_color = theme.bottom_color if theme else "#60a5fa"  # Use bottom color for gradient
            print(f"🎨 Canvas background color will be: {bg_color}")
            
            # Create gradient background canvas first
            self.gradient_canvas = tk.Canvas(
                self.master,
                highlightthickness=0,
                relief='flat',
                borderwidth=0,
                bg=bg_color  # Use theme color
            )
            self.gradient_canvas.pack(fill=tk.BOTH, expand=True)
            print("✅ Gradient canvas created")
            
            # Bind canvas resize to update gradient
            self.gradient_canvas.bind('<Configure>', self._on_canvas_resize)
            
            # Main container over gradient - match gradient color
            canvas_bg = theme.top_color  # Use gradient start color
            self.main_frame = tk.Frame(self.gradient_canvas, bg=canvas_bg, relief='flat', bd=0)
            self.canvas_frame_id = self.gradient_canvas.create_window(
                0, 0, anchor=tk.NW, window=self.main_frame
            )
            print(f"✅ Main frame created with gradient top color: {canvas_bg}")
            
            # Custom title bar
            self._create_title_bar()
            print("✅ Title bar created")
            
            # Time display area
            self._create_time_display()
            print("✅ Time display created")
            
            # Standard time display
            self._create_standard_time()
            print("✅ Standard time display created")
            
            # Tab buttons
            self._create_tab_buttons()
            print("✅ Tab buttons created")
            
            # Enable window dragging
            self._setup_dragging()
            print("✅ Window dragging enabled")
            
        except Exception as e:
            print(f"❌ UI creation failed: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def _get_gradient_color_at_position(self, relative_y=0.0):
        """Get interpolated gradient color at relative Y position (0.0 to 1.0)."""
        if not hasattr(self, 'current_theme') or not self.current_theme:
            return "#2563eb"  # Fallback
        
        theme = self.current_theme
        # Interpolate between top and bottom colors
        top_rgb = self.master.winfo_rgb(theme.top_color)
        bottom_rgb = self.master.winfo_rgb(theme.bottom_color)
        
        # Interpolate each color channel
        r = int(top_rgb[0] + (bottom_rgb[0] - top_rgb[0]) * relative_y) // 256
        g = int(top_rgb[1] + (bottom_rgb[1] - top_rgb[1]) * relative_y) // 256
        b = int(top_rgb[2] + (bottom_rgb[2] - top_rgb[2]) * relative_y) // 256
        
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def _create_title_bar(self):
        """Create custom title bar with language selector and close button."""
        # Use solid theme color
        theme = self._get_current_theme()
        bg_color = theme.top_color
        
        self.title_bar = tk.Frame(self.main_frame, height=50, bg=bg_color, relief='flat', bd=0)
        self.title_bar.pack(fill=tk.X)
        self.title_bar.pack_propagate(False)
        
        # Close button (right side first) 
        self.close_button = tk.Button(
            self.title_bar,
            text="✕",
            bg="#ff4444", 
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            width=3,
            height=1,
            command=self._close_window
        )
        self.close_button.pack(side=tk.RIGHT, padx=10, pady=8)
        
        # Language selector (left side)
        self.lang_frame = tk.Frame(self.title_bar, bg=bg_color)
        self.lang_frame.pack(side=tk.LEFT, padx=10, pady=8)
        
        self.lang_button = tk.Button(
            self.lang_frame, 
            text="🌐 EN", 
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=5,
            command=self._show_language_menu
        )
        self.lang_button.pack()
        
        # Title (center) - use place for absolute centering
        self.title_label = tk.Label(
            self.title_bar,
            text="Astronomical Watch", 
            font=("Arial", 14, "bold"),
            bg=bg_color,
            fg="#e2e8f0"
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def _create_time_display(self):
        """Create the main time display area with proper grid layout."""
        # Use solid theme color
        theme = self._get_current_theme()
        bg_color = theme.top_color
        text_color = "#e2e8f0"  # Light gray text for dark background
        
        self.time_frame = tk.Frame(self.main_frame, bg=bg_color, relief='flat', bd=0)
        self.time_frame.pack(fill=tk.X, pady=5)
        
        # Configure grid columns for consistent layout
        self.time_frame.grid_columnconfigure(0, weight=1, minsize=120)  # Label column
        self.time_frame.grid_columnconfigure(1, weight=2, minsize=200)  # Value column
        
        # Dies display
        self.dies_label_text = tk.Label(
            self.time_frame,
            text="Dies:",
            font=("Arial", 14, "bold"),
            anchor="e",
            bg=bg_color,
            fg=text_color
        )
        self.dies_label_text.grid(row=0, column=0, padx=(15, 8), pady=5, sticky="e")
        
        self.dies_label = tk.Label(
            self.time_frame,
            text="000",
            font=get_monospace_font(48),
            anchor="w",
            bg=bg_color,
            fg=text_color
        )
        self.dies_label.grid(row=0, column=1, padx=(8, 15), pady=5, sticky="w")
        
        # MiliDies display
        self.milidies_label_text = tk.Label(
            self.time_frame,
            text="miliDies:",
            font=("Arial", 14, "bold"),
            anchor="e",
            bg=bg_color,
            fg=text_color
        )
        self.milidies_label_text.grid(row=1, column=0, padx=(15, 8), pady=5, sticky="e")
        
        self.milidies_label = tk.Label(
            self.time_frame,
            text="000",
            font=get_monospace_font(48),
            anchor="w",
            bg=bg_color,
            fg=text_color
        )
        self.milidies_label.grid(row=1, column=1, padx=(8, 15), pady=5, sticky="w")
        
        # MikroDies display
        self.mikrodies_label_text = tk.Label(
            self.time_frame,
            text="mikroDies:",
            font=("Arial", 14, "bold"),
            anchor="e",
            bg=bg_color,
            fg=text_color
        )
        self.mikrodies_label_text.grid(row=2, column=0, padx=(15, 8), pady=5, sticky="e")
        
        self.mikrodies_label = tk.Label(
            self.time_frame,
            text="000",
            font=get_monospace_font(48),
            anchor="w",
            bg=bg_color,
            fg=text_color
        )
        self.mikrodies_label.grid(row=2, column=1, padx=(8, 15), pady=5, sticky="w")
        
    def _create_standard_time(self):
        """Create standard time display section."""
        # Use solid theme color
        theme = self._get_current_theme()
        bg_color = theme.top_color
        text_color = "#e2e8f0"  # Light gray text for dark background
        
        # Add visual separator
        separator_frame = tk.Frame(self.main_frame, height=2, bg=bg_color, relief='flat', bd=0)
        separator_frame.pack(fill=tk.X, pady=20)
        separator_frame.pack_propagate(False)
        
        self.std_time_frame = tk.Frame(self.main_frame, bg=bg_color, relief='flat', bd=0)
        self.std_time_frame.pack(fill=tk.X, pady=5)
        
        # Label for standard time
        self.std_time_label_text = tk.Label(
            self.std_time_frame,
            text=tr("standard_time", self.current_language),
            font=("Arial", 14),
            bg=bg_color,
            fg=text_color
        )
        self.std_time_label_text.pack(pady=(0, 5))
        
        self.std_time_label = tk.Label(
            self.std_time_frame,
            text="Loading...",
            font=("Arial", 16, "bold"),
            bg=bg_color,
            fg=text_color
        )
        self.std_time_label.pack()
        
        # Countdown label (pokazuje se samo kad je < 11 dies)
        self.countdown_label = tk.Label(
            self.std_time_frame,  # Koristimo std_time_frame koji koristi pack()
            text="",
            font=("Arial", 11, "italic"),
            bg=bg_color,
            fg="#FFD700"  # Gold color
        )
        self.countdown_label.pack(pady=(5, 0))
        
    def _create_tab_buttons(self):
        """Create tab navigation buttons with icons."""
        # Use solid theme color
        theme = self._get_current_theme()
        bg_color = theme.top_color
        text_color = "#e2e8f0"  # Light gray text for dark background
        
        self.tab_frame = tk.Frame(self.main_frame, bg=bg_color, relief='flat', bd=0)
        self.tab_frame.pack(fill=tk.X, pady=5)
        
        # Center the buttons
        button_container = tk.Frame(self.tab_frame, bg=bg_color, relief='flat', bd=0)
        button_container.pack()
        
        self.tab_buttons = {}
        self.tab_tooltip_keys = {}  # Store tooltip translation keys
        
        # Tab definitions with translation keys for tooltips
        tabs = [
            ("explanation", self.icons["info"], "explanation"),
            ("comparison", self.icons["compare"], "comparison"), 
            ("settings", self.icons["settings"], "settings_title")  # Use settings_title and strip emoji
        ]
        
        for tab_id, icon, tooltip_key in tabs:
            btn = tk.Button(
                button_container,
                text=icon,
                font=("Arial", 24, "bold"),
                relief=tk.FLAT,
                width=4,
                height=2,
                bg="#4a5568",  # Lighter gray for visibility
                fg=text_color,
                activebackground="#2d3748",  # Dark gray active
                activeforeground=text_color,
                command=lambda t=tab_id: self._switch_tab(t)
            )
            btn.pack(side=tk.LEFT, padx=8)
            self.tab_buttons[tab_id] = btn
            self.tab_tooltip_keys[tab_id] = tooltip_key  # Store key for updates
            
            # Add tooltip with translated text (strip emoji from settings_title)
            tooltip_text = tr(tooltip_key, self.current_language)
            if tooltip_key == "settings_title":
                # Remove emoji and extra spaces
                tooltip_text = tooltip_text.replace("⚙️", "").strip()
            self._create_tooltip(btn, tooltip_text)
            
        # Note: Tab content will open in separate windows
        print("Tab buttons configured for external window opening")
        
        # Initialize button states
        self._highlight_active_tab()
        
    def _setup_dragging(self):
        """Setup window dragging functionality."""
        self._drag_data = {"x": 0, "y": 0}
        
        def start_drag(event):
            self._drag_data["x"] = event.x_root
            self._drag_data["y"] = event.y_root
            
        def do_drag(event):
            deltax = event.x_root - self._drag_data["x"]
            deltay = event.y_root - self._drag_data["y"]
            
            x = self.master.winfo_x() + deltax
            y = self.master.winfo_y() + deltay
            
            self.master.geometry(f"+{x}+{y}")
            
            self._drag_data["x"] = event.x_root
            self._drag_data["y"] = event.y_root
            
        # Bind to title bar for dragging
        self.title_bar.bind("<Button-1>", start_drag)
        self.title_bar.bind("<B1-Motion>", do_drag)
        self.title_label.bind("<Button-1>", start_drag) 
        self.title_label.bind("<B1-Motion>", do_drag)
        
    def _create_tooltip(self, widget, text):
        """Create a simple tooltip for a widget."""
        # Store text for updates
        widget._tooltip_text = text
        
        def on_enter(event):
            # Create tooltip window
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip, 
                text=widget._tooltip_text,  # Use stored text
                background="#2d3748", 
                foreground="white",
                relief=tk.SOLID, 
                borderwidth=1,
                font=("Arial", 10),
                padx=8,
                pady=4
            )
            label.pack()
            
            # Store tooltip reference
            widget._tooltip = tooltip
            
        def on_leave(event):
            # Destroy tooltip
            if hasattr(widget, '_tooltip'):
                widget._tooltip.destroy()
                del widget._tooltip
                
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
        
    def _show_language_menu(self):
        """Show language selection menu with scrollbar."""
        # Create toplevel window for language selection
        lang_window = tk.Toplevel(self.master)
        lang_window.overrideredirect(True)  # Remove window decorations
        lang_window.configure(bg="#3d3d3d")
        
        # Position below the language button
        try:
            x = self.lang_button.winfo_rootx()
            y = self.lang_button.winfo_rooty() + self.lang_button.winfo_height()
            lang_window.geometry(f"300x400+{x}+{y}")
        except tk.TclError:
            lang_window.geometry("300x400")
        
        # Make window topmost and grab focus
        lang_window.attributes('-topmost', True)
        lang_window.grab_set()
        
        # Create frame for listbox and scrollbar
        frame = tk.Frame(lang_window, bg="#3d3d3d", bd=2, relief=tk.RAISED)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(frame, bg="#3d3d3d", troughcolor="#2d2d2d")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox
        listbox = tk.Listbox(
            frame,
            bg="#3d3d3d",
            fg="white",
            selectbackground="#5d5d5d",
            selectforeground="white",
            font=("Arial", 11),
            bd=0,
            highlightthickness=0,
            activestyle="none",
            yscrollcommand=scrollbar.set
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Add languages to listbox
        for lang_name, lang_code in LANGUAGES:
            listbox.insert(tk.END, f"{lang_name} ({lang_code.upper()})")
        
        # Highlight current language
        for i, (_, lang_code) in enumerate(LANGUAGES):
            if lang_code == self.current_language:
                listbox.selection_set(i)
                listbox.see(i)
                break
        
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                _, lang_code = LANGUAGES[index]
                lang_window.destroy()
                self._change_language(lang_code)
        
        def on_close(event=None):
            lang_window.destroy()
        
        # Bind events
        listbox.bind('<<ListboxSelect>>', on_select)
        listbox.bind('<Return>', on_select)
        listbox.bind('<Escape>', on_close)
        lang_window.bind('<FocusOut>', on_close)
        
        # Focus on listbox
        listbox.focus_set()
            
    def bring_to_front(self):
        """Bring Normal Mode window to front temporarily."""
        try:
            self.master.lift()
            self.master.focus_force()
            self.master.attributes('-topmost', True)
            self.master.after(100, lambda: self.master.attributes('-topmost', False))
            print("🔝 Normal Mode brought to front")
        except Exception as e:
            print(f"⚠️ Could not bring Normal Mode to front: {e}")
            
    def _change_language(self, lang_code):
        """Change the display language and update all UI text. Persist selection."""
        self.current_language = lang_code
        self.lang = lang_code  # Keep alias in sync
        self.lang_button.config(text=f"🌐 {lang_code.upper()}")
        self._save_language_setting(lang_code)
        # Update all translatable text in UI
        self._update_text_labels()
        if self.on_language:
            self.on_language(lang_code)
            
    def _update_text_labels(self):
        """Update all text labels with current language."""
        # Update title with explicit text clearing
        new_title = tr("title", self.current_language)
        self.title_label.config(text="")  # Clear first
        self.title_label.update_idletasks()  # Force update
        self.title_label.config(text=new_title)  # Set new text
        
        # Update time labels
        # Note: Dies, miliDies, mikroDies are universal terms, but we could translate them if needed
        
        # Update standard time label
        if hasattr(self, 'std_time_label_text'):
            new_std_time_text = tr("standard_time", self.current_language)
            self.std_time_label_text.config(text="")  # Clear first
            self.std_time_label_text.update_idletasks()  # Force update
            self.std_time_label_text.config(text=new_std_time_text)  # Set new text
            
        # Update tab button tooltips
        if hasattr(self, 'tab_tooltip_keys'):
            for tab_id, button in self.tab_buttons.items():
                tooltip_key = self.tab_tooltip_keys.get(tab_id)
                if tooltip_key:
                    tooltip_text = tr(tooltip_key, self.current_language)
                    # Strip emoji from settings_title
                    if tooltip_key == "settings_title":
                        tooltip_text = tooltip_text.replace("⚙️", "").strip()
                    button._tooltip_text = tooltip_text
            
    def _switch_tab(self, tab_id):
        """Open tab content in a new window."""
        self._highlight_active_tab()
        self._open_tab_window(tab_id)
        
    def _highlight_active_tab(self):
        """Highlight the active tab button and show window status."""
        print(f"🔍 _highlight_active_tab called, open_windows: {list(self.open_windows.keys())}")
        for tab_id, button in self.tab_buttons.items():
            # Check if window is open for this tab
            window_open = False
            if self.open_windows[tab_id] is not None:
                try:
                    self.open_windows[tab_id].winfo_exists()
                    window_open = True
                    print(f"  ✅ {tab_id}: window exists and is open")
                except tk.TclError:
                    # Window was closed, clear reference
                    self.open_windows[tab_id] = None
                    window_open = False
                    print(f"  ❌ {tab_id}: window was closed (TclError)")
            else:
                print(f"  ⭕ {tab_id}: no window open")
            
            if window_open:
                # Window is open - show as inactive/disabled
                button.config(bg="#2a2a2a", fg="#666666", state="disabled")
                button.update_idletasks()  # Force immediate update
                print(f"  🔒 {tab_id} button DISABLED")
            else:
                # Normal state - use original colors
                button.config(bg="#4a5568", fg="#e2e8f0", state="normal")
                button.update_idletasks()  # Force immediate update
                print(f"  🔓 {tab_id} button ENABLED")
                
    def _open_tab_window(self, tab_id):
        """Open tab content in a separate window."""
        # Check if window is already open
        if self.open_windows[tab_id] is not None:
            # Window exists, check if it's still valid
            try:
                self.open_windows[tab_id].winfo_exists()
                # Window exists and is valid, just bring to front
                self.open_windows[tab_id].lift()
                self.open_windows[tab_id].focus_force()
                self.open_windows[tab_id].attributes('-topmost', True)
                self.open_windows[tab_id].after(100, lambda: self.open_windows[tab_id].attributes('-topmost', False))
                print(f"🔍 Brought existing {tab_id} window to front")
                return
            except tk.TclError:
                # Window was closed, clear reference
                self.open_windows[tab_id] = None
        
        # Create new window
        if tab_id == "explanation":
            self._show_explanation()
        elif tab_id == "comparison":
            # Create functional comparison card
            comparison_window = create_comparison_card(None, self.current_language)
            
            # Store reference to prevent duplicates
            self.open_windows[tab_id] = comparison_window
            
            # Update button state immediately
            self._highlight_active_tab()
            
            # Bring to front with temporary topmost
            comparison_window.lift()
            comparison_window.focus_force()
            comparison_window.attributes('-topmost', True)
            comparison_window.after(100, lambda: comparison_window.attributes('-topmost', False))
            
            # Bind to <Destroy> event to clean up when window is destroyed
            def on_comparison_destroy(event):
                # Only handle the main window destroy, not child widgets
                if event.widget == comparison_window:
                    print(f"🔄 Comparison <Destroy> event triggered")
                    self.open_windows[tab_id] = None
                    print(f"🔄 Calling _highlight_active_tab to re-enable button")
                    self._highlight_active_tab()
                    print(f"❌ Closed {tab_id} tab")
            
            comparison_window.bind('<Destroy>', on_comparison_destroy)
            
        else:
            # Create simple window for other tabs
            tab_window = tk.Toplevel(self.master)
            tab_window.title(f"Astronomical Watch - {tab_id.title()}")
            tab_window.geometry("500x400")
            
            # Bring window to front with temporary topmost
            tab_window.lift()
            tab_window.focus_force()
            tab_window.attributes('-topmost', True)
            tab_window.after(100, lambda: tab_window.attributes('-topmost', False))
            
            # Store reference to prevent duplicates
            self.open_windows[tab_id] = tab_window
            
            # Add cleanup when window is closed
            def on_window_close():
                self.open_windows[tab_id] = None
                tab_window.destroy()
                # Update button states when window closes
                self._highlight_active_tab()
                # Bring Normal Mode to front when card closes
                self.bring_to_front()
            
            tab_window.protocol("WM_DELETE_WINDOW", on_window_close)
            
            # Add content based on tab type
            if tab_id == "settings":
                # Open settings card
                print(f"🔧 Opening settings card for language: {self.lang}")
                try:
                    # Close the placeholder window first
                    tab_window.destroy()
                    
                    # Create settings card with widget reference
                    settings_card = create_settings_card(None, self.lang, widget_ref=self.widget_ref)
                    print(f"🔧 settings_card created: {settings_card}")
                    
                    # Track the settings card
                    self.open_windows[tab_id] = settings_card
                    
                    # Update button state immediately
                    self._highlight_active_tab()
                    
                    # Bring to front
                    settings_card.lift()
                    settings_card.focus_force()
                    settings_card.attributes('-topmost', True)
                    settings_card.after(100, lambda: settings_card.attributes('-topmost', False))
                    
                    # Bind to <Destroy> event to clean up when window is destroyed
                    def on_settings_destroy(event):
                        # Only handle the main window destroy, not child widgets
                        if event.widget == settings_card:
                            print(f"🔄 Settings <Destroy> event triggered")
                            self.open_windows[tab_id] = None
                            print(f"🔄 Calling _highlight_active_tab to re-enable button")
                            self._highlight_active_tab()
                            print(f"❌ Closed {tab_id} tab")
                    
                    settings_card.bind('<Destroy>', on_settings_destroy)
                    print(f"✅ Settings card opened successfully")
                    return
                    
                except Exception as e:
                    print(f"❌ ERROR creating settings_card: {e}")
                    import traceback
                    traceback.print_exc()
                    
                content = "Settings and preferences will be displayed here."
            else:
                content = f"Content for {tab_id} tab."
                
            label = tk.Label(tab_window, text=content, font=("Arial", 12), wraplength=400)
            label.pack(expand=True, pady=50)
            
            print(f"🗂️ Opened {tab_id} tab")
        
    def _show_explanation(self):
        """Show explanation window with content based on current language."""
        # Check if explanation window is already open
        if self.open_windows["explanation"] is not None:
            try:
                self.open_windows["explanation"].winfo_exists()
                # Window exists and is valid, just bring to front
                self.open_windows["explanation"].lift()
                self.open_windows["explanation"].focus_force()
                self.open_windows["explanation"].attributes('-topmost', True)
                self.open_windows["explanation"].after(100, lambda: self.open_windows["explanation"].attributes('-topmost', False))
                print(f"🔍 Brought existing explanation window to front")
                return
            except tk.TclError:
                # Window was closed, clear reference
                self.open_windows["explanation"] = None
        
        try:
            # Import explanation content based on current language
            explanation_module = f"..translate.explanation_{self.current_language}_card"
            
            # Dynamic import of explanation module
            import importlib
            module = importlib.import_module(explanation_module, package=__package__)
            explanation_text = module.EXPLANATION_TEXT
            
            # Create explanation window
            explanation_window = tk.Toplevel(self.master)
            explanation_window.title(f"{tr('explanation', self.current_language)} — {tr('title', self.current_language)}")
            explanation_window.geometry("700x600")
            explanation_window.minsize(600, 500)
            
            # Remove window decorations (minimize/maximize buttons)
            explanation_window.overrideredirect(True)
            
            # Store reference to prevent duplicates
            self.open_windows["explanation"] = explanation_window
            
            # Update button state immediately
            self._highlight_active_tab()
            
            # Bring window to front with temporary topmost
            explanation_window.lift()
            explanation_window.focus_force()
            explanation_window.attributes('-topmost', True)
            explanation_window.after(100, lambda: explanation_window.attributes('-topmost', False))
            
            # Bind to <Destroy> event to clean up when window is destroyed
            def on_explanation_destroy(event):
                # Only handle the main window destroy, not child widgets
                if event.widget == explanation_window:
                    print(f"🔄 Explanation <Destroy> event triggered")
                    self.open_windows["explanation"] = None
                    print(f"🔄 Calling _highlight_active_tab to re-enable button")
                    self._highlight_active_tab()
                    print(f"❌ Closed explanation tab")
            
            explanation_window.bind('<Destroy>', on_explanation_destroy)
            
            # Apply theme to explanation window
            theme = self._get_current_theme()
            
            # Create canvas with solid background
            gradient_canvas = tk.Canvas(
                explanation_window,
                highlightthickness=0,
                relief='flat',
                borderwidth=0,
                bg=theme.top_color,
                width=480,
                height=550
            )
            gradient_canvas.pack(fill=tk.BOTH, expand=True)
            
            # Setup drag functionality
            drag_data = {"x": 0, "y": 0}
            
            def start_drag(event):
                drag_data["x"] = event.x_root
                drag_data["y"] = event.y_root
                
            def do_drag(event):
                deltax = event.x_root - drag_data["x"]
                deltay = event.y_root - drag_data["y"]
                
                x = explanation_window.winfo_x() + deltax
                y = explanation_window.winfo_y() + deltay
                
                explanation_window.geometry(f"+{x}+{y}")
                
                drag_data["x"] = event.x_root
                drag_data["y"] = event.y_root
            
            # Bind to canvas
            gradient_canvas.bind("<Button-1>", start_drag)
            gradient_canvas.bind("<B1-Motion>", do_drag)
            
            # Main container on canvas with solid off-white background
            outer_frame = tk.Frame(gradient_canvas, bg="#f5f1e8")
            canvas_window = gradient_canvas.create_window(
                20, 20, anchor=tk.NW, window=outer_frame,
                width=660, height=560
            )
            
            # === Top: Title with close button (fixed) ===
            title_frame = tk.Frame(outer_frame, bg="#f5f1e8")
            title_frame.pack(fill=tk.X, pady=(0, 15))
            
            title = tk.Label(
                title_frame,
                text=f"📖 {tr('explanation', self.current_language)}",
                font=("Arial", 18, "bold"),
                bg="#f5f1e8",
                fg="#2c3e50"
            )
            title.pack(side=tk.LEFT)
            
            # Make title label draggable - this allows dragging by clicking on the text
            title.bind("<Button-1>", lambda e: (start_drag(e), "break"))
            title.bind("<B1-Motion>", lambda e: (do_drag(e), "break"))
            
            close_btn = tk.Button(
                title_frame,
                text="✕",
                command=explanation_window.destroy,
                bg="#FF5252",
                fg="white",
                font=("Arial", 14, "bold"),
                width=3,
                relief=tk.FLAT
            )
            close_btn.pack(side=tk.RIGHT)
            
            # Make the empty space in title_frame draggable (between title and close button)
            # We need to create a filler frame
            filler = tk.Frame(title_frame, bg="#f5f1e8")
            filler.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            filler.bind("<Button-1>", start_drag)
            filler.bind("<B1-Motion>", do_drag)
            
            # Create scrollable text widget
            text_frame = tk.Frame(outer_frame, bg="#f5f1e8")
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            # Bind drag to frame as well
            text_frame.bind("<Button-1>", start_drag)
            text_frame.bind("<B1-Motion>", do_drag)
            
            # Text widget with scrollbar - using off-white background
            text_widget = tk.Text(
                text_frame,
                wrap=tk.WORD,
                font=("Arial", 12),
                bg="#f5f1e8",
                fg="#2c3e50",
                padx=15,
                pady=15,
                highlightthickness=0,
                relief='flat'
            )
            
            scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            # Pack text and scrollbar
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Insert explanation text
            print(f"DEBUG: Inserting explanation text, length: {len(explanation_text)}")
            print(f"DEBUG: Text widget bg: {text_widget.cget('bg')}, fg: {text_widget.cget('fg')}")
            text_widget.insert(tk.END, explanation_text)
            text_widget.config(state=tk.DISABLED)
            print(f"DEBUG: Text inserted and widget disabled")
            
            # Bind drag to text widget as well (works even when disabled)
            text_widget.bind("<Button-1>", start_drag)
            text_widget.bind("<B1-Motion>", do_drag)
            
            # Bind drag to scrollbar
            scrollbar.bind("<Button-1>", start_drag)
            scrollbar.bind("<B1-Motion>", do_drag)
            
            print(f"📖 Opened explanation in {self.current_language}")
            
        except Exception as e:
            print(f"❌ Could not load explanation for {self.current_language}: {e}")
            # Fallback to simple text
            explanation_window = tk.Toplevel(self.master)
            explanation_window.title("Explanation")
            explanation_window.geometry("500x400")
            
            label = tk.Label(
                explanation_window, 
                text=f"Explanation content for {self.current_language} is not available.\nPlease check the translate/ directory.",
                font=("Arial", 12),
                wraplength=400
            )
            label.pack(expand=True, pady=50)
            
    def _close_window(self):
        """Close the normal mode window and all open cards."""
        print("📴 Closing Normal Mode and all cards...")
        # First, close all open card windows
        # We need to clear the references BEFORE calling destroy to trigger button updates
        windows_to_close = list(self.open_windows.items())
        
        # Clear all references first
        for tab_id in self.open_windows.keys():
            self.open_windows[tab_id] = None
        
        # Update button states to show all as enabled
        self._highlight_active_tab()
        
        # Now destroy the actual windows
        for tab_id, window in windows_to_close:
            if window is not None:
                try:
                    if window.winfo_exists():
                        print(f"🔄 Destroying {tab_id} card...")
                        window.destroy()
                except Exception as e:
                    print(f"⚠️ Error closing {tab_id}: {e}")
        
        # Stop any updates
        self.stop_updates()
        
        # Close Normal Mode and return to widget
        if self.on_back:
            self.on_back()
            print("✅ Normal Mode closed, returned to widget")
            
    def _apply_theme(self):
        """Apply the astronomical theme based on current local time."""
        try:
            # Get theme using local system time
            from datetime import datetime
            now_local = datetime.now()
            theme = get_sky_theme(now_local)
            
            if not theme:
                # Fallback to default theme
                from .gradient import SkyTheme
                theme = SkyTheme("#2563eb", "#60a5fa", "#000000")
            
            self.current_theme = theme
            
            # Set background color
            self._create_gradient_background(theme)
            
            # Apply theme colors to all widgets
            self._update_widget_colors(theme)
            
        except Exception as e:
            print(f"❌ Theme application failed: {e}")
            import traceback
            traceback.print_exc()
            # Continue without theme - use default colors
        
    def _create_gradient_background(self, theme):
        """Set solid background color on canvas."""
        try:
            if theme is None or not self.gradient_canvas:
                return
                
            # Set solid background color (top_color)
            self.gradient_canvas.configure(bg=theme.top_color)
                
        except Exception as e:
            print(f"❌ Background color update failed: {e}")
            if self.gradient_canvas:
                self.gradient_canvas.configure(bg=theme.top_color)
    
    def _on_canvas_resize(self, event):
        """Handle canvas resize to update gradient and frame size."""
        try:
            # Update canvas frame size to match canvas
            canvas_width = event.width
            canvas_height = event.height
            
            self.gradient_canvas.itemconfig(
                self.canvas_frame_id, 
                width=canvas_width, 
                height=canvas_height
            )
            
            # Recreate gradient with new dimensions
            if hasattr(self, 'current_theme'):
                self._create_gradient_background(self.current_theme)
                
        except Exception as e:
            print(f"⚠️ Canvas resize handling failed: {e}")
        
    def _update_widget_colors(self, theme):
        """Update all widget colors based on theme."""
        text_color = theme.text_color
        bg_color = theme.top_color  # Use solid top_color everywhere
        
        # Determine if background is dark for contrast
        bg_is_dark = self._is_dark_color(theme.top_color)
        button_bg = "#ffffff" if bg_is_dark else "#000000"
        button_fg = "#000000" if bg_is_dark else "#ffffff"
        
        # Update all frames and labels with solid top_color
        self.main_frame.configure(bg=bg_color)
        
        # Update title bar
        self.title_bar.configure(bg=bg_color)
        self.lang_frame.configure(bg=bg_color)
        self.title_label.configure(bg=bg_color, fg=text_color)
        self.lang_button.configure(bg=button_bg, fg=button_fg)
        self.close_button.configure(bg="#ff4444", fg="white")
        
        # Update time display frame and labels
        self.time_frame.configure(bg=bg_color)
        self.dies_label_text.configure(bg=bg_color, fg=text_color)
        self.dies_label.configure(bg=bg_color, fg=text_color)
        self.milidies_label_text.configure(bg=bg_color, fg=text_color)
        self.milidies_label.configure(bg=bg_color, fg=text_color)
        self.mikrodies_label_text.configure(bg=bg_color, fg=text_color)
        self.mikrodies_label.configure(bg=bg_color, fg=text_color)
        
        # Update standard time section
        if hasattr(self, 'std_time_frame'):
            self.std_time_frame.configure(bg=bg_color)
            self.std_time_label_text.configure(bg=bg_color, fg=text_color)
            self.std_time_label.configure(bg=bg_color, fg=text_color)
            if hasattr(self, 'countdown_label'):
                self.countdown_label.configure(bg=bg_color)
        
        # Update tab buttons section
        self.tab_frame.configure(bg=bg_color)
        for child in self.tab_frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=bg_color)
                
        for button in self.tab_buttons.values():
            button.configure(bg=button_bg, fg=button_fg)
        
        print(f"🎨 Widget colors updated with solid top_color: {bg_color}")
        
    def _update_time_widget_colors(self, text_color):
        """Update time display widget colors."""
        # Note: Skip bg='' for transparency in Tkinter
        
        # Update time labels with grid layout
        if hasattr(self, 'dies_label_text'):
            self.dies_label_text.configure(fg=text_color)
        if hasattr(self, 'dies_label'):
            self.dies_label.configure(fg=text_color)
            
        if hasattr(self, 'milidies_label_text'):
            self.milidies_label_text.configure(fg=text_color)
        if hasattr(self, 'milidies_label'):
            self.milidies_label.configure(fg=text_color)
            
        if hasattr(self, 'mikrodies_label_text'):
            self.mikrodies_label_text.configure(fg=text_color)
        if hasattr(self, 'mikrodies_label'):
            self.mikrodies_label.configure(fg=text_color)
            
    def _is_dark_color(self, hex_color):
        """Check if a color is dark (for contrast decisions)."""
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        
        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16) 
        b = int(hex_color[4:6], 16)
        
        # Calculate perceived brightness (0-255)
        brightness = (r * 0.299 + g * 0.587 + b * 0.114)
        
        return brightness < 128
        
    def start_updates(self):
        """Start the periodic update cycle."""
        self._update_display()
        
    def stop_updates(self):
        """Stop the periodic update cycle."""
        if self._update_job:
            self.master.after_cancel(self._update_job)
            self._update_job = None
            
    def _update_display(self):
        """Update the astronomical time display."""
        try:
            from ..core.equinox import compute_vernal_equinox
            
            now_utc = datetime.now(timezone.utc)
            current_year = now_utc.year
            equinox = compute_vernal_equinox(current_year)
            next_equinox = compute_vernal_equinox(current_year + 1)
            
            # Check if we need next year's equinox
            if now_utc < equinox:
                equinox = compute_vernal_equinox(current_year - 1)
                next_equinox = compute_vernal_equinox(current_year)
                
            astro_year = AstroYear(equinox)
            reading = astro_year.reading(now_utc)
            
            # Update astronomical time values
            self.dies = reading.dies
            self.miliDies = reading.miliDies
            mikroDies = reading.mikroDies
            
            # Calculate countdown to next equinox
            year_length_seconds = (next_equinox - equinox).total_seconds()
            year_length_dies = int(year_length_seconds / 86400.0)
            
            remaining_dies = year_length_dies - self.dies
            remaining_milidies = 1000 - self.miliDies
            
            if remaining_milidies == 1000:
                remaining_milidies = 0
                remaining_dies += 1
            
            # Update display labels (with error checking)
            try:
                if hasattr(self, 'dies_label') and self.dies_label:
                    self.dies_label.config(text=f"{self.dies:03d}")
                if hasattr(self, 'milidies_label') and self.milidies_label:
                    self.milidies_label.config(text=f"{self.miliDies:03d}")
                if hasattr(self, 'mikrodies_label') and self.mikrodies_label:
                    self.mikrodies_label.config(text=f"{mikroDies:03d}")
                    
                # Update countdown (show only if < 11 dies)
                if hasattr(self, 'countdown_label') and self.countdown_label:
                    if remaining_dies < 11:
                        countdown_text = tr("countdown_label", self.current_language, 
                                          dies=remaining_dies, milidies=remaining_milidies)
                        self.countdown_label.config(text=countdown_text)
                    else:
                        self.countdown_label.config(text="")
            except Exception as e:
                print(f"⚠️ Could not update time labels: {e}")
            
            # Update standard time
            try:
                # Get local system time with timezone
                local_now = datetime.now()
                local_tz = local_now.astimezone()
                
                # Get timezone name - prefer TZ environment variable
                if 'TZ' in os.environ:
                    tz_display = os.environ['TZ']
                else:
                    # Fallback to UTC offset format (UTC+/-HH:MM)
                    offset = local_tz.utcoffset()
                    if offset:
                        total_seconds = int(offset.total_seconds())
                        hours = total_seconds // 3600
                        minutes = abs(total_seconds % 3600) // 60
                        
                        # Format offset as UTC+/-HH:MM
                        if hours >= 0:
                            tz_display = f"UTC+{hours:02d}:{minutes:02d}"
                        else:
                            tz_display = f"UTC{hours:03d}:{minutes:02d}"
                    else:
                        tz_display = "UTC+00:00"
                
                # Format system time
                local_time = local_tz.strftime("%H:%M:%S %d/%m/%Y")
                std_time = f"{tz_display} {local_time}"
                
                if hasattr(self, 'std_time_label') and self.std_time_label:
                    self.std_time_label.config(text=std_time)
            except Exception as e:
                print(f"⚠️ Could not update standard time: {e}")
            
            # Update gradient theme (every few minutes to track sky changes)
            try:
                self._update_gradient_theme(now_utc)
            except Exception as e:
                print(f"⚠️ Could not update gradient theme: {e}")
            
            # Check for equinox moment (Dies 000, miliDies 000-005)
            if self.dies == 0 and self.miliDies < 5 and not self.fireworks_active:
                self._start_fireworks()
            elif self.dies > 0 and self.fireworks_active:
                self._stop_fireworks()
            
        except Exception as e:
            print(f"❌ Update error: {e}")
            # Fallback values - only update labels that exist
            try:
                if hasattr(self, 'dies_label') and self.dies_label:
                    self.dies_label.config(text="ERR")
                if hasattr(self, 'milidies_label') and self.milidies_label:
                    self.milidies_label.config(text="ERR")
                if hasattr(self, 'mikrodies_label') and self.mikrodies_label:
                    self.mikrodies_label.config(text="ERR")
            except:
                pass  # Ignore errors in error handling
            
        finally:
            # Always schedule next update if master still exists
            try:
                if self.master and hasattr(self.master, 'after'):
                    self._update_job = self.master.after(86, self._update_display)  # ~86ms = 1 mikroDies
            except:
                print("⚠️ Could not schedule next update")
        
    def _update_gradient_theme(self, current_time):
        """Update gradient theme based on current time (called periodically)."""
        # Get fresh theme from theme manager (Widget updates it every 86ms)
        from .theme_manager import get_shared_theme
        new_theme = get_shared_theme()
        
        # Check if theme has changed significantly
        theme_changed = (self.current_theme is None or 
                        new_theme.top_color != self.current_theme.top_color or
                        new_theme.bottom_color != self.current_theme.bottom_color)
        
        if theme_changed:
            print(f"🎨 Theme changed: {new_theme.top_color} → {new_theme.bottom_color}")
            self.current_theme = new_theme
            self._create_gradient_background(new_theme)
            self._update_widget_colors(new_theme)
    
    def _start_fireworks(self):
        """Start fireworks animation for equinox celebration"""
        print("🎆 Starting fireworks animation in Normal Mode!")
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
        if not hasattr(self, 'gradient_canvas') or not self.gradient_canvas:
            return
        
        canvas_width = self.gradient_canvas.winfo_width()
        canvas_height = self.gradient_canvas.winfo_height()
        
        # Random starting position
        x = random.randint(50, canvas_width - 50)
        y = random.randint(50, canvas_height - 100)
        
        # Random color
        colors = ["#FFD700", "#FF6347", "#00FF00", "#00BFFF", "#FF69B4", "#FFA500", "#FFFF00", "#FFFFFF"]
        color = random.choice(colors)
        
        # Create particles radiating outward
        num_particles = 25
        for i in range(num_particles):
            angle = (2 * math.pi * i) / num_particles
            speed = random.uniform(2.0, 4.5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            self.fireworks_particles.append({
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'color': color,
                'life': 40,  # frames
                'size': 4
            })
    
    def _animate_fireworks(self):
        """Animate fireworks particles"""
        if not self.fireworks_active or not hasattr(self, 'gradient_canvas'):
            return
        
        # Create new firework occasionally
        if random.random() < 0.2:  # 20% chance per frame
            self._create_firework()
        
        # Update and draw particles
        canvas_width = self.gradient_canvas.winfo_width()
        canvas_height = self.gradient_canvas.winfo_height()
        
        # Update particles
        for particle in self.fireworks_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['life'] -= 1
            
            # Remove dead particles
            if particle['life'] <= 0 or particle['y'] > canvas_height:
                self.fireworks_particles.remove(particle)
        
        # Draw fireworks particles on gradient canvas
        # Remove old firework particles
        self.gradient_canvas.delete("firework")
        
        for particle in self.fireworks_particles:
            alpha = particle['life'] / 40.0
            size = max(2, int(particle['size'] * alpha))
            self.gradient_canvas.create_oval(
                particle['x'] - size, particle['y'] - size,
                particle['x'] + size, particle['y'] + size,
                fill=particle['color'],
                outline="",
                tags="firework"
            )
        
        # Schedule next frame
        self.fireworks_job = self.master.after(50, self._animate_fireworks)  # ~20 FPS


def create_normal_mode(parent, on_back=None, on_language=None, widget_ref=None):
    """Factory function to create normal mode instance."""
    return ModernNormalMode(parent, on_back, on_language, widget_ref)