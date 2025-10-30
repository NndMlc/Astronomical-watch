# -*- coding: utf-8 -*-
"""
Astronomical Watch - ULTIMATE WINDOWS VERSION
Combines best of all versions - GUARANTEED TO WORK
"""
import time
import os
import sys
from datetime import datetime, timezone, timedelta

# Try to import tkinter, fallback to console if not available
try:
    import tkinter as tk
    from tkinter import ttk
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

class AstronomicalCalculator:
    """Core astronomical calculations"""
    
    @staticmethod
    def calculate_time():
        """Calculate current astronomical time"""
        now = datetime.now(timezone.utc)
        
        # Equinox 2025 reference
        equinox = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
        
        # Time since equinox
        delta_seconds = (now - equinox).total_seconds()
        
        # Day boundary adjustment (23:15:54 UTC)
        boundary_offset = 23*3600 + 15*60 + 54
        adjusted_seconds = delta_seconds + boundary_offset
        
        # Convert to astronomical components
        total_days = adjusted_seconds / 86400.0
        dies = max(0, int(total_days))
        day_fraction = total_days - dies
        
        # miliDies calculation
        milides_total = day_fraction * 1000.0
        milides = int(milides_total)
        milides_fraction = milides_total - milides
        
        # mikroDies calculation
        mikrodiet = int(milides_fraction * 1000.0)
        mikrodiet_fraction = (milides_fraction * 1000.0) - mikrodiet
        
        return {
            'utc': now,
            'dies': dies,
            'milides': milides,
            'mikrodiet': mikrodiet,
            'fraction': mikrodiet_fraction
        }
    
    @staticmethod
    def format_time(data):
        """Format as DDD.mmm.uuu"""
        return "{:03d}.{:03d}.{:03d}".format(
            data['dies'], data['milides'], data['mikrodiet']
        )

