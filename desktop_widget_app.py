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
        """Kreiraj jednostavan vertikalni normal mode UI - NOVA SPECIFIKACIJA"""
        
        # Main container sa scroll
        self.main_canvas = tk.Canvas(self.parent, bg=self.current_theme.bottom_color, highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.main_frame = tk.Frame(self.main_canvas, bg=self.current_theme.bottom_color)
        canvas_frame = self.main_canvas.create_window(0, 0, anchor=tk.NW, window=self.main_frame)
        
        def configure_canvas(event=None):
            canvas_width = event.width if event else self.main_canvas.winfo_width()
            self.main_canvas.itemconfig(canvas_frame, width=canvas_width)
        
        self.main_canvas.bind('<Configure>', configure_canvas)
        
        # 1. HEADER sa dugmićima - OKRUGLI DIZAJN
        header_frame = tk.Frame(self.main_frame, bg=self.current_theme.bottom_color)
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Levo dugme - povratak na widget (okrugli)
        back_btn = tk.Button(header_frame,
                           text="←",
                           font=("Arial", 18, "bold"),
                           bg=self.current_theme.top_color,
                           fg=self.current_theme.text_color,
                           bd=3,
                           relief='raised',
                           width=3,
                           height=1,
                           highlightthickness=2,
                           highlightbackground=self.current_theme.text_color,
                           command=self.minimize_to_widget)
        back_btn.pack(side=tk.LEFT)
        self.add_button_hover_effect(back_btn)
        
        # Naslov u centru
        title = tk.Label(header_frame,
                        text="Astronomical Watch",
                        font=("Arial", 16, "bold"),
                        bg=self.current_theme.bottom_color,
                        fg=self.current_theme.text_color)
        title.pack(side=tk.LEFT, expand=True)
        
        # Desno dugme - izbor jezika (okrugli)
        lang_btn = tk.Button(header_frame,
                           text="🌐",
                           font=("Arial", 16),
                           bg=self.current_theme.top_color,
                           fg=self.current_theme.text_color,
                           bd=3,
                           relief='raised',
                           width=3,
                           height=1,
                           highlightthickness=2,
                           highlightbackground=self.current_theme.text_color,
                           command=self.show_language_menu)
        lang_btn.pack(side=tk.RIGHT)
        self.add_button_hover_effect(lang_btn)
        
        # 2. DIES broj + label
        dies_frame = tk.Frame(self.main_frame, bg=self.current_theme.bottom_color)
        dies_frame.pack(pady=(20, 5))
        
        self.dies_number_label = tk.Label(dies_frame,
                                         text="000",
                                         font=("DejaVu Sans Mono", 48, "bold"),
                                         bg=self.current_theme.bottom_color,
                                         fg=self.current_theme.text_color)
        self.dies_number_label.pack()
        
        tk.Label(dies_frame,
                text="Dies",
                font=("Arial", 14),
                bg=self.current_theme.bottom_color,
                fg=self.current_theme.text_color).pack()
        
        # 3. MILIDIES broj + label
        milides_frame = tk.Frame(self.main_frame, bg=self.current_theme.bottom_color)
        milides_frame.pack(pady=(15, 5))
        
        self.milides_number_label = tk.Label(milides_frame,
                                            text="000",
                                            font=("DejaVu Sans Mono", 48, "bold"),
                                            bg=self.current_theme.bottom_color,
                                            fg=self.current_theme.text_color)
        self.milides_number_label.pack()
        
        tk.Label(milides_frame,
                text="miliDies",
                font=("Arial", 14),
                bg=self.current_theme.bottom_color,
                fg=self.current_theme.text_color).pack()
        
        # 4. PROGRESS BAR za mikroDies
        progress_frame = tk.Frame(self.main_frame, bg=self.current_theme.bottom_color)
        progress_frame.pack(pady=(20, 5), padx=40)
        
        self.main_progress_var = tk.IntVar(value=0)
        self.main_progress_bar = ttk.Progressbar(progress_frame,
                                               variable=self.main_progress_var,
                                               maximum=1000,
                                               length=300,
                                               mode='determinate')
        self.main_progress_bar.pack()
        
        # Label ISPOD progress bar-a sa trocifrenim mikroDies
        self.mikro_label = tk.Label(progress_frame,
                                   text="mikroDies: 000",
                                   font=("DejaVu Sans Mono", 14),
                                   bg=self.current_theme.bottom_color,
                                   fg=self.current_theme.text_color)
        self.mikro_label.pack(pady=(8, 0))
        
        # 5. STANDARDNO VREME - vidno odvojeno
        time_separator = tk.Frame(self.main_frame, bg=self.current_theme.text_color, height=1)
        time_separator.pack(fill=tk.X, padx=50, pady=(25, 15))
        
        time_frame = tk.Frame(self.main_frame, bg=self.current_theme.bottom_color)
        time_frame.pack(pady=(0, 20))
        
        self.standard_time_label = tk.Label(time_frame,
                                           text="UTC+1  30/10/2025  12:34:56",
                                           font=("DejaVu Sans Mono", 16),
                                           bg=self.current_theme.bottom_color,
                                           fg=self.current_theme.text_color)
        self.standard_time_label.pack()
        
        # 6. DUGMAD sa slikama u jednom nizu - OKRUGLI I JEDNAKI
        buttons_frame = tk.Frame(self.main_frame, bg=self.current_theme.bottom_color)
        buttons_frame.pack(pady=(20, 30))
        
        # Jedan red dugmadi sa slikama - jednake veličine
        button_row = tk.Frame(buttons_frame, bg=self.current_theme.bottom_color)
        button_row.pack()
        
        # Definišemo jedinstvene parametre za sve dugmad
        button_config = {
            'font': ("Arial", 18, "bold"),
            'bg': self.current_theme.top_color,
            'fg': self.current_theme.text_color,
            'bd': 3,
            'relief': 'raised',
            'width': 3,  # Smanjena širina za okrugliji oblik
            'height': 1,  # Smanjena visina za okrugliji oblik
            'highlightthickness': 2,
            'highlightbackground': self.current_theme.text_color
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
        
    def minimize_to_widget(self):
        """Minimize to widget mode"""
        if self.on_minimize:
            self.on_minimize()
    
    def update_normal(self):
        """Update normal mode display - NOVA JEDNOSTAVNA SPECIFIKACIJA"""
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
                        'utc': reading.utc
                    }
                except:
                    data = AstronomicalCalculator.calculate_time()
            else:
                data = AstronomicalCalculator.calculate_time()
            
            # 1. Dies broj (veliki font)
            self.dies_number_label.config(text=str(data['dies']))
            
            # 2. miliDies broj (veliki font, trocifreni)
            self.milides_number_label.config(text=f"{data['milides']:03d}")
            
            # 3. Progress bar za mikroDies i label ispod
            self.main_progress_var.set(data['mikrodiet'])
            self.mikro_label.config(text=f"mikroDies: {data['mikrodiet']:03d}")
            
            # 4. Standardno vreme - UTC+timezone DD/MM/YYYY hh:mm:ss
            utc_time = data['utc']
            
            # Pokušaj da izračunaš lokalnu timezone offset
            try:
                local_time = utc_time.replace(tzinfo=timezone.utc).astimezone()
                # Izračunaj offset u satima
                offset_seconds = local_time.utcoffset().total_seconds()
                offset_hours = int(offset_seconds / 3600)
                
                # Format timezone
                if offset_hours >= 0:
                    timezone_str = f"UTC+{offset_hours}"
                else:
                    timezone_str = f"UTC{offset_hours}"
                
                # Format datum i vreme
                date_str = local_time.strftime("%d/%m/%Y")
                time_str = local_time.strftime("%H:%M:%S")
                
                standard_time_text = f"{timezone_str}  {date_str}  {time_str}"
                
            except:
                # Fallback na UTC
                date_str = utc_time.strftime("%d/%m/%Y")
                time_str = utc_time.strftime("%H:%M:%S")
                standard_time_text = f"UTC+0  {date_str}  {time_str}"
            
            self.standard_time_label.config(text=standard_time_text)
            
        except Exception as e:
            # Error handling
            self.dies_number_label.config(text="ERR")
            self.milides_number_label.config(text="ERR")
            self.standard_time_label.config(text="ERROR")
            print(f"Normal mode update error: {e}")
        
        # Schedule next update
        self.parent.after(100, self.update_normal)
    
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