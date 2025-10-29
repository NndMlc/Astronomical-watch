#!/usr/bin/env python3
"""
Astronomical Watch Desktop Application
Kompaktni desktop widget sa mikroDies preciznosću
"""
import tkinter as tk
from tkinter import ttk
import sys
import os
from datetime import datetime, timezone, timedelta
import math

# Dodaj src direktorijum u path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from astronomical_watch.core.astro_time_core import AstroYear

class AstronomicalWatchDesktop:
    """Desktop widget aplikacija sa mikroDies preciznosću"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Astronomical Watch - mikroDies")
        self.root.geometry("320x180")
        self.root.resizable(False, False)
        
        # Pokušaj da postaviš window da bude "always on top"
        try:
            self.root.attributes('-topmost', True)
        except:
            pass
            
        # Style konfiguacija
        self.setup_styles()
        
        # Kreiranje UI elemenata
        self.create_widgets()
        
        # Inicijalizacija AstroYear objekta
        self.astro_year = None
        self.init_astro_year()
        
        # Start auto-update
        self.update_display()
        
    def setup_styles(self):
        """Postavlja stilove za UI"""
        self.root.configure(bg='#1a1a2e')
        
        # Boje
        self.bg_color = '#1a1a2e'
        self.primary_color = '#16213e'
        self.accent_color = '#0f3460'
        self.text_color = '#e94560'
        self.secondary_text = '#f5f5f5'
        
    def create_widgets(self):
        """Kreira UI komponente"""
        # Glavni container
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Naslov
        title_label = tk.Label(main_frame, 
                              text="🌟 Astronomical Watch mikroDies", 
                              font=("Segoe UI", 12, "bold"),
                              bg=self.bg_color, 
                              fg=self.text_color)
        title_label.pack(pady=(0, 10))
        
        # Vreme prikaz frame
        time_frame = tk.Frame(main_frame, bg=self.primary_color, relief='raised', bd=2)
        time_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Astronomical time prikaz (DDD.mmm.µµµ)
        self.astro_time_label = tk.Label(time_frame, 
                                        text="000.000.000", 
                                        font=("Courier New", 18, "bold"),
                                        bg=self.primary_color, 
                                        fg=self.secondary_text)
        self.astro_time_label.pack(pady=8)
        
        # Format opis
        format_label = tk.Label(time_frame, 
                               text="Dies.miliDies.mikroDies", 
                               font=("Segoe UI", 9),
                               bg=self.primary_color, 
                               fg='#cccccc')
        format_label.pack(pady=(0, 5))
        
        # Info panel
        info_frame = tk.Frame(main_frame, bg=self.accent_color, relief='sunken', bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # UTC vreme
        self.utc_label = tk.Label(info_frame, 
                                 text="UTC: --", 
                                 font=("Segoe UI", 9),
                                 bg=self.accent_color, 
                                 fg=self.secondary_text)
        self.utc_label.pack(pady=2)
        
        # Progress bar za miliDies
        progress_frame = tk.Frame(info_frame, bg=self.accent_color)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(progress_frame, 
                text="miliDies napredak:", 
                font=("Segoe UI", 8),
                bg=self.accent_color, 
                fg='#cccccc').pack(anchor='w')
                
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                          variable=self.progress_var,
                                          maximum=100.0,
                                          length=280)
        self.progress_bar.pack(fill=tk.X, pady=2)
        
        # Detalji
        details_frame = tk.Frame(main_frame, bg=self.bg_color)
        details_frame.pack(fill=tk.X)
        
        # Leva kolona
        left_col = tk.Frame(details_frame, bg=self.bg_color)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.dies_label = tk.Label(left_col, 
                                  text="Dies: --", 
                                  font=("Segoe UI", 9),
                                  bg=self.bg_color, 
                                  fg=self.secondary_text)
        self.dies_label.pack(anchor='w')
        
        self.milidies_label = tk.Label(left_col, 
                                      text="miliDies: --", 
                                      font=("Segoe UI", 9),
                                      bg=self.bg_color, 
                                      fg=self.secondary_text)
        self.milidies_label.pack(anchor='w')
        
        # Desna kolona  
        right_col = tk.Frame(details_frame, bg=self.bg_color)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.mikrodiet_label = tk.Label(right_col, 
                                       text="mikroDies: --", 
                                       font=("Segoe UI", 9),
                                       bg=self.bg_color, 
                                       fg=self.secondary_text)
        self.mikrodiet_label.pack(anchor='e')
        
        self.precision_label = tk.Label(right_col, 
                                       text="Preciznost: --", 
                                       font=("Segoe UI", 9),
                                       bg=self.bg_color, 
                                       fg=self.secondary_text)
        self.precision_label.pack(anchor='e')
        
    def compute_simple_equinox(self, year: int) -> datetime:
        """Jednostavno izračunavanje equinox-a"""
        base_dates = {
            2023: datetime(2023, 3, 20, 21, 24, 20, tzinfo=timezone.utc),
            2024: datetime(2024, 3, 20, 3, 6, 28, tzinfo=timezone.utc),
            2025: datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc),
            2026: datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc),
        }
        return base_dates.get(year, base_dates[2025])
        
    def init_astro_year(self):
        """Inicijalizuje AstroYear objekat"""
        try:
            now = datetime.now(timezone.utc)
            year = now.year
            
            # Proveri da li je pre ili posle equinox-a
            current_eq = self.compute_simple_equinox(year)
            if now < current_eq:
                year -= 1
                current_eq = self.compute_simple_equinox(year)
                
            next_eq = self.compute_simple_equinox(year + 1)
            
            self.astro_year = AstroYear(current_eq, next_eq)
            print(f"✓ AstroYear inicijalizovan za {year}-{year+1}")
            
        except Exception as e:
            print(f"Greška pri inicijalizaciji AstroYear: {e}")
            
    def update_display(self):
        """Ažurira prikaz sa trenutnim podacima"""
        try:
            if self.astro_year:
                now = datetime.now(timezone.utc)
                reading = self.astro_year.reading(now)
                
                # Glavni prikaz (DDD.mmm.µµµ)
                self.astro_time_label.config(text=reading.timestamp_full())
                
                # UTC vreme
                self.utc_label.config(text=f"UTC: {now.strftime('%H:%M:%S')}")
                
                # Detalji
                self.dies_label.config(text=f"Dies: {reading.day_index}")
                self.milidies_label.config(text=f"miliDies: {reading.miliDies}")
                self.mikrodiet_label.config(text=f"mikroDies: {reading.mikroDies}")
                self.precision_label.config(text=f"Preciznost: {reading.mikroDies_fraction:.3f}")
                
                # Progress bar (trenutni miliDies kao procenat)
                # 0 mikroDies = 0%, 1000 mikroDies = 100% (jedan miliDies)
                progress_percent = (reading.mikroDies + reading.mikroDies_fraction) / 10.0  # 0-100%
                self.progress_var.set(progress_percent)
                
        except Exception as e:
            print(f"Greška pri ažuriranju prikaza: {e}")
            self.astro_time_label.config(text="ERROR")
            
        # Zakaži sledeće ažuriranje (svaki 100ms za smooth mikroDies)
        self.root.after(100, self.update_display)
        
    def run(self):
        """Pokreće desktop aplikaciju"""
        print("🚀 Pokretam Astronomical Watch Desktop sa mikroDies...")
        print("Pritisnite Ctrl+C za izlaz")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\n👋 Desktop aplikacija zatvorena")

def main():
    """Glavna funkcija"""
    print("=== ASTRONOMICAL WATCH DESKTOP ===")
    print("mikroDies preciznost | Desktop widget")
    print()
    
    app = AstronomicalWatchDesktop()
    app.run()

if __name__ == "__main__":
    main()