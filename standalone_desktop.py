# -*- coding: utf-8 -*-
"""
Astronomical Watch Desktop - Standalone verzija
Može biti kompajlovan u .exe sa PyInstaller
"""
import tkinter as tk
from tkinter import ttk
import sys
import os
from datetime import datetime, timezone, timedelta
import math

# Ako je pakovano sa PyInstaller
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Embedded astronomical calculations (minimalna verzija)
class SimpleAstroCalculator:
    """Jednostavan astronomical calculator za standalone app"""
    
    REFERENCE_MERIDIAN = -168.975  # 168°58'30"W
    DAY_BOUNDARY_OFFSET_HOURS = 23.2650  # 23:15:54 UTC
    
    # mikroDies konstante
    MIKRODIES_PER_MILIDES = 1000
    MIKRODIES_PER_DAY = 1_000_000
    SECONDS_PER_MIKRODIES = 0.0864
    
    def __init__(self):
        self.equinox_dates = {
            2023: datetime(2023, 3, 20, 21, 24, 20, tzinfo=timezone.utc),
            2024: datetime(2024, 3, 20, 3, 6, 28, tzinfo=timezone.utc), 
            2025: datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc),
            2026: datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc),
        }
        
    def get_current_equinox_year(self, dt: datetime) -> int:
        """Pronađi current equinox year"""
        year = dt.year
        current_eq = self.equinox_dates.get(year, self.equinox_dates[2025])
        
        if dt < current_eq:
            year -= 1
            
        return year
        
    def calculate_astro_reading(self, dt: datetime) -> dict:
        """Glavni calculation za astronomical reading"""
        # Pronađi equinox period
        year = self.get_current_equinox_year(dt)
        
        current_eq = self.equinox_dates.get(year, self.equinox_dates[2025])
        next_eq = self.equinox_dates.get(year + 1, self.equinox_dates[2025])
        
        # Day boundary calculation (mean solar noon at reference meridian)
        hours_offset = self.DAY_BOUNDARY_OFFSET_HOURS
        day_boundary_offset = timedelta(hours=hours_offset)
        
        # Sekunde od equinox-a
        seconds_since_equinox = (dt - current_eq).total_seconds()
        
        # Calculate raw days
        raw_days = seconds_since_equinox / 86400.0
        
        # Apply day boundary offset
        adjusted_days = raw_days + (day_boundary_offset.total_seconds() / 86400.0)
        
        # Extract components
        day_index = int(adjusted_days)
        day_fraction = adjusted_days - day_index
        
        # miliDies calculation
        total_milides = day_fraction * 1000.0
        milides = int(total_milides)
        milides_fraction = total_milides - milides
        
        # mikroDies calculation  
        total_mikrodiet = milides_fraction * self.MIKRODIES_PER_MILIDES
        mikrodiet = int(total_mikrodiet)
        mikrodiet_fraction = total_mikrodiet - mikrodiet
        
        return {
            'day_index': max(0, day_index),
            'miliDies': milides,
            'mikroDies': mikrodiet,
            'mikroDies_fraction': mikrodiet_fraction,
            'equinox_year': year
        }

