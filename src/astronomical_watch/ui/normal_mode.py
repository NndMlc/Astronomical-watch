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
        
        # Window configuration
        self.window_width = 650
        self.window_height = 800
        
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
            
            # Apply theme
            self._apply_theme()
            print("✅ Theme applied")
            
            # Schedule gradient refresh after UI is fully created
            self.master.after(100, lambda: self._apply_theme())
            
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
            
            # Create gradient background canvas first - let it expand naturally
            self.gradient_canvas = tk.Canvas(
                self.master,
                highlightthickness=0,
                relief='flat',
                borderwidth=0
            )
            self.gradient_canvas.pack(fill=tk.BOTH, expand=True)
            print("✅ Gradient canvas created")
            
            # Bind canvas resize to update gradient
            self.gradient_canvas.bind('<Configure>', self._on_canvas_resize)
            
            # Main container over gradient
            self.main_frame = tk.Frame(self.gradient_canvas, bg="")
            self.canvas_frame_id = self.gradient_canvas.create_window(
                0, 0, anchor=tk.NW, window=self.main_frame
            )
            print("✅ Main frame created")
            
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
        self.title_bar = tk.Frame(self.main_frame, height=50)
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
        self.close_button.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # Activity indicator (right side)
        self.activity_dot = tk.Label(
            self.title_bar,
            text="●",
            fg="#00ff00",
            font=("Arial", 8)
        )
        self.activity_dot.pack(side=tk.RIGHT, padx=(0, 10), pady=15)
        
        # Language selector (left side)
        self.lang_frame = tk.Frame(self.title_bar)
        self.lang_frame.pack(side=tk.LEFT, padx=15, pady=10)
        
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
            font=("Arial", 14, "bold")
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def _create_time_display(self):
        """Create the main time display area."""
        self.time_frame = tk.Frame(self.main_frame)
        self.time_frame.pack(fill=tk.X, pady=20)
        
        # Dies display
        dies_container = tk.Frame(self.time_frame)
        dies_container.pack(fill=tk.X, pady=15)
        
        self.dies_label_text = tk.Label(
            dies_container,
            text="Dies:",
            font=("Arial", 12, "bold")
        )
        self.dies_label_text.pack(side=tk.LEFT, padx=(50, 0))
        
        self.dies_label = tk.Label(
            dies_container,
            text="000",
            font=get_monospace_font(52)
        )
        self.dies_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # MiliDies display
        milidies_container = tk.Frame(self.time_frame)
        milidies_container.pack(fill=tk.X, pady=15)
        
        self.milidies_label_text = tk.Label(
            milidies_container,
            text="miliDies:",
            font=("Arial", 12, "bold")
        )
        self.milidies_label_text.pack(side=tk.LEFT, padx=(50, 0))
        
        self.milidies_label = tk.Label(
            milidies_container,
            text="000", 
            font=get_monospace_font(52)
        )
        self.milidies_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # MikroDies display
        mikrodies_container = tk.Frame(self.time_frame)
        mikrodies_container.pack(fill=tk.X, pady=15)
        
        self.mikrodies_label_text = tk.Label(
            mikrodies_container,
            text="mikroDies:",
            font=("Arial", 12, "bold") 
        )
        self.mikrodies_label_text.pack(side=tk.LEFT, padx=(50, 0))
        
        self.mikrodies_label = tk.Label(
            mikrodies_container,
            text="000",
            font=get_monospace_font(52)
        )
        self.mikrodies_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def _create_standard_time(self):
        """Create standard time display."""
        # Add visual separator
        separator_frame = tk.Frame(self.main_frame, height=2)
        separator_frame.pack(fill=tk.X, pady=20)
        separator_frame.pack_propagate(False)
        
        self.std_time_frame = tk.Frame(self.main_frame)
        self.std_time_frame.pack(fill=tk.X, pady=20)
        
        # Label for standard time
        self.std_time_label_text = tk.Label(
            self.std_time_frame,
            text=tr("standard_time", self.current_language),
            font=("Arial", 14)
        )
        self.std_time_label_text.pack(pady=(0, 5))
        
        self.std_time_label = tk.Label(
            self.std_time_frame,
            text="UTC 00:00:00 26/11/2025",
            font=("Arial", 16, "bold")
        )
        self.std_time_label.pack()
        
    def _create_tab_buttons(self):
        """Create tab navigation buttons with icons."""
        self.tab_frame = tk.Frame(self.main_frame)
        self.tab_frame.pack(fill=tk.X, pady=20)
        
        # Center the buttons
        button_container = tk.Frame(self.tab_frame)
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
                command=lambda t=tab_id: self._switch_tab(t)
            )
            btn.pack(side=tk.LEFT, padx=8)
            self.tab_buttons[tab_id] = btn
            
        # Note: Tab content will open in separate windows
        print("Tab buttons configured for external window opening")
        
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
        self.current_tab = tab_id
        self._highlight_active_tab()
        self._open_tab_window(tab_id)
        
    def _highlight_active_tab(self):
        """Highlight the active tab button."""
        for tab_id, button in self.tab_buttons.items():
            if tab_id == self.current_tab:
                button.config(bg="#5d5d5d", fg="#ffffff")
            else:
                button.config(bg="#3d3d3d", fg="#cccccc")
                
    def _open_tab_window(self, tab_id):
        """Open tab content in a separate window."""
        if tab_id == "explanation":
            self._show_explanation()
        else:
            # Create simple window for other tabs
            tab_window = tk.Toplevel(self.master)
            tab_window.title(f"Astronomical Watch - {tab_id.title()}")
            tab_window.geometry("500x400")
            
            # Add content based on tab type
            if tab_id == "comparison":
                content = "Time comparison tools will be displayed here."
            elif tab_id == "calculation":
                content = "Astronomical calculations will be displayed here."
            elif tab_id == "settings":
                content = "Settings and preferences will be displayed here."
            else:
                content = f"Content for {tab_id} tab."
                
            label = tk.Label(tab_window, text=content, font=("Arial", 12), wraplength=400)
            label.pack(expand=True, pady=50)
            
        print(f"🗂️ Opened {tab_id} tab")
        
    def _show_explanation(self):
        """Show explanation window with content based on current language."""
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
        """Close the normal mode window."""
        if self.on_back:
            self.on_back()
            
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
            if not self.gradient_canvas:
                print("⚠️ No gradient canvas available")
                return
                
            print(f"🎨 Creating gradient background...")
            
            # Clear existing gradient
            self.gradient_canvas.delete("gradient")
            
            # Multiple attempts to get proper canvas dimensions
            attempts = 0
            canvas_width = canvas_height = 0
            
            while (canvas_width <= 1 or canvas_height <= 1) and attempts < 3:
                self.gradient_canvas.update_idletasks()
                self.master.update_idletasks()
                
                canvas_width = self.gradient_canvas.winfo_width()
                canvas_height = self.gradient_canvas.winfo_height()
                
                print(f"📐 Attempt {attempts + 1}: Canvas size {canvas_width}x{canvas_height}")
                
                if canvas_width <= 1 or canvas_height <= 1:
                    canvas_width = self.window_width
                    canvas_height = self.window_height
                    print(f"📐 Using fallback dimensions: {canvas_width}x{canvas_height}")
                    break
                    
                attempts += 1
            
            if canvas_width <= 1 or canvas_height <= 1:
                print("❌ Could not get valid canvas dimensions")
                # Fallback to setting background color
                self.gradient_canvas.configure(bg=theme.bottom_color)
                return
            
            # Create gradient colors
            gradient_colors = create_gradient_colors(theme, steps=canvas_height)
            print(f"🌈 Creating gradient: {len(gradient_colors)} colors for {canvas_width}x{canvas_height}")
            
            # Draw gradient as filled rectangles for seamless appearance
            lines_drawn = 0
            for i, color in enumerate(gradient_colors):
                if i < canvas_height:
                    try:
                        # Use filled rectangles instead of lines to avoid gaps
                        self.gradient_canvas.create_rectangle(
                            0, i, canvas_width, i + 1,
                            fill=color, outline=color, width=0, tags="gradient"
                        )
                        lines_drawn += 1
                    except Exception as line_error:
                        print(f"⚠️ Error drawing rectangle {i}: {line_error}")
                        break
                
            print(f"✅ Gradient created: {lines_drawn} lines drawn")
                
            # Make main frame transparent
            if hasattr(self, 'main_frame'):
                self.main_frame.configure(bg="")
                print("✅ Main frame made transparent")
                
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
        self.title_bar.configure(bg="")
        self.lang_frame.configure(bg="")
        self.lang_button.configure(bg=button_bg, fg=button_fg)
        self.title_label.configure(bg="", fg=text_color)
        self.close_button.configure(bg="#ff4444", fg="white")
        self.activity_dot.configure(bg="", fg="#00ff00")
        
        # Update time display
        self._update_time_widget_colors(text_color)
        
        # Update standard time
        self.std_time_frame.configure(bg="")
        self.std_time_label_text.configure(bg="", fg=text_color)
        self.std_time_label.configure(bg="", fg=text_color)
        
        # Update tab buttons and frames
        self.tab_frame.configure(bg="")
        for child in self.tab_frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg="")
                
        for button in self.tab_buttons.values():
            button.configure(bg=button_bg, fg=button_fg)
            
        # Tab contents are now in separate windows, no need to update here
        print("Theme updated for main window widgets")
        
    def _update_time_widget_colors(self, text_color):
        """Update time display widget colors."""
        # Update frames
        for frame_name in ['time_frame']:
            if hasattr(self, frame_name):
                getattr(self, frame_name).configure(bg="")
        
        # Update all child frames (dies, milidies, mikrodies frames)
        for child in self.time_frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg="")
                
        # Update labels
        if hasattr(self, 'dies_label_text'):
            self.dies_label_text.configure(bg="", fg=text_color)
        if hasattr(self, 'dies_label'):
            self.dies_label.configure(bg="", fg=text_color)
            
        if hasattr(self, 'milidies_label_text'):
            self.milidies_label_text.configure(bg="", fg=text_color)
        if hasattr(self, 'milidies_label'):
            self.milidies_label.configure(bg="", fg=text_color)
            
        if hasattr(self, 'mikrodies_label_text'):
            self.mikrodies_label_text.configure(bg="", fg=text_color)
        if hasattr(self, 'mikrodies_label'):
            self.mikrodies_label.configure(bg="", fg=text_color)
            
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
                # Get UTC time
                utc_time = now_utc.strftime("UTC %H:%M:%S %d/%m/%Y")
                
                # Get local time with timezone
                local_now = datetime.now()
                
                # Try to get proper timezone name
                try:
                    # Get timezone info
                    local_tz = local_now.astimezone()
                    tz_name = local_tz.tzinfo.tzname(local_tz)
                    
                    # If timezone name is just UTC, try to get offset
                    if tz_name == 'UTC':
                        offset = local_tz.strftime('%z')
                        if offset == '+0000':
                            tz_name = 'UTC'
                        else:
                            tz_name = f'UTC{offset[:3]}:{offset[3:]}'
                    
                    local_time = local_now.strftime("%H:%M:%S %d/%m/%Y")
                    
                    # Only show local time if different from UTC
                    if tz_name != 'UTC' or local_now.hour != now_utc.hour:
                        std_time = f"{utc_time}\n{tz_name} {local_time}"
                    else:
                        std_time = utc_time
                        
                except:
                    # Fallback to just UTC if timezone detection fails
                    std_time = utc_time
                
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