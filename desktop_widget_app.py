#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astronomical Watch Desktop Widget Application
Modern widget + normal mode with astronomical time display
"""
import tkinter as tk
from tkinter import ttk, Canvas
import math
from datetime import datetime, timezone
import threading
import time
import sys
import os

# Add src to path for gradient access
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from astronomical_watch.ui.gradient import get_sky_theme, create_gradient_colors, SkyTheme
    GRADIENT_AVAILABLE = True
except ImportError:
    GRADIENT_AVAILABLE = False
    # Fallback theme
    class SkyTheme:
        def __init__(self, top_color, bottom_color, text_color):
            self.top_color = top_color
            self.bottom_color = bottom_color
            self.text_color = text_color
    
    def get_sky_theme(dt=None):
        return SkyTheme("#1e3a8a", "#3b82f6", "#ffffff")
    
    def create_gradient_colors(theme, steps=256):
        return [theme.top_color] * steps

# Dodaj src u path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from astronomical_watch.core.astro_time_core import AstroYear
    HAS_CORE = True
except ImportError:
    HAS_CORE = False

class AstronomicalCalculator:
    """Embedded calculator ako core nije dostupan"""
    
    @staticmethod
    def calculate_time():
        now = datetime.now(timezone.utc)
        equinox = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
        
        delta_seconds = (now - equinox).total_seconds()
        boundary_offset = 23*3600 + 15*60 + 54
        adjusted_seconds = delta_seconds + boundary_offset
        
        total_days = adjusted_seconds / 86400.0
        dies = max(0, int(total_days))
        day_fraction = total_days - dies
        
        milides_total = day_fraction * 1000.0
        milides = int(milides_total)
        milides_fraction = milides_total - milides
        
        mikrodiet = int(milides_fraction * 1000.0)
        
        return {
            'dies': dies,
            'milides': milides,
            'mikrodiet': mikrodiet,
            'utc': now
        }

class WidgetMode:
    """Modern widget mode sa gradientom i zaobljenim uglovima"""
    
    def __init__(self, parent, on_double_click=None):
        self.parent = parent
        self.on_double_click = on_double_click
        self.current_theme = None
        self.update_running = False
        
        # Setup modern widget window
        self.setup_modern_widget()
        self.create_gradient_canvas()
        self.create_content()
        
        # Bind double click na sve komponente
        self.bind_double_click()
        
        # Start updates
        self.start_updates()
        
    def setup_modern_widget(self):
        """Setup modern widget window properties"""
        # Remove window decorations (title bar)
        self.parent.overrideredirect(True)
        
        # Povećana širina za margine brojeva, optimalna visina za sve elemente
        self.widget_width = 160  # Povećano sa 140 na 160
        self.widget_height = 85  # Povećano sa 78 na 85 za dovoljno prostora
        
        self.parent.geometry(f"{self.widget_width}x{self.widget_height}")
        self.parent.resizable(False, False)
        
        # Always on top and corner positioning
        try:
            # NE STAVLJA always on top - widget ostaje na desktopu
            # self.parent.attributes('-topmost', True)  # Uklonjeno
            
            # Position u desni gornji ugao sa minimalnim margin (default pozicija)
            screen_width = self.parent.winfo_screenwidth()
            x_pos = screen_width - self.widget_width - 10  # Malo veći margin za desktop
            y_pos = 10  # Malo veći margin za desktop
            self.parent.geometry(f"+{x_pos}+{y_pos}")
        except:
            pass
    
    def create_gradient_canvas(self):
        """Kreiraj canvas sa gradientom"""
        self.canvas = tk.Canvas(
            self.parent, 
            width=self.widget_width, 
            height=self.widget_height,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Update gradient initially
        self.update_gradient()
    
    def update_gradient(self):
        """Update gradient pozadinu na osnovu trenutnog vremena"""
        if not GRADIENT_AVAILABLE:
            # Fallback solid color
            self.canvas.configure(bg="#1e3a8a")
            self.current_theme = SkyTheme("#1e3a8a", "#3b82f6", "#ffffff")
            return
            
        # Get current sky theme
        current_time = datetime.now(timezone.utc)
        self.current_theme = get_sky_theme(current_time)
        
        # Create gradient
        gradient_colors = create_gradient_colors(self.current_theme, steps=self.widget_height)
        
        # Clear previous gradient
        self.canvas.delete("gradient")
        
        # Draw gradient lines
        for i, color in enumerate(gradient_colors):
            self.canvas.create_line(
                0, i, self.widget_width, i,
                fill=color, width=1, tags="gradient"
            )
        
        # UKLONJEN rounded corners - ostaju normalni uglovi
    
    def get_contrast_color(self, background_theme):
        """Uvek vrati belu boju za bolju vidljivost"""
        return "#ffffff"
    
    def create_text_with_outline(self, x, y, text, font, fill_color="#ffffff", outline_color="#000000", outline_width=1, tags="content"):
        """Kreira tekst sa crnom ivicom za bolju vidljivost"""
        # Kreiraj crnu ivicu sa offset-ima
        offsets = [
            (-outline_width, -outline_width), (-outline_width, 0), (-outline_width, outline_width),
            (0, -outline_width), (0, outline_width),
            (outline_width, -outline_width), (outline_width, 0), (outline_width, outline_width)
        ]
        
        # Kreiraj outline (crnu ivicu)
        outline_texts = []
        for dx, dy in offsets:
            outline_text = self.canvas.create_text(
                x + dx, y + dy, text=text, font=font, fill=outline_color, tags=tags
            )
            outline_texts.append(outline_text)
        
        # Kreiraj glavni tekst (beli) preko outline-a
        main_text = self.canvas.create_text(
            x, y, text=text, font=font, fill=fill_color, tags=tags
        )
        
        return main_text, outline_texts
    
    def create_content(self):
        """Kreiraj sadržaj widget-a na canvas-u - kompaktan dizajn sa outline textom"""
        # Clear previous content
        self.canvas.delete("content")
        
        # 1. Naslov većim fontom - SAMO BELA BOJA (bez outline)
        self.title_text = self.canvas.create_text(
            self.widget_width // 2, 8,
            text="Astronomical Watch",
            font=("Segoe UI", 9, "normal"),
            fill="#ffffff",
            tags="content"
        )
        
        # 2. Brojevi koji pokazuju Dies i miliDies - SKORO DUPLO VEĆI
        self.time_text, self.time_outline = self.create_text_with_outline(
            self.widget_width // 2, 35,  # Spušteno sa 25 na 35
            "0.000",  # Dies bez padding, miliDies trocifreni
            ("DejaVu Sans Mono", 28, "bold"),  # tkinter će koristiti fallback ako nema
            tags="content"
        )
        
        # 3. Label veći font - PRIBLIŽEN BROJEVIMA
        self.format_text = self.canvas.create_text(
            self.widget_width // 2, 57,  # Podesio sa 55 na 57
            text="Dies . miliDies",
            font=("Segoe UI", 10, "normal"),
            fill="#ffffff",
            tags="content"
        )
        
        # 4. Progress bar ISPOD LABELA
        bar_y = 75  # Spušteno sa 68 na 75 za dovoljno prostora ispod labela
        bar_height = 5
        bar_margin = 3
        
        # Progress bar background - tamna za kontrast sa belom
        self.progress_bg = self.canvas.create_rectangle(
            bar_margin, bar_y, self.widget_width - bar_margin, bar_y + bar_height,
            fill="#333333", outline="",
            tags="content"
        )
        
        # Progress bar fill - bela boja
        self.progress_fill = self.canvas.create_rectangle(
            bar_margin + 1, bar_y + 1, bar_margin + 1, bar_y + bar_height - 1,
            fill="#ffffff", outline="",
            tags="content"
        )
        
        # Nema outline za naslov i label - samo brojevi imaju outline
        
    def bind_double_click(self):
        """Bind double click event na canvas i sve elemente"""
        def handle_double_click(event=None):
            if self.on_double_click:
                self.on_double_click()
        
        # Bind na canvas i parent window
        self.canvas.bind("<Double-Button-1>", handle_double_click)
        self.parent.bind("<Double-Button-1>", handle_double_click)
    
    def start_updates(self):
        """Pokreni redovne update-ove"""
        self.update_running = True
        self.update_widget()
    
    def stop_updates(self):
        """Zaustavi update-ove"""
        self.update_running = False
    
    def update_text_with_outline(self, main_text_id, outline_ids, new_text):
        """Update tekst sa outline-om"""
        # Proveri da atributi postoje
        if not hasattr(self, 'canvas') or main_text_id is None or outline_ids is None:
            return
            
        # Update outline tekstove
        for outline_id in outline_ids:
            try:
                self.canvas.itemconfig(outline_id, text=new_text)
            except:
                pass
        
        # Update glavni tekst
        try:
            self.canvas.itemconfig(main_text_id, text=new_text)
        except:
            pass
    
    def update_widget(self):
        """Update widget data sa gradientom i vizuelima"""
        if not self.update_running:
            return
        
        # Proveri da su svi potrebni atributi inicijalizovani
        if not hasattr(self, 'canvas') or not hasattr(self, 'time_text'):
            # Schedule retry
            if self.update_running:
                self.parent.after(100, self.update_widget)
            return
            
        try:
            # Get astronomical data
            if HAS_CORE:
                try:
                    current_eq = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
                    next_eq = datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
                    
                    ay = AstroYear(current_eq, next_eq)
                    reading = ay.reading(datetime.now(timezone.utc))
                    
                    data = {
                        'dies': reading.day_index,
                        'milides': reading.miliDies,
                        'mikrodiet': reading.mikroDies
                    }
                except:
                    # Fallback na embedded calculator
                    data = AstronomicalCalculator.calculate_time()
            else:
                # Koristi embedded calculator
                data = AstronomicalCalculator.calculate_time()
            
            # Update gradient (periodically)
            import time
            if not hasattr(self, '_last_gradient_update') or time.time() - self._last_gradient_update > 60:
                self.update_gradient()
                self.create_content()  # Recreate content with new colors
                self._last_gradient_update = time.time()
            
            # Update text displays sa outline
            # Dies bez fiksne širine, miliDies uvek trocifreni, tačka na istoj poziciji
            time_str = "{}.{:03d}".format(data['dies'], data['milides'])
            if hasattr(self, 'time_text') and hasattr(self, 'time_outline'):
                self.update_text_with_outline(self.time_text, self.time_outline, time_str)
            
            # Update progress bar za mikroDies (0-1000) - bela boja
            mikro_value = data['mikrodiet']
            if hasattr(self, 'progress_fill'):
                bar_margin = 3  # Usklađeno sa create_content
                bar_y = 75  # Ista pozicija kao u create_content
                bar_height = 5  # Ista visina kao u create_content
                bar_width = self.widget_width - (2 * bar_margin) - 2  # Account for border
                progress_width = (mikro_value / 1000.0) * bar_width
                
                # Update progress fill - koordinate usklađene sa background
                self.canvas.coords(
                    self.progress_fill,
                    bar_margin + 1, bar_y + 1,  # y=76 (bar_y + 1)
                    bar_margin + 1 + progress_width, bar_y + bar_height - 1  # y=79 (bar_y + height - 1)
                )
                
                # Keep progress bar white
                self.canvas.itemconfig(self.progress_fill, fill="#ffffff")
            
            # Outline tekstovi se ne menjaju jer su statični
            
        except Exception as e:
            # Error handling - show fallback sa outline textom
            try:
                if hasattr(self, 'time_text') and hasattr(self, 'time_outline'):
                    self.update_text_with_outline(self.time_text, self.time_outline, "ERR.ERR")
                # UKLONJEN mikroDies error display
            except:
                pass
        
        # Schedule next update
        if self.update_running:
            self.parent.after(100, self.update_widget)  # Update every 100ms

class NormalMode:
    """Prošireni normal mode aplikacije"""
    
    def __init__(self, parent, on_minimize=None):
        self.parent = parent
        self.on_minimize = on_minimize
        
        self.setup_normal_window()
        self.create_normal_ui()
        self.update_normal()
        
    def setup_normal_window(self):
        """Setup normal mode window sa gradientom"""
        self.parent.title("Astronomical Watch - Full Display")
        self.parent.geometry("520x650")  # Povećano za dodatni sadržaj
        self.parent.resizable(True, True)
        self.parent.minsize(500, 600)  # Minimalne dimenzije
        
        # Restore normal decorations
        self.parent.overrideredirect(False)
        
        # Center window
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - 260  # Adjusted for new width
        y = (screen_height // 2) - 325  # Adjusted for new height
        self.parent.geometry(f"+{x}+{y}")
        
        # Get current sky theme
        if GRADIENT_AVAILABLE:
            current_time = datetime.now(timezone.utc)
            self.current_theme = get_sky_theme(current_time)
        else:
            self.current_theme = SkyTheme("#1e3a8a", "#3b82f6", "#ffffff")
        
        # Apply gradient background
        self.parent.configure(bg=self.current_theme.bottom_color)
    
    def draw_normal_gradient(self):
        """Draw gradient background for normal mode"""
        if not GRADIENT_AVAILABLE:
            self.main_canvas.configure(bg=self.current_theme.bottom_color)
            return
        
        # Get canvas dimensions
        self.parent.update_idletasks()
        canvas_width = self.main_canvas.winfo_width()
        canvas_height = self.main_canvas.winfo_height()
        
        if canvas_width < 100 or canvas_height < 100:  # Default size
            canvas_width = 480
            canvas_height = 420
        
        # Create gradient
        gradient_colors = create_gradient_colors(self.current_theme, steps=canvas_height)
        
        # Clear canvas
        self.main_canvas.delete("gradient")
        
        # Draw gradient lines
        for i, color in enumerate(gradient_colors):
            if i < canvas_height:
                self.main_canvas.create_line(
                    0, i, canvas_width, i,
                    fill=color, width=1, tags="gradient"
                )
    
    def create_normal_ui(self):
        """Kreiraj full UI sa gradientom"""
        
        # Main canvas for gradient background
        self.main_canvas = tk.Canvas(
            self.parent,
            highlightthickness=0,
            bd=0
        )
        self.main_canvas.pack(fill='both', expand=True)
        
        # Draw gradient background
        self.draw_normal_gradient()
        
        # Main frame over canvas
        self.main_frame = tk.Frame(self.main_canvas, bg='', highlightthickness=0, bd=0)
        self.main_frame.configure(bg=self.current_theme.bottom_color)
        
        canvas_frame = self.main_canvas.create_window(0, 0, anchor='nw', window=self.main_frame)
        
        # Configure canvas scrolling
        def configure_canvas(event):
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
            canvas_width = event.width
            self.main_canvas.itemconfig(canvas_frame, width=canvas_width)
        
        self.main_canvas.bind('<Configure>', configure_canvas)
        
        # Header sa minimize dugmetom
        header_frame = tk.Frame(self.main_frame, bg=self.current_theme.bottom_color)
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Minimize dugme u gornjem desnom uglu
        minimize_btn = tk.Button(header_frame,
                               text="━",  # Unicode minimize simbol
                               font=("Arial", 14, "bold"),
                               bg=self.current_theme.top_color,
                               fg=self.current_theme.text_color,
                               bd=1,
                               relief='raised',
                               width=3,
                               command=self.minimize_to_widget)
        minimize_btn.pack(side=tk.RIGHT)
        
        title = tk.Label(header_frame,
                        text="ASTRONOMICAL WATCH",
                        font=("Segoe UI", 16, "bold"),
                        bg=self.current_theme.bottom_color,
                        fg=self.current_theme.text_color)
        title.pack(side=tk.LEFT)
        
        subtitle = tk.Label(header_frame,
                           text="mikroDies Precision • Web API Style",
                           font=("Segoe UI", 11),
                           bg=self.current_theme.bottom_color,
                           fg=self.current_theme.text_color)
        subtitle.pack(side=tk.LEFT, padx=(0, 10))
        
        # Main time card with semi-transparent background
        time_frame = tk.Frame(self.main_frame, bg=self.current_theme.top_color, relief='raised', bd=1)
        time_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.main_time_label = tk.Label(time_frame,
                                       text="000.000.000",
                                       font=("Consolas", 24, "bold"),
                                       bg=self.current_theme.top_color,
                                       fg=self.current_theme.text_color)
        self.main_time_label.pack(pady=15)
        
        format_desc = tk.Label(time_frame,
                              text="Dies . miliDies . mikroDies",
                              font=("Segoe UI", 10),
                              bg=self.current_theme.top_color,
                              fg=self.current_theme.text_color)
        format_desc.pack(pady=(0, 10))
        
        # Info grid - PROŠIRENO kao web API prikaz
        info_frame = tk.Frame(self.main_frame, bg=self.current_theme.bottom_color)
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Timestamp card - kao web API
        timestamp_frame = tk.Frame(info_frame, bg=self.current_theme.top_color, relief='raised', bd=1)
        timestamp_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(timestamp_frame, text="TIMESTAMPS",
                font=("Arial", 10, "bold"), bg=self.current_theme.top_color, fg=self.current_theme.text_color).pack(pady=(8, 5))
        
        self.timestamp_basic_label = tk.Label(timestamp_frame,
                                             text="Basic: 000.000",
                                             font=("Consolas", 12),
                                             bg=self.current_theme.top_color,
                                             fg=self.current_theme.text_color)
        self.timestamp_basic_label.pack(pady=2)
        
        self.timestamp_full_label = tk.Label(timestamp_frame,
                                            text="Full: 000.000.000",
                                            font=("Consolas", 12),
                                            bg=self.current_theme.top_color,
                                            fg=self.current_theme.text_color)
        self.timestamp_full_label.pack(pady=(2, 8))
        
        # Glavni sadržaj - dve kolone
        content_frame = tk.Frame(info_frame, bg=self.current_theme.bottom_color)
        content_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left column - Components
        left_col = tk.Frame(content_frame, bg=self.current_theme.bottom_color)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_col, text="ASTRONOMICAL COMPONENTS",
                font=("Arial", 10, "bold"), bg=self.current_theme.bottom_color, fg=self.current_theme.text_color).pack(anchor='w', pady=(0, 5))
        self.dies_label = tk.Label(left_col,
                                  text="Dies: ---",
                                  font=("Consolas", 10),
                                  bg=self.current_theme.bottom_color,
                                  fg=self.current_theme.text_color)
        self.dies_label.pack(anchor='w', pady=2)
        
        self.milides_label = tk.Label(left_col,
                                     text="miliDies: ---",
                                     font=("Consolas", 10),
                                     bg=self.current_theme.bottom_color,
                                     fg=self.current_theme.text_color)
        self.milides_label.pack(anchor='w', pady=2)
        
        self.mikrodiet_label = tk.Label(left_col,
                                       text="mikroDies: ---",
                                       font=("Consolas", 10),
                                       bg=self.current_theme.bottom_color,
                                       fg=self.current_theme.text_color)
        self.mikrodiet_label.pack(anchor='w', pady=2)
        
        self.mikro_fraction_label = tk.Label(left_col,
                                            text="μDies Fraction: ---.---",
                                            font=("Consolas", 10),
                                            bg=self.current_theme.bottom_color,
                                            fg=self.current_theme.text_color)
        self.mikro_fraction_label.pack(anchor='w', pady=2)
        
        # Right column - Time References
        right_col = tk.Frame(content_frame, bg=self.current_theme.bottom_color)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right_col, text="TIME REFERENCES",
                font=("Arial", 10, "bold"), bg=self.current_theme.bottom_color, fg=self.current_theme.text_color).pack(anchor='e', pady=(0, 5))
        self.utc_label = tk.Label(right_col,
                                 text="UTC: ---",
                                 font=("Consolas", 10),
                                 bg=self.current_theme.bottom_color,
                                 fg=self.current_theme.text_color)
        self.utc_label.pack(anchor='e', pady=2)
        
        self.utc_iso_label = tk.Label(right_col,
                                     text="UTC ISO: ---",
                                     font=("Consolas", 9),
                                     bg=self.current_theme.bottom_color,
                                     fg=self.current_theme.text_color)
        self.utc_iso_label.pack(anchor='e', pady=2)
        
        self.local_label = tk.Label(right_col,
                                   text="Local: ---",
                                   font=("Consolas", 10),
                                   bg=self.current_theme.bottom_color,
                                   fg=self.current_theme.text_color)
        self.local_label.pack(anchor='e', pady=2)
        
        # Equinox information card
        equinox_frame = tk.Frame(info_frame, bg=self.current_theme.top_color, relief='raised', bd=1)
        equinox_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(equinox_frame, text="EQUINOX PERIOD",
                font=("Arial", 10, "bold"), bg=self.current_theme.top_color, fg=self.current_theme.text_color).pack(pady=(8, 5))
        
        self.current_equinox_label = tk.Label(equinox_frame,
                                             text="Current: 2025-03-20T09:01:28Z",
                                             font=("Consolas", 9),
                                             bg=self.current_theme.top_color,
                                             fg=self.current_theme.text_color)
        self.current_equinox_label.pack(pady=1)
        
        self.next_equinox_label = tk.Label(equinox_frame,
                                          text="Next: 2026-03-20T14:45:50Z",
                                          font=("Consolas", 9),
                                          bg=self.current_theme.top_color,
                                          fg=self.current_theme.text_color)
        self.next_equinox_label.pack(pady=(1, 8))
        
        # Progress section
        progress_frame = tk.Frame(self.parent, bg=self.card_color, relief='sunken', bd=2)
        progress_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(progress_frame,
                text="mikroDies Progress (0-1000)",
                font=("Arial", 10, "bold"),
                bg=self.card_color,
                fg=self.text_color).pack(pady=(10, 5))
        
        self.main_progress_var = tk.IntVar(value=0)
        self.main_progress_bar = ttk.Progressbar(progress_frame,
                                               variable=self.main_progress_var,
                                               maximum=1000,
                                               length=380,
                                               mode='determinate')
        self.main_progress_bar.pack(pady=(0, 5))
        
        self.progress_label = tk.Label(progress_frame,
                                      text="0 / 1000 mikroDies",
                                      font=("Arial", 9),
                                      bg=self.card_color,
                                      fg='#cccccc')
        self.progress_label.pack(pady=(0, 10))
        
        # Control buttons
        button_frame = tk.Frame(self.parent, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        minimize_btn = tk.Button(button_frame,
                               text="Minimize to Widget",
                               command=self.minimize_to_widget,
                               bg=self.card_color,
                               fg=self.text_color,
                               relief='raised',
                               bd=2,
                               padx=20)
        minimize_btn.pack(side=tk.LEFT)
        
        close_btn = tk.Button(button_frame,
                            text="Close Application",
                            command=self.parent.quit,
                            bg='#8b0000',
                            fg=self.text_color,
                            relief='raised',
                            bd=2,
                            padx=20)
        close_btn.pack(side=tk.RIGHT)
        
    def minimize_to_widget(self):
        """Minimize to widget mode"""
        if self.on_minimize:
            self.on_minimize()
    
    def update_normal(self):
        """Update normal mode display - WEB API stil"""
        try:
            if HAS_CORE:
                try:
                    current_eq = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
                    next_eq = datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
                    
                    ay = AstroYear(current_eq, next_eq)
                    reading = ay.reading(datetime.now(timezone.utc))
                    
                    data = {
                        'dies': reading.day_index,
                        'milides': reading.miliDies,
                        'mikrodiet': reading.mikroDies,
                        'mikro_fraction': reading.mikroDies_fraction,
                        'utc': reading.utc,
                        'current_equinox': current_eq,
                        'next_equinox': next_eq
                    }
                except:
                    calc_data = AstronomicalCalculator.calculate_time()
                    data = {
                        'dies': calc_data['dies'],
                        'milides': calc_data['milides'], 
                        'mikrodiet': calc_data['mikrodiet'],
                        'mikro_fraction': 0.0,
                        'utc': calc_data['utc'],
                        'current_equinox': datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc),
                        'next_equinox': datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
                    }
            else:
                calc_data = AstronomicalCalculator.calculate_time()
                data = {
                    'dies': calc_data['dies'],
                    'milides': calc_data['milides'], 
                    'mikrodiet': calc_data['mikrodiet'],
                    'mikro_fraction': 0.0,
                    'utc': calc_data['utc'],
                    'current_equinox': datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc),
                    'next_equinox': datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
                }
            
            # Main time display - NOVO FORMATIRANJE
            time_str = "{}.{:03d}.{:03d}".format(
                data['dies'], data['milides'], data['mikrodiet']
            )
            self.main_time_label.config(text=time_str)
            
            # Timestamps - kao web API
            basic_timestamp = "{}.{:03d}".format(data['dies'], data['milides'])
            full_timestamp = "{}.{:03d}.{:03d}".format(data['dies'], data['milides'], data['mikrodiet'])
            
            self.timestamp_basic_label.config(text=f"Basic: {basic_timestamp}")
            self.timestamp_full_label.config(text=f"Full: {full_timestamp}")
            
            # Components - POBOLJŠANO
            self.dies_label.config(text=f"Dies: {data['dies']}")
            self.milides_label.config(text=f"miliDies: {data['milides']}")
            self.mikrodiet_label.config(text=f"mikroDies: {data['mikrodiet']}")
            self.mikro_fraction_label.config(text=f"μDies Fraction: {data['mikro_fraction']:.3f}")
            
            # Time references - PROŠIRENO
            utc_str = data['utc'].strftime('%H:%M:%S UTC')
            self.utc_label.config(text=f"UTC: {utc_str}")
            
            # UTC ISO format - kao web API
            utc_iso = data['utc'].isoformat().replace("+00:00", "Z")
            # Skrati ISO da stane u prikaz
            if len(utc_iso) > 20:
                utc_iso = utc_iso[:19] + "Z"
            self.utc_iso_label.config(text=f"UTC ISO: {utc_iso}")
            
            try:
                local_time = data['utc'].replace(tzinfo=timezone.utc).astimezone()
                local_str = local_time.strftime('%H:%M:%S')
                self.local_label.config(text=f"Local: {local_str}")
            except:
                self.local_label.config(text="Local: --:--:--")
            
            # Equinox information - NOVO
            current_eq_str = data['current_equinox'].strftime('%Y-%m-%dT%H:%M:%SZ')
            next_eq_str = data['next_equinox'].strftime('%Y-%m-%dT%H:%M:%SZ')
            
            self.current_equinox_label.config(text=f"Current: {current_eq_str}")
            self.next_equinox_label.config(text=f"Next: {next_eq_str}")
            
            # Progress - POBOLJŠANO
            self.main_progress_var.set(data['mikrodiet'])
            self.progress_label.config(text=f"mikroDies: {data['mikrodiet']} / 1000 ({data['mikrodiet']/10:.1f}%)")
            
        except Exception as e:
            self.main_time_label.config(text="ERROR")
            print(f"Normal mode update error: {e}")
        
        # Schedule next update
        self.parent.after(100, self.update_normal)

class AstronomicalWatchApp:
    """Glavna aplikacija - widget/normal mode manager"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.current_mode = None
        self.widget_mode = None
        self.normal_mode = None
        
        # Start in widget mode
        self.show_widget_mode()
        
    def show_widget_mode(self):
        """Prikaži widget mode"""
        # Clear current mode
        if self.current_mode:
            for widget in self.root.winfo_children():
                widget.destroy()
        
        # Create widget mode
        self.widget_mode = WidgetMode(self.root, on_double_click=self.show_normal_mode)
        self.current_mode = 'widget'
        
    def show_normal_mode(self):
        """Prikaži normal mode"""
        # Clear current mode
        if self.current_mode:
            for widget in self.root.winfo_children():
                widget.destroy()
        
        # Create normal mode
        self.normal_mode = NormalMode(self.root, on_minimize=self.show_widget_mode)
        self.current_mode = 'normal'
        
    def run(self):
        """Pokreni aplikaciju"""
        print("=== ASTRONOMICAL WATCH DESKTOP ===")
        print("Starts in WIDGET MODE:")
        print("- Minimalistic widget in corner")
        print("- Shows Dies.miliDies with progress bar")
        print("- DOUBLE-CLICK anywhere to open Normal Mode")
        print()
        print("Normal Mode features:")
        print("- Full astronomical display")
        print("- Complete mikroDies precision")
        print("- Click 'Minimize to Widget' to return")
        print()
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Application closed")

def main():
    """Glavna funkcija"""
    app = AstronomicalWatchApp()
    app.run()

if __name__ == "__main__":
    main()