"""
Astronomical Watch Normal Mode - Modern UI Design

A clean, modern interface without traditional window decorations.
Features custom title bar with language selector and close button.
Main content shows astronomical time values in hierarchical layout.
"""

import tkinter as tk
from tkinter import ttk, font as tk_font
import math
from datetime import datetime, timezone
from ..core.astro_time_core import AstroYear
from .gradient import get_sky_theme, create_gradient_colors
from .translations import TRANSLATIONS
from .comparison_card import create_comparison_card

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
    ("Српски (Serbian)", "sr"),
    ("Español", "es"),
    ("中文 (Chinese)", "zh"),
    ("العربية (Arabic)", "ar"),
    ("Português", "pt"),
    ("Français", "fr"),
    ("Deutsch", "de"),
    ("Русский (Russian)", "ru"),
    ("日本語 (Japanese)", "ja"),
    ("हिन्दी (Hindi)", "hi"),
    ("فارسی (Persian)", "fa"),
    ("Bahasa Indonesia", "id"),
    ("Kiswahili", "sw"),
    ("Hausa", "ha"),
    ("Türkçe", "tr"),
    ("Ελληνικά (Greek)", "el"),
    ("Polski", "pl"),
    ("Italiano", "it"),
    ("Nederlands", "nl")
]

def tr(key: str, lang: str = "en") -> str:
    """Simple translation function."""
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS.get("en", {}).get(key, key))


