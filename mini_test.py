"""
MINI ASTRONOMICAL WATCH TEST - Windows Quick Test
Kopiraj ovaj kod u .py fajl na Windows-u i pokreni sa: python test.py
"""
import tkinter as tk
from datetime import datetime, timezone

def create_test_app():
    # Kreiranje osnovnog window-a
    root = tk.Tk()
    root.title("🌟 Astro Watch - Test")
    root.geometry("280x150")
    root.configure(bg='#1a1a2e')
    
    # Always on top
    root.attributes('-topmost', True)
    
    # Header
    title_label = tk.Label(root, 
                          text="🌟 Astronomical Watch Test",
                          font=("Arial", 12, "bold"),
                          bg='#1a1a2e', 
                          fg='#f39c12')
    title_label.pack(pady=10)
    
    # Time display
    time_label = tk.Label(root,
                         text="000.000",
                         font=("Courier", 16, "bold"),
                         bg='#1a1a2e',
                         fg='#3498db')
    time_label.pack(pady=5)
    
    # UTC display
    utc_label = tk.Label(root,
                        text="UTC: --:--:--",
                        font=("Arial", 10),
                        bg='#1a1a2e',
                        fg='#ecf0f1')
    utc_label.pack(pady=5)
    
    # Status
    status_label = tk.Label(root,
                           text="Status: Testing...",
                           font=("Arial", 9),
                           bg='#1a1a2e',
                           fg='#2ecc71')
    status_label.pack(pady=5)
    
    def update_time():
        try:
            now = datetime.now(timezone.utc)
            
            # Simulacija astronomical time (jednostavna verzija)
            # Dies od početka 2025. godine
            start_2025 = datetime(2025, 1, 1, tzinfo=timezone.utc)
            days_since = (now - start_2025).days
            
            # Trenutni deo dana kao milides (0-999)
            seconds_today = now.hour * 3600 + now.minute * 60 + now.second
            milides = int((seconds_today / 86400.0) * 1000)
            
            # Format prikaza
            time_str = f"{days_since:03d}.{milides:03d}"
            time_label.config(text=time_str)
            
            # UTC time
            utc_label.config(text=f"UTC: {now.strftime('%H:%M:%S')}")
            
            # Status
            status_label.config(text="Status: Running ✓", fg='#2ecc71')
            
        except Exception as e:
            time_label.config(text="ERROR")
            status_label.config(text=f"Error: {str(e)[:20]}", fg='#e74c3c')
        
        # Update every second
        root.after(1000, update_time)
    
    # Start updates
    update_time()
    
    print("🚀 Mini Astronomical Watch Test - Running...")
    print("Ako vidiš ovaj window, desktop aplikacije će raditi!")
    print("Zatvori window da završiš test.")
    
    return root

if __name__ == "__main__":
    print("=== MINI ASTRO WATCH TEST ===")
    print("Windows Desktop Compatibility Test")
    print()
    
    try:
        app = create_test_app()
        app.mainloop()
        print("✓ Test završen uspešno!")
        print("Desktop aplikacije su kompatibilne sa tvojim sistemom.")
    except Exception as e:
        print(f"❌ Test neuspešan: {e}")
        print("Možda trebaš da instaliraš tkinter ili Python.")