class ConsoleDisplay:
    """Console version display"""
    
    def __init__(self):
        self.calc = AstronomicalCalculator()
        
    def clear_screen(self):
        """Clear console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def progress_bar(self, value, max_val, width=30):
        """Create ASCII progress bar"""
        progress = min(value / max_val, 1.0)
        filled = int(progress * width)
        bar = "█" * filled + "░" * (width - filled)
        percentage = progress * 100
        return f"[{bar}] {percentage:.1f}%"
    
    def run(self):
        """Run console display"""
        print("Astronomical Watch Console - Starting...")
        print("Press Ctrl+C to exit")
        print()
        
        try:
            while True:
                data = self.calc.calculate_time()
                
                self.clear_screen()
                
                print("=" * 60)
                print("        ASTRONOMICAL WATCH - CONSOLE")
                print("        mikroDies Precision Display")
                print("=" * 60)
                print()
                
                # Main time
                time_str = self.calc.format_time(data)
                print(f"    TIME: {time_str}")
                print("    Dies . miliDies . mikroDies")
                print()
                
                # Details
                utc_str = data['utc'].strftime('%Y-%m-%d %H:%M:%S UTC')
                print(f"    UTC:       {utc_str}")
                print(f"    Dies:      {data['dies']}")
                print(f"    miliDies:  {data['milides']}")
                print(f"    mikroDies: {data['mikrodiet']}")
                print(f"    Precision: {data['fraction']:.6f}")
                print()
                
                # Progress bars
                mili_prog = self.progress_bar(data['milides'], 999, 25)
                mikro_prog = self.progress_bar(data['mikrodiet'], 999, 25)
                
                print("    PROGRESS:")
                print(f"    miliDies  {mili_prog}")
                print(f"    mikroDies {mikro_prog}")
                print()
                print("    Press Ctrl+C to exit | Updates every 1s")
                print("=" * 60)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.clear_screen()
            print("Astronomical Watch Console stopped!")

class GUIDisplay:
    """GUI version display (if tkinter available)"""
    
    def __init__(self):
        self.calc = AstronomicalCalculator()
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Setup main window"""
        self.root.title("Astronomical Watch - mikroDies")
        self.root.geometry("350x220")
        self.root.resizable(False, False)
        
        # Always on top
        try:
            self.root.attributes('-topmost', True)
        except:
            pass
        
        # Colors
        self.bg_color = '#1e1e2e'
        self.card_color = '#313244'
        self.text_color = '#ffffff'
        self.accent_color = '#89b4fa'
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Create UI widgets"""
        # Header
        header = tk.Frame(self.root, bg=self.bg_color)
        header.pack(fill=tk.X, padx=15, pady=10)
        
        title = tk.Label(header,
                        text="ASTRONOMICAL WATCH",
                        font=("Arial", 14, "bold"),
                        bg=self.bg_color,
                        fg=self.accent_color)
        title.pack()
        
        subtitle = tk.Label(header,
                           text="mikroDies Precision Desktop",
                           font=("Arial", 10),
                           bg=self.bg_color,
                           fg=self.text_color)
        subtitle.pack()
        
        # Time display
        time_frame = tk.Frame(self.root, bg=self.card_color, relief='raised', bd=2)
        time_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.time_label = tk.Label(time_frame,
                                  text="000.000.000",
                                  font=("Courier New", 18, "bold"),
                                  bg=self.card_color,
                                  fg=self.text_color)
        self.time_label.pack(pady=8)
        
        format_label = tk.Label(time_frame,
                               text="Dies . miliDies . mikroDies",
                               font=("Arial", 9),
                               bg=self.card_color,
                               fg='#aaaaaa')
        format_label.pack(pady=(0, 5))
        
        # Info section
        info_frame = tk.Frame(self.root, bg=self.card_color, relief='sunken', bd=1)
        info_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.utc_label = tk.Label(info_frame,
                                 text="UTC: --:--:--",
                                 font=("Arial", 10),
                                 bg=self.card_color,
                                 fg=self.text_color)
        self.utc_label.pack(pady=5)
        
        # Details
        details_frame = tk.Frame(self.root, bg=self.bg_color)
        details_frame.pack(fill=tk.X, padx=15)
        
        self.details_label = tk.Label(details_frame,
                                     text="Dies: --- | mikroDies: --- | Status: Loading...",
                                     font=("Arial", 9),
                                     bg=self.bg_color,
                                     fg=self.text_color)
        self.details_label.pack()
    
    def update_display(self):
        """Update GUI display"""
        try:
            data = self.calc.calculate_time()
            
            # Main time
            time_str = self.calc.format_time(data)
            self.time_label.config(text=time_str)
            
            # UTC time
            utc_str = data['utc'].strftime('%H:%M:%S UTC')
            self.utc_label.config(text=f"UTC: {utc_str}")
            
            # Details
            details_str = f"Dies: {data['dies']} | mikroDies: {data['mikrodiet']} | Status: Running"
            self.details_label.config(text=details_str)
            
        except Exception as e:
            self.time_label.config(text="ERROR")
            self.details_label.config(text=f"Error: {str(e)[:30]}")
        
        # Schedule next update
        self.root.after(100, self.update_display)
    
    def run(self):
        """Run GUI application"""
        print("Astronomical Watch GUI - Starting...")
        print("Close window to exit")
        
        self.update_display()
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("GUI application closed")

def main():
    """Main function - auto-detect best version"""
    print("=== ASTRONOMICAL WATCH ULTIMATE ===")
    print("Windows Compatible | Auto-Detection")
    print()
    
    if HAS_TKINTER:
        try:
            print("tkinter detected - launching GUI version...")
            app = GUIDisplay()
            app.run()
        except Exception as e:
            print(f"GUI failed: {e}")
            print("Falling back to console version...")
            app = ConsoleDisplay()
            app.run()
    else:
        print("tkinter not available - launching console version...")
        app = ConsoleDisplay()
        app.run()

if __name__ == "__main__":
    main()