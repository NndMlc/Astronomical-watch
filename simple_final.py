#!/usr/bin/env python3
"""
FINAL SIMPLE Astronomical Watch
Maksimalno jednostavna implementacija:
- Widget mode: mali ugao
- Normal mode: veliki centralni
- Garantovana vidljivost
"""

import tkinter as tk
from datetime import datetime, timezone
import sys
import os

# Core library check
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
try:
    from astronomical_watch.core.astro_time_core import AstroYear
    HAS_CORE = True
except:
    HAS_CORE = False

def get_time_data():
    """Get astronomical time"""
    if HAS_CORE:
        try:
            eq1 = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
            eq2 = datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
            ay = AstroYear(eq1, eq2)
            reading = ay.reading(datetime.now(timezone.utc))
            return {
                'dies': reading.day_index,
                'milides': reading.miliDies,
                'mikrodiet': reading.mikroDies,
                'utc': datetime.now(timezone.utc)
            }
        except:
            pass
    
    # Fallback
    now = datetime.now(timezone.utc)
    equinox = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
    delta = now - equinox
    dies = max(0, delta.days)
    seconds_today = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    milides = int((seconds_today / 86400) * 1000)
    mikrodiet = int(((seconds_today % 86.4) / 86.4) * 1000)
    return {'dies': dies, 'milides': milides, 'mikrodiet': mikrodiet, 'utc': now}

class SimpleAstroWatch:
    def __init__(self):
        self.root = tk.Tk()
        self.is_widget = True
        self.create_widget()
        self.update_time()
    
    def create_widget(self):
        """Create widget mode"""
        self.root.title("AW")
        self.root.geometry("160x80")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # Corner position
        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"+{sw-180}+20")
        self.root.configure(bg="#003366")
        
        # Clear widgets
        for w in self.root.winfo_children():
            w.destroy()
        
        # Frame
        f = tk.Frame(self.root, bg="#003366")
        f.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Time
        self.time_lbl = tk.Label(f, text="000.000", font=("Courier", 16, "bold"), bg="#003366", fg="white")
        self.time_lbl.pack(pady=5)
        
        # Date
        self.date_lbl = tk.Label(f, text="00/00", font=("Arial", 8), bg="#003366", fg="white")
        self.date_lbl.pack()
        
        # Bind clicks
        for widget in [self.root, f, self.time_lbl, self.date_lbl]:
            widget.bind("<Double-Button-1>", lambda e: self.switch_normal())
        
        self.is_widget = True
    
    def create_normal(self):
        """Create normal mode"""
        self.root.title("Astronomical Watch")
        self.root.geometry("600x500")
        self.root.overrideredirect(False)
        
        # Center
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"+{(sw//2)-300}+{(sh//2)-250}")
        self.root.configure(bg="#ff4500")
        
        # Clear widgets
        for w in self.root.winfo_children():
            w.destroy()
        
        # Main frame
        f = tk.Frame(self.root, bg="#ff4500")
        f.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Back button
        btn = tk.Button(f, text="← Widget", command=self.switch_widget, 
                       font=("Arial", 14, "bold"), bg="#cc0000", fg="white", 
                       relief="raised", bd=3, padx=15, pady=8)
        btn.pack(anchor="nw", pady=(0, 30))
        
        # Title
        title = tk.Label(f, text="ASTRONOMICAL WATCH", font=("Arial", 28, "bold"), 
                        bg="#ff4500", fg="white", relief="ridge", bd=4, padx=20, pady=10)
        title.pack(pady=20)
        
        # Main time
        self.time_lbl = tk.Label(f, text="000.000", font=("Courier", 70, "bold"), 
                                bg="#000000", fg="#00ff00", relief="sunken", bd=6, 
                                padx=40, pady=25)
        self.time_lbl.pack(pady=40)
        
        # Info frame
        info = tk.Frame(f, bg="#ff4500")
        info.pack(fill="x", pady=20)
        
        # Date
        self.date_lbl = tk.Label(info, text="Date: Loading...", font=("Arial", 22, "bold"), 
                                bg="#000000", fg="#ffff00", relief="solid", bd=2, 
                                padx=15, pady=8)
        self.date_lbl.pack(pady=8)
        
        # UTC
        self.utc_lbl = tk.Label(info, text="UTC: Loading...", font=("Arial", 22, "bold"), 
                               bg="#000000", fg="#00ffff", relief="solid", bd=2, 
                               padx=15, pady=8)
        self.utc_lbl.pack(pady=8)
        
        # mikroDies
        self.mikro_lbl = tk.Label(info, text="mikroDies: 000", font=("Arial", 18, "bold"), 
                                 bg="#000000", fg="#ff00ff", relief="solid", bd=2, 
                                 padx=15, pady=8)
        self.mikro_lbl.pack(pady=8)
        
        self.is_widget = False
    
    def switch_normal(self):
        self.create_normal()
    
    def switch_widget(self):
        self.create_widget()
    
    def update_time(self):
        try:
            data = get_time_data()
            time_text = f"{data['dies']:03d}.{data['milides']:03d}"
            self.time_lbl.config(text=time_text)
            
            if self.is_widget:
                self.date_lbl.config(text=data['utc'].strftime("%d/%m"))
            else:
                self.date_lbl.config(text=f"Date: {data['utc'].strftime('%d/%m/%Y')}")
                self.utc_lbl.config(text=f"UTC: {data['utc'].strftime('%H:%M:%S')}")
                self.mikro_lbl.config(text=f"mikroDies: {data['mikrodiet']:03d}")
            
        except Exception as e:
            self.time_lbl.config(text="ERR")
            print(f"Error: {e}")
        
        self.root.after(1000, self.update_time)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    SimpleAstroWatch().run()