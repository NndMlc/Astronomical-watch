# -*- coding: utf-8 -*-
"""
Astronomical Watch - Console Version (NO GUI)
Za Windows sisteme gde tkinter ne radi
"""
import sys
import time
from datetime import datetime, timezone, timedelta
import os

class ConsoleAstronomicalWatch:
    """Console verzija Astronomical Watch-a"""
    
    def __init__(self):
        self.running = True
        
    def calculate_astronomical_time(self, dt):
        """Izračunaj astronomical time"""
        # Equinox 2025
        equinox_2025 = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
        
        # Sekunde od equinox-a
        seconds_since = (dt - equinox_2025).total_seconds()
        
        # Day boundary (23:15:54 UTC)
        boundary_hours = 23.2650
        boundary_offset = timedelta(hours=boundary_hours)
        
        # Konvertuj u dane
        raw_days = seconds_since / 86400.0
        adjusted_days = raw_days + (boundary_offset.total_seconds() / 86400.0)
        
        # Izvuci komponente
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
            'fraction': mikrodiet_fraction
        }
    
    def clear_screen(self):
        """Očisti konzolu"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_time(self):
        """Prikaži vreme u konzoli"""
        try:
            now = datetime.now(timezone.utc)
            astro_data = self.calculate_astronomical_time(now)
            
            # Clear screen za refresh
            self.clear_screen()
            
            print("=" * 50)
            print("       ASTRONOMICAL WATCH CONSOLE")
            print("       mikroDies Precision Display")
            print("=" * 50)
            print("")
            
            # Main time display
            time_str = "{:03d}.{:03d}.{:03d}".format(
                astro_data['day_index'],
                astro_data['miliDies'],
                astro_data['mikroDies']
            )
            
            print(f"  ASTRONOMICAL TIME: {time_str}")
            print("  Format: Dies.miliDies.mikroDies")
            print("")
            
            # Details
            print(f"  UTC Time:      {now.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Dies:          {astro_data['day_index']}")
            print(f"  miliDies:      {astro_data['miliDies']}")
            print(f"  mikroDies:     {astro_data['mikroDies']}")
            print(f"  Precision:     {astro_data['fraction']:.6f}")
            print("")
            
            # Progress bar za miliDies
            progress = astro_data['miliDies'] / 10.0  # 0-100%
            bar_length = 30
            filled = int(progress * bar_length / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"  miliDies [{bar}] {progress:.1f}%")
            print("")
            
            print("  Press Ctrl+C to exit")
            print("  Updates every 1 second")
            print("=" * 50)
            
        except Exception as e:
            print(f"ERROR: {e}")
    
    def run(self):
        """Pokreni console aplikaciju"""
        print("Astronomical Watch Console - Starting...")
        print("Real-time mikroDies display in console")
        print("")
        
        try:
            while self.running:
                self.display_time()
                time.sleep(1)  # Update every second
                
        except KeyboardInterrupt:
            self.clear_screen()
            print("Astronomical Watch Console - Stopped")
            print("Thank you for using Astronomical Watch!")

def main():
    """Glavna funkcija"""
    print("=== ASTRONOMICAL WATCH CONSOLE ===")
    print("Windows Compatible - No GUI Required")
    print("mikroDies Precision Timekeeping")
    print("")
    
    app = ConsoleAstronomicalWatch()
    app.run()

if __name__ == "__main__":
    main()