class AstronomicalWatchStandalone:
    """Standalone desktop aplikacija"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Astronomical Watch mikroDies - Standalone")
        self.root.geometry("340x200")
        self.root.resizable(False, False)
        
        # Always on top
        try:
            self.root.attributes('-topmost', True)
        except:
            pass
            
        # Calculator
        self.calculator = SimpleAstroCalculator()
        
        # Setup UI
        self.setup_styles()
        self.create_widgets()
        
        # Start updates
        self.update_display()
        
    def setup_styles(self):
        """UI stilovi"""
        self.root.configure(bg='#0a0a1a')
        
        self.bg_color = '#0a0a1a'
        self.primary_color = '#1a1a3a' 
        self.accent_color = '#2a2a5a'
        self.text_color = '#ffffff'
        self.highlight_color = '#ffaa00'
        
    def create_widgets(self):
        """Kreiranje UI komponenata"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(header_frame,
                              text="🌟 Astronomical Watch",
                              font=("Segoe UI", 14, "bold"),
                              bg=self.bg_color,
                              fg=self.highlight_color)
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame,
                                 text="mikroDies Precision",
                                 font=("Segoe UI", 10),
                                 bg=self.bg_color,
                                 fg='#cccccc')
        subtitle_label.pack()
        
        # Time display
        time_frame = tk.Frame(main_frame, bg=self.primary_color, relief='raised', bd=3)
        time_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.time_display = tk.Label(time_frame,
                                    text="000.000.000",
                                    font=("Courier New", 20, "bold"),
                                    bg=self.primary_color,
                                    fg=self.text_color)
        self.time_display.pack(pady=10)
        
        # Format label
        format_label = tk.Label(time_frame,
                               text="Dies . miliDies . mikroDies",
                               font=("Segoe UI", 9),
                               bg=self.primary_color,
                               fg='#aaaaaa')
        format_label.pack(pady=(0, 8))
        
        # Info panel
        info_frame = tk.Frame(main_frame, bg=self.accent_color, relief='sunken', bd=2)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # UTC display
        self.utc_display = tk.Label(info_frame,
                                   text="UTC: --:--:--",
                                   font=("Segoe UI", 10),
                                   bg=self.accent_color,
                                   fg=self.text_color)
        self.utc_display.pack(pady=5)
        
        # Details grid
        details_frame = tk.Frame(main_frame, bg=self.bg_color)
        details_frame.pack(fill=tk.X)
        
        # Left column
        left_frame = tk.Frame(details_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.dies_display = tk.Label(left_frame,
                                    text="Dies: ---",
                                    font=("Segoe UI", 9),
                                    bg=self.bg_color,
                                    fg=self.text_color)
        self.dies_display.pack(anchor='w')
        
        self.year_display = tk.Label(left_frame,
                                    text="Godina: ----",
                                    font=("Segoe UI", 9), 
                                    bg=self.bg_color,
                                    fg='#aaaaaa')
        self.year_display.pack(anchor='w')
        
        # Right column
        right_frame = tk.Frame(details_frame, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.precision_display = tk.Label(right_frame,
                                         text="Frakc: 0.000",
                                         font=("Segoe UI", 9),
                                         bg=self.bg_color,
                                         fg=self.text_color)
        self.precision_display.pack(anchor='e')
        
        self.status_display = tk.Label(right_frame,
                                      text="Status: OK",
                                      font=("Segoe UI", 9),
                                      bg=self.bg_color,
                                      fg='#00ff00')
        self.status_display.pack(anchor='e')
        
    def update_display(self):
        """Ažuriranje prikaza"""
        try:
            now = datetime.now(timezone.utc)
            reading = self.calculator.calculate_astro_reading(now)
            
            # Format glavni prikaz
            main_time = f"{reading['day_index']:03d}.{reading['miliDies']:03d}.{reading['mikroDies']:03d}"
            self.time_display.config(text=main_time)
            
            # UTC vreme
            self.utc_display.config(text=f"UTC: {now.strftime('%H:%M:%S')}")
            
            # Detalji
            self.dies_display.config(text=f"Dies: {reading['day_index']}")
            self.year_display.config(text=f"Godina: {reading['equinox_year']}-{reading['equinox_year']+1}")
            self.precision_display.config(text=f"Frakc: {reading['mikroDies_fraction']:.3f}")
            self.status_display.config(text="Status: OK", fg='#00ff00')
            
        except Exception as e:
            self.time_display.config(text="ERROR")
            self.status_display.config(text=f"Greška: {str(e)[:20]}", fg='#ff0000')
            
        # Sledeće ažuriranje
        self.root.after(100, self.update_display)
        
    def run(self):
        """Pokretanje aplikacije"""
        print("🚀 Astronomical Watch Standalone - Pokretanje...")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\n👋 Aplikacija zatvorena")

def main():
    """Glavna funkcija"""
    print("=== ASTRONOMICAL WATCH STANDALONE ===")
    print("mikroDies preciznost | Standalone Desktop")
    print()
    
    app = AstronomicalWatchStandalone()
    app.run()

if __name__ == "__main__":
    main()