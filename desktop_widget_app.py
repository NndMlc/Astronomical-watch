#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astronomical Watch Desktop Widget Application
Modern widget + normal mode with astronomical time display
"""
import tkinter as tk
from tkinter import ttk, Canvas
import math
import time
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
        self.parent.title("Astronomical Watch")
        self.parent.geometry("400x600")  # Prilagođeno za vertikalni layout
        self.parent.resizable(True, True)
        self.parent.minsize(350, 550)  # Minimalne dimenzije
        
        # Restore normal decorations
        self.parent.overrideredirect(False)
        
        # Onemogući maximize dugme
        try:
            self.parent.attributes('-toolwindow', True)  # Windows
        except:
            try:
                self.parent.maxsize(800, 800)  # Ograniči maksimalnu veličinu
            except:
                pass
        
        # Center window
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - 200  # Adjusted for new width
        y = (screen_height // 2) - 300  # Adjusted for new height
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
        """Kreiraj jednostavan vertikalni normal mode UI - NOVA SPECIFIKACIJA SA GRADIENTOM"""
        
        # Main container sa scroll i gradient pozadinom
        self.main_canvas = tk.Canvas(self.parent, bg=self.current_theme.bottom_color, highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Kreiraj gradient pozadinu kao u widget mode-u
        # Pozovi nakon što je canvas pakovan
        self.parent.after(100, self.update_normal_gradient)
        
        self.main_frame = tk.Frame(self.main_canvas, bg='', bd=0)  # Transparentna pozadina
        canvas_frame = self.main_canvas.create_window(0, 0, anchor=tk.NW, window=self.main_frame)
        
        def configure_canvas(event=None):
            canvas_width = event.width if event else self.main_canvas.winfo_width()
            self.main_canvas.itemconfig(canvas_frame, width=canvas_width)
        
        self.main_canvas.bind('<Configure>', configure_canvas)
        
        # 1. HEADER sa dugmićima - OKRUGLI DIZAJN
        header_frame = tk.Frame(self.main_frame, bg='', bd=0)  # Transparentna pozadina
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Levo dugme - povratak na widget (okrugli)
        back_btn = tk.Button(header_frame,
                           text="←",
                           font=("Arial", 18, "bold"),
                           bg=self.current_theme.top_color,
                           fg="#ffffff",  # Beli tekst
                           bd=3,
                           relief='raised',
                           width=3,
                           height=1,
                           highlightthickness=2,
                           highlightbackground="#ffffff",  # Beli highlight
                           command=self.minimize_to_widget)
        back_btn.pack(side=tk.LEFT)
        self.add_button_hover_effect(back_btn)
        
        # Naslov u centru - SA OUTLINE
        self.title_label = self.create_text_with_outline_normal(
            header_frame, "Astronomical Watch", ("Arial", 16, "bold")
        )
        self.title_label.pack(side=tk.LEFT, expand=True)
        
        # Desno dugme - izbor jezika (okrugli)
        lang_btn = tk.Button(header_frame,
                           text="🌐",
                           font=("Arial", 16),
                           bg=self.current_theme.top_color,
                           fg="#ffffff",  # Beli tekst
                           bd=3,
                           relief='raised',
                           width=3,
                           height=1,
                           highlightthickness=2,
                           highlightbackground="#ffffff",  # Beli highlight
                           command=self.show_language_menu)
        lang_btn.pack(side=tk.RIGHT)
        self.add_button_hover_effect(lang_btn)
        
        # 2. DIES broj + label - SA OUTLINE
        dies_frame = tk.Frame(self.main_frame, bg='', bd=0)  # Transparentna pozadina
        dies_frame.pack(pady=(20, 5))
        
        self.dies_number_label = self.create_text_with_outline_normal(
            dies_frame, "000", ("DejaVu Sans Mono", 48, "bold")
        )
        self.dies_number_label.pack()
        
        self.dies_text_label = self.create_text_with_outline_normal(
            dies_frame, "Dies", ("Arial", 14)
        )
        self.dies_text_label.pack()
        
        # 3. MILIDIES broj + label - SA OUTLINE
        milides_frame = tk.Frame(self.main_frame, bg='', bd=0)  # Transparentna pozadina
        milides_frame.pack(pady=(15, 5))
        
        self.milides_number_label = self.create_text_with_outline_normal(
            milides_frame, "000", ("DejaVu Sans Mono", 48, "bold")
        )
        self.milides_number_label.pack()
        
        self.milides_text_label = self.create_text_with_outline_normal(
            milides_frame, "miliDies", ("Arial", 14)
        )
        self.milides_text_label.pack()
        
        # 4. PROGRESS BAR za mikroDies
        progress_frame = tk.Frame(self.main_frame, bg='', bd=0)  # Transparentna pozadina
        progress_frame.pack(pady=(20, 5), padx=40)
        
        self.main_progress_var = tk.IntVar(value=0)
        self.main_progress_bar = ttk.Progressbar(progress_frame,
                                               variable=self.main_progress_var,
                                               maximum=1000,
                                               length=300,
                                               mode='determinate')
        self.main_progress_bar.pack()
        
        # Label ISPOD progress bar-a sa trocifrenim mikroDies - SA OUTLINE
        self.mikro_label = self.create_text_with_outline_normal(
            progress_frame, "mikroDies: 000", ("DejaVu Sans Mono", 14)
        )
        self.mikro_label.pack(pady=(8, 0))
        
        # 5. STANDARDNO VREME - vidno odvojeno
        time_separator = tk.Frame(self.main_frame, bg="#ffffff", height=2)  # Beli separator
        time_separator.pack(fill=tk.X, padx=50, pady=(25, 15))
        
        time_frame = tk.Frame(self.main_frame, bg='', bd=0)  # Transparentna pozadina
        time_frame.pack(pady=(0, 20))
        
        self.standard_time_label = self.create_text_with_outline_normal(
            time_frame, "UTC+1  30/10/2025  12:34:56", ("DejaVu Sans Mono", 16)
        )
        self.standard_time_label.pack()
        
        # 6. DUGMAD sa slikama u jednom nizu - OKRUGLI I JEDNAKI
        buttons_frame = tk.Frame(self.main_frame, bg='', bd=0)  # Transparentna pozadina
        buttons_frame.pack(pady=(20, 30))
        
        # Jedan red dugmadi sa slikama - jednake veličine
        button_row = tk.Frame(buttons_frame, bg='', bd=0)  # Transparentna pozadina
        button_row.pack()
        
        # Definišemo jedinstvene parametre za sve dugmad - BELI TEKST
        button_config = {
            'font': ("Arial", 18, "bold"),
            'bg': self.current_theme.top_color,
            'fg': "#ffffff",  # Beli tekst
            'bd': 3,
            'relief': 'raised',
            'width': 3,  # Smanjena širina za okrugliji oblik
            'height': 1,  # Smanjena visina za okrugliji oblik
            'highlightthickness': 2,
            'highlightbackground': "#ffffff"  # Beli highlight
        }
        
        # Explanation - slovo "i"
        explanation_btn = tk.Button(button_row, text="i", 
                                   command=self.show_explanation, **button_config)
        explanation_btn.pack(side=tk.LEFT, padx=10)
        self.create_tooltip(explanation_btn, "Explanation")
        
        # Comparison - "<>"
        comparison_btn = tk.Button(button_row, text="<>", 
                                  command=self.show_comparison, **button_config)
        comparison_btn.pack(side=tk.LEFT, padx=10)
        self.create_tooltip(comparison_btn, "Comparison")
        
        # Calculation - kalkulator
        calculation_btn = tk.Button(button_row, text="🧮", 
                                   command=self.show_calculation, **button_config)
        calculation_btn.pack(side=tk.LEFT, padx=10)
        self.create_tooltip(calculation_btn, "Calculation")
        
        # Settings - mašinski ključ
        settings_btn = tk.Button(button_row, text="🔧", 
                               command=self.show_settings, **button_config)
        settings_btn.pack(side=tk.LEFT, padx=10)
        self.create_tooltip(settings_btn, "Settings")
        
        # Dodaj hover efekte za okrugli izgled
        for btn in [explanation_btn, comparison_btn, calculation_btn, settings_btn]:
            self.add_button_hover_effect(btn)
    
    def update_normal_gradient(self):
        """Update pozadinu normal mode-a - JEDNOSTAVAN PRISTUP"""
        try:
            # Jednostavan color-cycling sistem
            current_time = datetime.now(timezone.utc)
            hour = current_time.hour
            
            # Jednostavne boje na osnovu doba dana
            if 6 <= hour < 12:  # Jutro
                bg_color = "#4A90E2"  # Plava jutro
            elif 12 <= hour < 18:  # Dan
                bg_color = "#87CEEB"  # Svetlo plava dan
            elif 18 <= hour < 21:  # Veče
                bg_color = "#FF7F50"  # Narandžasta veče
            else:  # Noć
                bg_color = "#2F4F4F"  # Tamno plava noć
            
            print(f"DEBUG: Postavljam pozadinu na {bg_color} (sat: {hour})")
            
            # Postavi solid boju pozadine
            self.main_canvas.configure(bg=bg_color)
            
            # Update theme za dugmad
            if hasattr(self, 'current_theme'):
                self.current_theme.bottom_color = bg_color
                self.current_theme.top_color = "#ffffff"
                self.current_theme.text_color = "#ffffff"
            
            print("DEBUG: Pozadina uspešno postavljena")
            
        except Exception as e:
            print(f"DEBUG: Greška u pozadini: {e}")
            # Fallback na plavu boju
            self.main_canvas.configure(bg="#2563eb")
    
    def create_text_with_outline_normal(self, canvas, x, y, text, font, fill="white", outline="black", anchor="center"):
        """Kreira text sa outline na normal canvasu - JEDNOSTAVAN PRISTUP"""
        try:
            print(f"DEBUG: Kreiram tekst '{text}' na poziciji ({x}, {y})")
            
            # Samo glavni text sa velikim, kontrast fontom
            text_id = canvas.create_text(
                x, y, 
                text=text, 
                font=font, 
                fill="white",  # Uvek beli text za maksimalnu vidljivost
                anchor=anchor,
                tags="text_label"
            )
            
            print(f"DEBUG: Tekst kreiran sa ID {text_id}")
            canvas.update()
            return text_id
            
        except Exception as e:
            print(f"DEBUG: Greška u kreiranju teksta: {e}")
            return None
    
    def create_normal_labels(self):
        """Kreiranje labela za normal mode - JEDNOSTAVNA VERZIJA"""
        try:
            print("DEBUG: Kreiram normal mode labele...")
            
            # Veliki fontovi
            large_font = ("DejaVu Sans Mono", 32, "bold")  # Veći font
            medium_font = ("DejaVu Sans Mono", 18, "bold")
            
            # Clear postojeće
            self.main_canvas.delete("text_label")
            
            # Pozicije
            center_x = 200
            
            # Dies.miliDies
            self.dies_label = self.create_text_with_outline_normal(
                self.main_canvas, center_x, 100, "000.000", large_font
            )
            
            # Datum
            self.date_label = self.create_text_with_outline_normal(
                self.main_canvas, center_x, 180, "Date: Loading...", medium_font
            )
            
            # UTC time
            self.utc_label = self.create_text_with_outline_normal(
                self.main_canvas, center_x, 230, "UTC: Loading...", medium_font
            )
            
            print("DEBUG: Svi labeli kreirani - GOTOVO!")
            self.main_canvas.update()
            
        except Exception as e:
            print(f"DEBUG: Greška u labela: {e}")
    
        
    def minimize_to_widget(self):
        """Minimize to widget mode"""
        if self.on_minimize:
            self.on_minimize()
    
    def update_normal(self):
        """Update normal mode display - RADIKALNO JEDNOSTAVNO"""
        try:
            print("DEBUG: Update normal mode...")
            
            # Update gradient svakih 60 sekundi
            if not hasattr(self, '_last_normal_gradient_update') or time.time() - self._last_normal_gradient_update > 60:
                self.update_normal_gradient()
                self._last_normal_gradient_update = time.time()
            
            # Kreiraj labele ako ne postoje
            if not hasattr(self, 'dies_label') or self.dies_label is None:
                self.create_normal_labels()
            
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
                        'mikrodiet': reading.mikroDies,
                        'utc': datetime.now(timezone.utc)
                    }
                except:
                    data = AstronomicalCalculator.calculate_time()
            else:
                data = AstronomicalCalculator.calculate_time()
            
            # Update labele sa novim podacima
            if hasattr(self, 'dies_label') and self.dies_label:
                dies_text = f"{data['dies']:03d}.{data['milides']:03d}"
                self.main_canvas.itemconfig(self.dies_label, text=dies_text)
                print(f"DEBUG: Dies text updated: {dies_text}")
            
            if hasattr(self, 'date_label') and self.date_label:
                date_text = f"Date: {data['utc'].strftime('%d/%m/%Y')}"
                self.main_canvas.itemconfig(self.date_label, text=date_text)
                print(f"DEBUG: Date text updated: {date_text}")
            
            if hasattr(self, 'utc_label') and self.utc_label:
                utc_text = f"UTC: {data['utc'].strftime('%H:%M:%S')}"
                self.main_canvas.itemconfig(self.utc_label, text=utc_text)
                print(f"DEBUG: UTC text updated: {utc_text}")
            
            self.main_canvas.update()
            print("DEBUG: Normal mode update završen!")
            
        except Exception as e:
            print(f"DEBUG: Greška u normal update: {e}")
        
        # Schedule next update
        self.parent.after(1000, self.update_normal)
    
    def create_tooltip(self, widget, text):
        """Kreiraj tooltip za widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text,
                           background="lightyellow",
                           relief="solid",
                           borderwidth=1,
                           font=("Arial", 9))
            label.pack()
            
            # Auto-hide nakon 2 sekunde
            tooltip.after(2000, tooltip.destroy)
            
            # Sakrij kad se miš pomeri
            def hide_tooltip(event):
                tooltip.destroy()
            widget.bind("<Leave>", hide_tooltip)
        
        widget.bind("<Enter>", show_tooltip)
    
    def add_button_hover_effect(self, button):
        """Dodaj hover efekat za okrugli izgled dugmeta"""
        original_bg = button.cget('bg')
        original_relief = button.cget('relief')
        
        def on_enter(event):
            button.config(bg=self.current_theme.text_color, 
                         fg=self.current_theme.bottom_color,
                         relief='sunken')
        
        def on_leave(event):
            button.config(bg=original_bg, 
                         fg=self.current_theme.text_color,
                         relief=original_relief)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def show_language_menu(self):
        """Prikaži meni za izbor jezika"""
        # Placeholder - može se implementirati kasnije
        print("Language menu - to be implemented")
    
    def show_explanation(self):
        """Prikaži explanation karticu"""
        # Placeholder - može se implementirati kasnije
        print("Explanation card - to be implemented")
    
    def show_comparison(self):
        """Prikaži comparison karticu"""
        # Placeholder - može se implementirati kasnije
        print("Comparison card - to be implemented")
    
    def show_calculation(self):
        """Prikaži calculation karticu"""
        # Placeholder - može se implementirati kasnije
        print("Calculation card - to be implemented")
    
    def show_settings(self):
        """Prikaži settings karticu"""
        # Placeholder - može se implementirati kasnije
        print("Settings card - to be implemented")

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