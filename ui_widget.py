#!/usr/bin/env python3
"""
Astronomical Watch - Funkcionalni UI Widget
Tkinter widget koji prikazuje astronomsko vreme sa gradijentom neba
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timezone, timedelta
import math
import threading
import time

def compute_simple_equinox(year: int) -> datetime:
    """Aproksimativno izračunavanje prolećne ravnodnevnice"""
    base_dates = {
        2023: datetime(2023, 3, 20, 21, 24, tzinfo=timezone.utc),
        2024: datetime(2024, 3, 20, 3, 6, tzinfo=timezone.utc),
        2025: datetime(2025, 3, 20, 9, 1, tzinfo=timezone.utc),
    }
    
    if year in base_dates:
        return base_dates[year]
    
    return datetime(year, 3, 20, 12, 0, tzinfo=timezone.utc)

def get_astronomical_time():
    """Vraća astronomsko vreme kao (day_index, mili_dies, milidi_fraction)"""
    now = datetime.now(timezone.utc)
    year = now.year
    
    current_equinox = compute_simple_equinox(year)
    
    if now < current_equinox:
        year -= 1
        current_equinox = compute_simple_equinox(year)
    
    elapsed = now - current_equinox
    total_seconds = elapsed.total_seconds()
    
    day_index = int(total_seconds // 86400)
    remainder_seconds = total_seconds % 86400
    mili_dies = int((remainder_seconds / 86400) * 1000)
    
    # Frakcija unutar trenutnog miliDies-a za progres bar
    milidi_seconds = remainder_seconds % 86.4  # 86.4 sekunde = 1 miliDies
    milidi_fraction = milidi_seconds / 86.4  # 0.0 - 1.0
    
    return day_index, mili_dies, milidi_fraction

def get_sky_color(hour_of_day):
    """Jednostavan algoritam za boju neba zavisno od sata"""
    # Mapiranje sata na boje neba
    if 5 <= hour_of_day <= 7:  # svitanje
        return "#FFB366"  # narandžasta
    elif 7 < hour_of_day <= 18:  # dan
        return "#87CEEB"  # plavo nebo
    elif 18 < hour_of_day <= 20:  # zalazak
        return "#FF6B6B"  # crvenkasto
    else:  # noć
        return "#1B1B2F"  # tamno plavo

class AstronomicalWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Astronomical Watch")
        self.root.geometry("300x150")
        
        # Glavni frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Naslov
        self.title_label = tk.Label(self.main_frame, 
                                   text="Astronomical Watch", 
                                   font=("Arial", 14, "bold"))
        self.title_label.pack(pady=5)
        
        # Astronomsko vreme
        self.time_label = tk.Label(self.main_frame, 
                                  text="000.000", 
                                  font=("Courier", 24, "bold"))
        self.time_label.pack(pady=10)
        
        # Format objašnjenje
        self.format_label = tk.Label(self.main_frame, 
                                    text="Dies.miliDies", 
                                    font=("Arial", 10))
        self.format_label.pack()
        
        # Progress bar za miliDies
        self.milidi_label = tk.Label(self.main_frame, text="Napredak miliDies-a:")
        self.milidi_label.pack(pady=(10,0))
        
        self.milidi_progress = ttk.Progressbar(self.main_frame, length=250)
        self.milidi_progress.pack(pady=5)
        
        # UTC vreme
        self.utc_label = tk.Label(self.main_frame, 
                                 text="", 
                                 font=("Arial", 9))
        self.utc_label.pack(pady=(10,0))
        
        self.running = True
        self.update_display()
        
        # Pokreni update thread
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
        # Zatvaranje
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def update_display(self):
        """Ažurira prikaz"""
        try:
            day_index, mili_dies, milidi_fraction = get_astronomical_time()
            now = datetime.now(timezone.utc)
            
            # Ažuriraj glavno vreme
            self.time_label.config(text=f"{day_index:03d}.{mili_dies:03d}")
            
            # Ažuriraj progres miliDies-a (0-100%)
            milidi_progress = milidi_fraction * 100
            self.milidi_progress['value'] = milidi_progress
            
            # Ažuriraj UTC vreme
            utc_str = now.strftime("%Y-%m-%d %H:%M:%S UTC")
            self.utc_label.config(text=utc_str)
            
            # Ažuriraj boju pozadine na osnovu sata
            hour = now.hour
            bg_color = get_sky_color(hour)
            self.main_frame.config(bg=bg_color)
            
            # Ažuriraj boju teksta za kontrast
            if hour >= 20 or hour <= 6:
                text_color = "white"
            else:
                text_color = "black"
                
            for widget in [self.title_label, self.time_label, self.format_label, 
                          self.milidi_label, self.utc_label]:
                widget.config(fg=text_color, bg=bg_color)
                
        except Exception as e:
            self.time_label.config(text=f"Greška: {e}")
    
    def update_loop(self):
        """Thread loop za ažuriranje"""
        while self.running:
            self.root.after(0, self.update_display)
            time.sleep(1)
    
    def on_closing(self):
        """Zatvaranje aplikacije"""
        self.running = False
        self.root.destroy()

def main():
    """Pokreni GUI"""
    root = tk.Tk()
    app = AstronomicalWidget(root)
    root.mainloop()

if __name__ == "__main__":
    main()