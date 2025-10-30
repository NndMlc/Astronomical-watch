# -*- coding: utf-8 -*-
"""
Windows Compatible Astronomical Watch
NO UNICODE CHARACTERS - maksimalna Windows kompatibilnost
"""
import tkinter as tk
from datetime import datetime, timezone, timedelta

class WindowsAstronomicalWatch:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Astronomical Watch Desktop")
        self.root.geometry("320x200")
        self.root.resizable(False, False)
        
        # Windows always on top
        try:
            self.root.attributes('-topmost', True)
        except:
            pass
        
        # Colors (Windows friendly)
        self.bg_color = '#1e1e2e'
        self.card_color = '#313244'
        self.text_color = '#ffffff'
        self.accent_color = '#89b4fa'
        
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
        self.start_updates()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        
        title_label = tk.Label(header_frame,
                              text="ASTRONOMICAL WATCH",
                              font=("Arial", 14, "bold"),
                              bg=self.bg_color,
                              fg=self.accent_color)
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame,
                                 text="mikroDies Precision Desktop",
                                 font=("Arial", 10),
                                 bg=self.bg_color,
                                 fg=self.text_color)
        subtitle_label.pack()
        
        # Main time display
        time_frame = tk.Frame(self.root, bg=self.card_color, relief='raised', bd=2)
        time_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.time_display = tk.Label(time_frame,
                                    text="000.000.000",
                                    font=("Courier New", 18, "bold"),
                                    bg=self.card_color,
                                    fg=self.text_color)
        self.time_display.pack(pady=8)
        
        format_desc = tk.Label(time_frame,
                              text="Dies . miliDies . mikroDies",
                              font=("Arial", 9),
                              bg=self.card_color,
                              fg='#aaaaaa')
        format_desc.pack(pady=(0, 5))
        
        # Info section
        info_frame = tk.Frame(self.root, bg=self.card_color, relief='sunken', bd=1)
        info_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.utc_display = tk.Label(info_frame,
                                   text="UTC: --:--:--",
                                   font=("Arial", 10),
                                   bg=self.card_color,
                                   fg=self.text_color)
        self.utc_display.pack(pady=5)
        
        # Details
        details_frame = tk.Frame(self.root, bg=self.bg_color)
        details_frame.pack(fill=tk.X, padx=15)
        
        # Left side
        left_details = tk.Frame(details_frame, bg=self.bg_color)
        left_details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.dies_display = tk.Label(left_details,
                                    text="Dies: ---",
                                    font=("Arial", 9),
                                    bg=self.bg_color,
                                    fg=self.text_color)
        self.dies_display.pack(anchor='w')
        
        self.year_display = tk.Label(left_details,
                                    text="Period: ----",
                                    font=("Arial", 9),
                                    bg=self.bg_color,
                                    fg='#aaaaaa')
        self.year_display.pack(anchor='w')
        
        # Right side
        right_details = tk.Frame(details_frame, bg=self.bg_color)
        right_details.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.mikro_display = tk.Label(right_details,
                                     text="mikroDies: ---",
                                     font=("Arial", 9),
                                     bg=self.bg_color,
                                     fg=self.text_color)
        self.mikro_display.pack(anchor='e')
        
        self.status_display = tk.Label(right_details,
                                      text="Status: Starting...",
                                      font=("Arial", 9),
                                      bg=self.bg_color,
                                      fg='#00ff00')
        self.status_display.pack(anchor='e')
        
    def calculate_astronomical_time(self, dt):
        # Equinox 2025 (astronomical year reference)
        equinox_2025 = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
        equinox_2026 = datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
        
        # Determine period
        if dt >= equinox_2025:
            current_eq = equinox_2025
            year_period = "2025-26"
        else:
            current_eq = datetime(2024, 3, 20, 3, 6, 28, tzinfo=timezone.utc)
            year_period = "2024-25"
        
        # Calculate seconds since equinox
        seconds_since = (dt - current_eq).total_seconds()
        
        # Day boundary (mean solar noon at reference meridian = 23:15:54 UTC)
        boundary_hours = 23.2650
        boundary_offset = timedelta(hours=boundary_hours)
        
        # Convert to days with boundary adjustment
        raw_days = seconds_since / 86400.0
        adjusted_days = raw_days + (boundary_offset.total_seconds() / 86400.0)
        
        # Extract components
        day_index = max(0, int(adjusted_days))
        day_fraction = adjusted_days - day_index
        
        # miliDies calculation
        total_milides = day_fraction * 1000.0
        milides = int(total_milides)
        milides_fraction = total_milides - milides
        
        # mikroDies calculation
        mikrodiet = int(milides_fraction * 1000.0)
        mikrodiet_fraction = (milides_fraction * 1000.0) - mikrodiet
        
        return {
            'day_index': day_index,
            'miliDies': milides,
            'mikroDies': mikrodiet,
            'fraction': mikrodiet_fraction,
            'period': year_period
        }
        
    def update_time_display(self):
        try:
            now = datetime.now(timezone.utc)
            astro_data = self.calculate_astronomical_time(now)
            
            # Main display format
            time_text = "{:03d}.{:03d}.{:03d}".format(
                astro_data['day_index'],
                astro_data['miliDies'],
                astro_data['mikroDies']
            )
            self.time_display.config(text=time_text)
            
            # UTC display
            utc_text = "UTC: " + now.strftime('%H:%M:%S')
            self.utc_display.config(text=utc_text)
            
            # Details
            dies_text = "Dies: {}".format(astro_data['day_index'])
            self.dies_display.config(text=dies_text)
            
            period_text = "Period: {}".format(astro_data['period'])
            self.year_display.config(text=period_text)
            
            mikro_text = "mikroDies: {}".format(astro_data['mikroDies'])
            self.mikro_display.config(text=mikro_text)
            
            self.status_display.config(text="Status: Running", fg='#00ff00')
            
        except Exception as e:
            self.time_display.config(text="ERROR")
            error_text = "Error: " + str(e)[:20]
            self.status_display.config(text=error_text, fg='#ff0000')
            
        # Schedule next update (100ms for smooth mikroDies)
        self.root.after(100, self.update_time_display)
        
    def start_updates(self):
        print("Astronomical Watch Windows - Starting...")
        print("Format: DDD.mmm.uuu (Dies.miliDies.mikroDies)")
        print("Real-time mikroDies precision display")
        print("Press Alt+F4 to close")
        self.update_time_display()
        
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Application closed")

def main():
    print("=== ASTRONOMICAL WATCH WINDOWS ===")
    print("mikroDies Precision Desktop Widget")
    print("Windows Compatible Version (No Unicode)")
    print("")
    
    app = WindowsAstronomicalWatch()
    app.run()

if __name__ == "__main__":
    main()