# -*- coding: utf-8 -*-
"""
MINI TEST - Windows Desktop Compatibility
NO UNICODE - maksimalna kompatibilnost
"""
import tkinter as tk
from datetime import datetime, timezone

def create_mini_test():
    # Basic window
    root = tk.Tk()
    root.title("Astro Watch - Test")
    root.geometry("250x120")
    root.configure(bg='#1a1a2e')
    
    # Always on top
    try:
        root.attributes('-topmost', True)
    except:
        pass
    
    # Title
    title = tk.Label(root, 
                    text="ASTRONOMICAL WATCH TEST",
                    font=("Arial", 10, "bold"),
                    bg='#1a1a2e', 
                    fg='#f39c12')
    title.pack(pady=5)
    
    # Time display
    time_label = tk.Label(root,
                         text="000.000",
                         font=("Courier", 14, "bold"),
                         bg='#1a1a2e',
                         fg='#3498db')
    time_label.pack(pady=5)
    
    # UTC display
    utc_label = tk.Label(root,
                        text="UTC: --:--:--",
                        font=("Arial", 9),
                        bg='#1a1a2e',
                        fg='#ecf0f1')
    utc_label.pack(pady=5)
    
    # Status
    status_label = tk.Label(root,
                           text="Status: Testing...",
                           font=("Arial", 8),
                           bg='#1a1a2e',
                           fg='#2ecc71')
    status_label.pack(pady=5)
    
    def update_test():
        try:
            now = datetime.now(timezone.utc)
            
            # Simple simulation (days since 2025)
            start_2025 = datetime(2025, 1, 1, tzinfo=timezone.utc)
            days_since = (now - start_2025).days
            
            # Current part of day as milides
            seconds_today = now.hour * 3600 + now.minute * 60 + now.second
            milides = int((seconds_today / 86400.0) * 1000)
            
            # Display format
            time_str = "{:03d}.{:03d}".format(days_since, milides)
            time_label.config(text=time_str)
            
            # UTC time
            utc_label.config(text="UTC: " + now.strftime('%H:%M:%S'))
            
            # Status
            status_label.config(text="Status: Running OK", fg='#2ecc71')
            
        except Exception as e:
            time_label.config(text="ERROR")
            status_label.config(text="Error: " + str(e)[:15], fg='#e74c3c')
        
        # Update every second
        root.after(1000, update_test)
    
    # Start updates
    update_test()
    
    print("MINI TEST STARTED")
    print("Ako vidiš window, desktop aplikacije će raditi!")
    print("Zatvori window da završiš test.")
    
    return root

if __name__ == "__main__":
    print("=== MINI ASTRO WATCH TEST ===")
    print("Windows Desktop Compatibility Check")
    print("")
    
    try:
        app = create_mini_test()
        app.mainloop()
        print("TEST USPEŠAN!")
        print("Desktop aplikacije su kompatibilne.")
    except Exception as e:
        print("TEST NEUSPEŠAN: " + str(e))
        print("Možda trebaš da instaliraš Python ili tkinter.")