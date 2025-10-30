# -*- coding: utf-8 -*-
"""
Astronomical Watch Desktop - Windows Optimized
Jednostavna verzija za Windows sa embedded kalkulacijama
Kopiraj ovaj kod u .py fajl na Windows-u i pokreni sa: python filename.py
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timezone, timedelta
import math

class WindowsAstronomicalWatch:
    """Windows optimizovana verzija Astronomical Watch"""
    
    def __init__(self):
        # Kreiranje glavnog window-a
        self.root = tk.Tk()
        self.root.title("Astronomical Watch - mikroDies")
        self.root.geometry("350x220")
        self.root.resizable(False, False)
        
        # Always on top za Windows
        self.root.attributes('-topmost', True)
        
        # Windows-friendly colors
        self.bg_color = '#1e1e2e'
        self.card_color = '#313244'
        self.accent_color = '#89b4fa'
        self.text_color = '#cdd6f4'
        self.highlight_color = '#f9e2af'
        
        self.root.configure(bg=self.bg_color)
        
        self.create_ui()
        self.start_updates()
        
    def create_ui(self):
        """Kreiranje UI komponenata optimizovano za Windows"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        
        title = tk.Label(header_frame, 
                        text="Astronomical Watch",
                        font=("Segoe UI", 14, "bold"),
                        bg=self.bg_color, 
                        fg=self.highlight_color)
        title.pack()
        
        subtitle = tk.Label(header_frame,
                           text="mikroDies Precision Timekeeping",
                           font=("Segoe UI", 9),
                           bg=self.bg_color,
                           fg=self.text_color)
        subtitle.pack()
        
        # Main time display card
        time_card = tk.Frame(self.root, bg=self.card_color, relief='raised', bd=2)
        time_card.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.time_label = tk.Label(time_card,
                                  text="000.000.000",
                                  font=("Consolas", 18, "bold"),  # Windows monospace font
                                  bg=self.card_color,
                                  fg=self.accent_color)
        self.time_label.pack(pady=8)
        
        format_desc = tk.Label(time_card,
                              text="Dies . miliDies . mikroDies",
                              font=("Segoe UI", 9),
                              bg=self.card_color,
                              fg='#a6adc8')
        format_desc.pack(pady=(0, 5))
        
        # Info panel
        info_card = tk.Frame(self.root, bg=self.card_color, relief='sunken', bd=1)
        info_card.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.utc_label = tk.Label(info_card,
                                 text="UTC: --:--:--",
                                 font=("Segoe UI", 10),
                                 bg=self.card_color,
                                 fg=self.text_color)
        self.utc_label.pack(pady=3)
        
        # Progress section
        progress_frame = tk.Frame(info_card, bg=self.card_color)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(progress_frame,
                text="miliDies Progress:",
                font=("Segoe UI", 8),
                bg=self.card_color,
                fg='#a6adc8').pack(anchor='w')
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame,
                                          variable=self.progress_var,
                                          maximum=100,
                                          length=300)
        self.progress_bar.pack(fill=tk.X, pady=2)
        
        # Details grid
        details_frame = tk.Frame(self.root, bg=self.bg_color)
        details_frame.pack(fill=tk.X, padx=15)
        
        # Left column
        left_col = tk.Frame(details_frame, bg=self.bg_color)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.dies_label = tk.Label(left_col,
                                  text="Dies: ---",
                                  font=("Segoe UI", 9),
                                  bg=self.bg_color,
                                  fg=self.text_color)
        self.dies_label.pack(anchor='w')
        
        self.year_label = tk.Label(left_col,
                                  text="Period: ----",
                                  font=("Segoe UI", 9),
                                  bg=self.bg_color,
                                  fg='#a6adc8')
        self.year_label.pack(anchor='w')
        
        # Right column
        right_col = tk.Frame(details_frame, bg=self.bg_color)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.mikro_label = tk.Label(right_col,
                                   text="mikroDies: ---",
                                   font=("Segoe UI", 9),
                                   bg=self.bg_color,
                                   fg=self.text_color)
        self.mikro_label.pack(anchor='e')
        
        self.precision_label = tk.Label(right_col,
                                       text="Precision: 0.000",
                                       font=("Segoe UI", 9),
                                       bg=self.bg_color,
                                       fg='#a6adc8')
        self.precision_label.pack(anchor='e')
        
    def calculate_astro_time(self, dt):
        """Embedded astronomical calculation"""
        # Equinox dates (simplified)
        equinox_2025 = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
        equinox_2026 = datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
        
        # Determine which equinox period we're in
        if dt >= equinox_2025:
            current_eq = equinox_2025
            next_eq = equinox_2026
            year_label = "2025-26"
        else:
            # Before 2025 equinox (use 2024 as approximate)
            current_eq = datetime(2024, 3, 20, 3, 6, 28, tzinfo=timezone.utc)
            next_eq = equinox_2025  
            year_label = "2024-25"
        
        # Day boundary offset (mean solar noon at reference meridian)
        day_boundary_hours = 23.2650  # 23:15:54 UTC
        day_boundary_offset = timedelta(hours=day_boundary_hours)
        
        # Calculate seconds since equinox
        seconds_since_eq = (dt - current_eq).total_seconds()
        
        # Convert to days with boundary offset
        raw_days = seconds_since_eq / 86400.0
        adjusted_days = raw_days + (day_boundary_offset.total_seconds() / 86400.0)
        
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
            'mikroDies_fraction': mikrodiet_fraction,
            'year_label': year_label
        }
        
    def update_display(self):
        """Update display with current time"""
        try:
            now = datetime.now(timezone.utc)
            astro_data = self.calculate_astro_time(now)
            
            # Main time display
            time_str = f"{astro_data['day_index']:03d}.{astro_data['miliDies']:03d}.{astro_data['mikroDies']:03d}"
            self.time_label.config(text=time_str)
            
            # UTC time
            self.utc_label.config(text=f"UTC: {now.strftime('%H:%M:%S')}")
            
            # Details
            self.dies_label.config(text=f"Dies: {astro_data['day_index']}")
            self.year_label.config(text=f"Period: {astro_data['year_label']}")
            self.mikro_label.config(text=f"mikroDies: {astro_data['mikroDies']}")
            self.precision_label.config(text=f"Precision: {astro_data['mikroDies_fraction']:.3f}")
            
            # Progress bar (mikroDies progress within current miliDies)
            progress = (astro_data['mikroDies'] + astro_data['mikroDies_fraction']) / 10.0
            self.progress_var.set(progress)
            
        except Exception as e:
            self.time_label.config(text="ERROR")
            print(f"Error: {e}")
            
        # Schedule next update (every 100ms for smooth animation)
        self.root.after(100, self.update_display)
        
    def start_updates(self):
        """Start the update loop"""
        print("Astronomical Watch Windows - Starting...")
        print("Real-time mikroDies precision display")
        print("Press Alt+F4 to close")
        self.update_display()
        
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\nApplication closed")

def main():
    """Main function"""
    print("=== ASTRONOMICAL WATCH WINDOWS ===")
    print("mikroDies Precision Desktop Widget")
    print("Compatible with Windows 10/11")
    print()
    
    # Check if running on Windows
    import platform
    if platform.system() == "Windows":
        print("Windows detected - optimized display enabled")
    else:
        print("Non-Windows system - basic compatibility mode")
    
    app = WindowsAstronomicalWatch()
    app.run()

if __name__ == "__main__":
    main()