class ModernNormalMode:
    """Modern Normal Mode without window decorations."""
    
    def __init__(self, parent, on_back=None, on_language=None):
        print("🚀 ModernNormalMode.__init__ starting...")
        
        self.master = parent
        self.on_back = on_back
        self.on_language = on_language
        
        # Data initialization first
        self.dies = 0
        self.miliDies = 0
        self.mikroDies = 0
        self.current_language = "en"
        
        # Theme state
        self.current_theme = None
        self.gradient_canvas = None
        
        # Update timer
        self._update_job = None
        
        # Active tab
        self.current_tab = "explanation"
        
        # Track open windows to prevent duplicates
        self.open_windows = {
            "explanation": None,
            "comparison": None,
            "calculation": None,
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
            "info": "ℹ️",
            "compare": "⚖️", 
            "calc": "🧮",
            "settings": "⚙️"
        }
        
    def _create_ui(self):
        """Create the modern UI layout."""
        try:
            print("🎨 Creating UI layout...")
            
            # Get initial theme colors
            theme = get_sky_theme()
            bg_color = "#1e293b"  # Force dark slate background 
            print(f"🎨 Canvas background color will be: {bg_color}")
            
            # Create gradient background canvas first
            self.gradient_canvas = tk.Canvas(
                self.master,
                highlightthickness=0,
                relief='flat',
                borderwidth=0,
                bg=bg_color  # Set dark background color
            )
            self.gradient_canvas.pack(fill=tk.BOTH, expand=True)
            print("✅ Gradient canvas created")
            
            # Bind canvas resize to update gradient
            self.gradient_canvas.bind('<Configure>', self._on_canvas_resize)
            
            # Main container over gradient - make truly transparent
            # Use the parent canvas background for transparency
            canvas_bg = self.gradient_canvas.cget('bg')
            self.main_frame = tk.Frame(self.gradient_canvas, bg=canvas_bg, relief='flat', bd=0)
            self.canvas_frame_id = self.gradient_canvas.create_window(
                0, 0, anchor=tk.NW, window=self.main_frame
            )
            print(f"✅ Main frame created with canvas background: {canvas_bg}")
            
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
        
    def _create_title_bar(self):
        """Create custom title bar with language selector and close button."""
        # Use canvas background for all frames
        canvas_bg = self.gradient_canvas.cget('bg')
        
        self.title_bar = tk.Frame(self.main_frame, height=50, bg=canvas_bg, relief='flat', bd=0)
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
        self.lang_frame = tk.Frame(self.title_bar, bg=canvas_bg)
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
            bg=canvas_bg,
            fg="#e2e8f0"
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def _create_time_display(self):
        """Create the main time display area with proper grid layout."""
        # Use canvas background for consistency
        canvas_bg = self.gradient_canvas.cget('bg')
        text_color = "#e2e8f0"  # Light gray text for dark background
        
        self.time_frame = tk.Frame(self.main_frame, bg=canvas_bg, relief='flat', bd=0)
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
            bg=canvas_bg,
            fg=text_color
        )
        self.dies_label_text.grid(row=0, column=0, padx=(15, 8), pady=5, sticky="e")
        
        self.dies_label = tk.Label(
            self.time_frame,
            text="000",
            font=get_monospace_font(48),
            anchor="w",
            bg=canvas_bg,
            fg=text_color
        )
        self.dies_label.grid(row=0, column=1, padx=(8, 15), pady=5, sticky="w")
        
        # MiliDies display
        self.milidies_label_text = tk.Label(
            self.time_frame,
            text="miliDies:",
            font=("Arial", 14, "bold"),
            anchor="e",
            bg=canvas_bg,
            fg=text_color
        )
        self.milidies_label_text.grid(row=1, column=0, padx=(15, 8), pady=5, sticky="e")
        
        self.milidies_label = tk.Label(
            self.time_frame,
            text="000",
            font=get_monospace_font(48),
            anchor="w",
            bg=canvas_bg,
            fg=text_color
        )
        self.milidies_label.grid(row=1, column=1, padx=(8, 15), pady=5, sticky="w")
        
        # MikroDies display
        self.mikrodies_label_text = tk.Label(
            self.time_frame,
            text="mikroDies:",
            font=("Arial", 14, "bold"),
            anchor="e",
            bg=canvas_bg,
            fg=text_color
        )
        self.mikrodies_label_text.grid(row=2, column=0, padx=(15, 8), pady=5, sticky="e")
        
        self.mikrodies_label = tk.Label(
            self.time_frame,
            text="000",
            font=get_monospace_font(48),
            anchor="w",
            bg=canvas_bg,
            fg=text_color
        )
        self.mikrodies_label.grid(row=2, column=1, padx=(8, 15), pady=5, sticky="w")
        
    def _create_standard_time(self):
        """Create standard time display section."""
        # Use canvas background for consistency
        canvas_bg = self.gradient_canvas.cget('bg')
        text_color = "#e2e8f0"  # Light gray text for dark background
        
        # Add visual separator
        separator_frame = tk.Frame(self.main_frame, height=2, bg=canvas_bg, relief='flat', bd=0)
        separator_frame.pack(fill=tk.X, pady=20)
        separator_frame.pack_propagate(False)
        
        self.std_time_frame = tk.Frame(self.main_frame, bg=canvas_bg, relief='flat', bd=0)
        self.std_time_frame.pack(fill=tk.X, pady=5)
        
        # Label for standard time
        self.std_time_label_text = tk.Label(
            self.std_time_frame,
            text=tr("standard_time", self.current_language),
            font=("Arial", 14),
            bg=canvas_bg,
            fg=text_color
        )
        self.std_time_label_text.pack(pady=(0, 5))
        
        self.std_time_label = tk.Label(
            self.std_time_frame,
            text="Loading...",
            font=("Arial", 16, "bold"),
            bg=canvas_bg,
            fg=text_color
        )
        self.std_time_label.pack()
        
    def _create_tab_buttons(self):
        """Create tab navigation buttons with icons."""
        # Use canvas background for consistency
        canvas_bg = self.gradient_canvas.cget('bg')
        text_color = "#e2e8f0"  # Light gray text for dark background
        
        self.tab_frame = tk.Frame(self.main_frame, bg=canvas_bg, relief='flat', bd=0)
        self.tab_frame.pack(fill=tk.X, pady=5)
        
        # Center the buttons
        button_container = tk.Frame(self.tab_frame, bg=canvas_bg, relief='flat', bd=0)
        button_container.pack()
        
        self.tab_buttons = {}
        
        tabs = [
            ("explanation", self.icons["info"], "Info"),
            ("comparison", self.icons["compare"], "Compare"), 
            ("calculation", self.icons["calc"], "Calc"),
            ("settings", self.icons["settings"], "Settings")
        ]
        
        for tab_id, icon, text in tabs:
            btn = tk.Button(
                button_container,
                text=icon,
                font=("Arial", 16),
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
        
    def _show_language_menu(self):
        """Show language selection menu."""
        menu = tk.Menu(self.master, tearoff=0, bg="#3d3d3d", fg="white")
        
        for lang_name, lang_code in LANGUAGES:
            menu.add_command(
                label=f"{lang_name} ({lang_code.upper()})",
                command=lambda lc=lang_code: self._change_language(lc)
            )
            
        try:
            x = self.lang_button.winfo_rootx()
            y = self.lang_button.winfo_rooty() + self.lang_button.winfo_height()
            menu.post(x, y)
        except tk.TclError:
            pass
            
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
        """Change the display language and update all UI text."""
        self.current_language = lang_code
        self.lang_button.config(text=f"🌐 {lang_code.upper()}")
        
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
            
    def _switch_tab(self, tab_id):
        """Open tab content in a new window."""
        self._highlight_active_tab()
        self._open_tab_window(tab_id)
        
    def _highlight_active_tab(self):
        """Highlight the active tab button and show window status."""
        for tab_id, button in self.tab_buttons.items():
            # Check if window is open for this tab
            window_open = False
            if self.open_windows[tab_id] is not None:
                try:
                    self.open_windows[tab_id].winfo_exists()
                    window_open = True
                except tk.TclError:
                    # Window was closed, clear reference
                    self.open_windows[tab_id] = None
                    window_open = False
            
            if window_open:
                # Window is open - show as inactive/disabled
                button.config(bg="#2a2a2a", fg="#666666", state="disabled")
            else:
                # Normal state - use original colors
                button.config(bg="#4a5568", fg="#e2e8f0", state="normal")
                
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
            comparison_window = create_comparison_card(self.master, self.current_language)
            
            # Force window to appear above normal mode
            comparison_window.transient(self.master)
            comparison_window.lift()
            comparison_window.focus_force()
            comparison_window.wm_attributes("-topmost", True)
            comparison_window.after(200, lambda: comparison_window.wm_attributes("-topmost", False))
            
            # Store reference to prevent duplicates
            self.open_windows[tab_id] = comparison_window
            
            # Override the close behavior to update our tracking
            original_destroy = comparison_window.destroy
            def enhanced_destroy():
                print(f"🗑️ Enhanced destroy called for {tab_id}")
                self.open_windows[tab_id] = None
                # Schedule button update after window is destroyed
                self.master.after(10, self._highlight_active_tab)
                self.master.after(50, self.bring_to_front)
                original_destroy()
            
            comparison_window.destroy = enhanced_destroy
            
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
            if tab_id == "calculation":
                content = "Astronomical calculations will be displayed here."
            elif tab_id == "settings":
                content = "Settings and preferences will be displayed here."
            else:
                content = f"Content for {tab_id} tab."
                
            label = tk.Label(tab_window, text=content, font=("Arial", 12), wraplength=400)
            label.pack(expand=True, pady=50)
            
            print(f"🗂️ Opened {tab_id} tab")
            
        # Update button states after opening window
        self._highlight_active_tab()
        
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
            
            # Bring window to front with temporary topmost
            explanation_window.lift()
            explanation_window.focus_force()
            explanation_window.attributes('-topmost', True)
            explanation_window.after(100, lambda: explanation_window.attributes('-topmost', False))
            
            # Store reference to prevent duplicates
            self.open_windows["explanation"] = explanation_window
            
            # Add cleanup when window is closed
            def on_explanation_close():
                self.open_windows["explanation"] = None
                explanation_window.destroy()
                # Update button states when window closes
                self._highlight_active_tab()
                # Bring Normal Mode to front when card closes
                self.bring_to_front()
            
            explanation_window.protocol("WM_DELETE_WINDOW", on_explanation_close)
            
            # Apply theme to explanation window
            theme = get_sky_theme()
            explanation_window.configure(bg=theme.bottom_color)
            
            # Create scrollable text widget
            text_frame = tk.Frame(explanation_window, bg=theme.bottom_color)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Text widget with scrollbar
            text_widget = tk.Text(
                text_frame,
                wrap=tk.WORD,
                font=("Arial", 11),
                bg="#f7fafc",
                fg="#2c3e50",
                padx=15,
                pady=15
            )
            
            scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            # Pack text and scrollbar
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Insert explanation text
            text_widget.insert(tk.END, explanation_text)
            text_widget.config(state=tk.DISABLED)
            
            print(f"📖 Opened explanation in {self.current_language}")
            
            # Update button states after opening window
            self._highlight_active_tab()
            
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
        # First, close all open card windows
        for tab_id, window in self.open_windows.items():
            if window is not None:
                try:
                    window.destroy()
                    print(f"✅ Closed {tab_id} card")
                except:
                    pass
        
        # Clear all window references
        self.open_windows = {
            "explanation": None,
            "comparison": None,
            "calculation": None,
            "settings": None
        }
        
        # Stop any updates
        self.stop_updates()
        
        # Close Normal Mode and return to widget
        if self.on_back:
            self.on_back()
            print("✅ Normal Mode closed, returned to widget")
            
    def _apply_theme(self):
        """Apply the astronomical theme with gradient background based on current time."""
        try:
            print("🎨 Applying theme...")
            now_utc = datetime.now(timezone.utc)
            theme = get_sky_theme(now_utc)
            self.current_theme = theme
            print(f"✅ Theme calculated: {theme.top_color} → {theme.bottom_color}")
            
            # Ensure canvas is ready before creating gradient
            if self.gradient_canvas:
                self.gradient_canvas.update_idletasks()
                canvas_w = self.gradient_canvas.winfo_width()
                canvas_h = self.gradient_canvas.winfo_height()
                print(f"📐 Canvas state: {canvas_w}x{canvas_h}")
            
            # Create gradient background
            self._create_gradient_background(theme)
            print("✅ Gradient background created")
            
            # Apply theme colors to all widgets
            self._update_widget_colors(theme)
            print("✅ Widget colors updated")
            
        except Exception as e:
            print(f"❌ Theme application failed: {e}")
            import traceback
            traceback.print_exc()
            # Continue without theme - use default colors
        
    def _create_gradient_background(self, theme):
        """Create gradient background on canvas."""
        try:
            print(f"📌 DEBUG: _create_gradient_background called")
            print(f"📌 DEBUG: gradient_canvas exists: {hasattr(self, 'gradient_canvas')}")
            if hasattr(self, 'gradient_canvas'):
                print(f"📌 DEBUG: gradient_canvas is not None: {self.gradient_canvas is not None}")
                
            if not self.gradient_canvas:
                print("⚠️ No gradient canvas available")
                return
                
            print(f"🎨 Creating gradient background...")
            
            # Clear existing gradient and set canvas background
            self.gradient_canvas.delete("gradient")
            self.gradient_canvas.configure(bg=theme.bottom_color)
            print(f"📋 Canvas background set to: {theme.bottom_color}")
            
            # Force canvas update and get dimensions
            self.gradient_canvas.update_idletasks()
            self.master.update_idletasks()
            
            canvas_width = self.gradient_canvas.winfo_width()
            canvas_height = self.gradient_canvas.winfo_height()
            
            # If canvas not properly sized yet, use window dimensions
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width = self.window_width
                canvas_height = self.window_height
                print(f"📐 Using window dimensions: {canvas_width}x{canvas_height}")
            else:
                print(f"📐 Canvas size: {canvas_width}x{canvas_height}")
            
            if canvas_width <= 1 or canvas_height <= 1:
                print("❌ Could not get valid canvas dimensions, using solid color")
                self.gradient_canvas.configure(bg=theme.bottom_color)
                return
            
            # Create gradient colors with adequate steps
            gradient_steps = max(canvas_height, 100)  # At least 100 steps for smooth gradient
            gradient_colors = create_gradient_colors(theme, steps=gradient_steps)
            print(f"🌈 Creating gradient: {len(gradient_colors)} colors for {canvas_width}x{canvas_height}")
            
            # Draw gradient as filled rectangles for seamless appearance
            lines_drawn = 0
            step_height = canvas_height / len(gradient_colors)
            
            for i, color in enumerate(gradient_colors):
                try:
                    # Calculate y position for this color strip
                    y_start = int(i * step_height)
                    y_end = int((i + 1) * step_height)
                    
                    # Ensure we don't exceed canvas bounds
                    if y_start < canvas_height:
                        y_end = min(y_end, canvas_height)
                        
                        # Use filled rectangles for smooth gradient
                        self.gradient_canvas.create_rectangle(
                            0, y_start, canvas_width, y_end,
                            fill=color, outline=color, width=0, tags="gradient"
                        )
                        lines_drawn += 1
                except Exception as line_error:
                    print(f"⚠️ Error drawing rectangle {i}: {line_error}")
                    break
                
            print(f"✅ Gradient created: {lines_drawn} strips drawn")
                
            # Make main frame transparent so gradient shows through
            # Note: Cannot use bg="" in Tkinter, frame stays transparent without bg setting
            print("✅ Main frame inherits gradient canvas background")
                
        except Exception as e:
            print(f"❌ Gradient background creation failed: {e}")
            import traceback
            traceback.print_exc()
            # Fallback: set a solid color
            try:
                if self.gradient_canvas:
                    self.gradient_canvas.configure(bg=theme.bottom_color)
                    print(f"🎨 Fallback: Set solid background {theme.bottom_color}")
            except:
                print("❌ Even fallback failed")
    
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
        
        # Determine if background is dark for contrast
        bg_is_dark = self._is_dark_color(theme.bottom_color)
        button_bg = "#ffffff" if bg_is_dark else "#000000"
        button_fg = "#000000" if bg_is_dark else "#ffffff"
        
        # Update title bar
        # Note: Cannot use bg='' for transparency in Tkinter
        self.lang_button.configure(bg=button_bg, fg=button_fg)
        self.title_label.configure(fg=text_color)
        self.close_button.configure(bg="#ff4444", fg="white")
        
        # Update time display
        self._update_time_widget_colors(text_color)
        
        # Update standard time
        self.std_time_label_text.configure(fg=text_color)
        self.std_time_label.configure(fg=text_color)
        
        # Update tab buttons and frames
        for child in self.tab_frame.winfo_children():
            if isinstance(child, tk.Frame):
                # Skip bg configuration for transparency effect
                pass
                
        for button in self.tab_buttons.values():
            button.configure(bg=button_bg, fg=button_fg)
            
        # Tab contents are now in separate windows, no need to update here
        print("Theme updated for main window widgets")
        
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
        print("🔄 Updating display...")
        try:
            from ..core.equinox import compute_vernal_equinox
            
            now_utc = datetime.now(timezone.utc)
            current_year = now_utc.year
            equinox = compute_vernal_equinox(current_year)
            
            # Check if we need next year's equinox
            if now_utc < equinox:
                equinox = compute_vernal_equinox(current_year - 1)
                
            astro_year = AstroYear(equinox)
            reading = astro_year.reading(now_utc)
            
            # Update astronomical time values
            self.dies = reading.dies
            self.miliDies = reading.miliDies
            mikroDies = reading.mikroDies
            
            # Update display labels (with error checking)
            try:
                if hasattr(self, 'dies_label') and self.dies_label:
                    self.dies_label.config(text=f"{self.dies:03d}")
                if hasattr(self, 'milidies_label') and self.milidies_label:
                    self.milidies_label.config(text=f"{self.miliDies:03d}")
                if hasattr(self, 'mikrodies_label') and self.mikrodies_label:
                    self.mikrodies_label.config(text=f"{mikroDies:03d}")
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
            
            print(f"🕐 Modern Normal Mode Updated: {self.dies:03d}.{self.miliDies:03d}.{mikroDies:03d}")
            
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
        new_theme = get_sky_theme(current_time)
        
        # Only update if theme has significantly changed (save CPU)
        if (self.current_theme is None or 
            new_theme.top_color != self.current_theme.top_color or
            new_theme.bottom_color != self.current_theme.bottom_color):
            
            self.current_theme = new_theme
            self._create_gradient_background(new_theme)
            self._update_widget_colors(new_theme)


def create_normal_mode(parent, on_back=None, on_language=None):
    """Factory function to create normal mode instance."""
    return ModernNormalMode(parent, on_back, on_language)