import tkinter as tk
from datetime import datetime, timezone, timedelta
import math
import sys
import os
from .translations import tr
from .gradient import get_sky_theme, create_gradient_colors

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATHPLOTLIB_AVAILABLE = True
except ImportError:
    MATHPLOTLIB_AVAILABLE = False

def is_mobile():
    if sys.platform == 'android':
        return True
    if sys.platform == 'ios':
        return True
    if sys.platform == 'linux' and 'ANDROID_ARGUMENT' in os.environ:
        return True
    return False

# Major cities coordinates for timezone-based location estimation
TIMEZONE_CITIES = {
    'UTC': {'city': 'Greenwich', 'lon': 0.0, 'lat': 51.5},
    'CET': {'city': 'Belgrade', 'lon': 20.45, 'lat': 44.8},  # Central European Time
    'CEST': {'city': 'Belgrade', 'lon': 20.45, 'lat': 44.8},  # Central European Summer Time
    'EET': {'city': 'Athens', 'lon': 23.72, 'lat': 37.98},
    'EEST': {'city': 'Athens', 'lon': 23.72, 'lat': 37.98},
    'WET': {'city': 'Lisbon', 'lon': -9.14, 'lat': 38.71},
    'WEST': {'city': 'Lisbon', 'lon': -9.14, 'lat': 38.71},
    'GMT': {'city': 'London', 'lon': -0.12, 'lat': 51.51},
    'BST': {'city': 'London', 'lon': -0.12, 'lat': 51.51},
    'MSK': {'city': 'Moscow', 'lon': 37.62, 'lat': 55.75},
    'IST': {'city': 'New Delhi', 'lon': 77.21, 'lat': 28.61},
    'CST': {'city': 'Beijing', 'lon': 116.40, 'lat': 39.90},
    'JST': {'city': 'Tokyo', 'lon': 139.69, 'lat': 35.69},
    'AEST': {'city': 'Sydney', 'lon': 151.21, 'lat': -33.87},
    'AEDT': {'city': 'Sydney', 'lon': 151.21, 'lat': -33.87},
    'NZST': {'city': 'Wellington', 'lon': 174.78, 'lat': -41.29},
    'NZDT': {'city': 'Wellington', 'lon': 174.78, 'lat': -41.29},
    'EST': {'city': 'New York', 'lon': -74.01, 'lat': 40.71},
    'EDT': {'city': 'New York', 'lon': -74.01, 'lat': 40.71},
    'PST': {'city': 'Los Angeles', 'lon': -118.24, 'lat': 34.05},
    'PDT': {'city': 'Los Angeles', 'lon': -118.24, 'lat': 34.05},
    'MST': {'city': 'Denver', 'lon': -104.99, 'lat': 39.74},
    'MDT': {'city': 'Denver', 'lon': -104.99, 'lat': 39.74},
}

def get_location():
    """Get user location from system timezone.
    
    Uses timezone name to find the major city in that timezone,
    then returns that city's longitude for solar noon calculation.
    """
    try:
        import time
        import os
        
        # First, try to set TZ from /etc/timezone if available
        if os.path.exists('/etc/timezone'):
            with open('/etc/timezone', 'r') as f:
                tz_file = f.read().strip()
                # Map timezone file to timezone abbreviation
                if 'Belgrade' in tz_file or 'Central' in tz_file:
                    # Manually set for CET
                    return {
                        "lat": 44.8,
                        "lon": 20.45,
                        "source": "Belgrade (CET from /etc/timezone)"
                    }
        
        # Get local time info
        local_time = time.localtime()
        
        # Get timezone offset in seconds
        if time.daylight and local_time.tm_isdst:
            offset_seconds = -time.altzone
        else:
            offset_seconds = -time.timezone
        
        offset_hours = offset_seconds / 3600
        
        # Get timezone name (e.g., 'CET', 'CEST', 'UTC')
        tz_name = time.tzname[local_time.tm_isdst] if hasattr(time, 'tzname') else None
        
        # Try to find city for this timezone
        if tz_name and tz_name in TIMEZONE_CITIES:
            city_info = TIMEZONE_CITIES[tz_name]
            return {
                "lat": city_info['lat'],
                "lon": city_info['lon'],
                "source": f"{city_info['city']} ({tz_name}, UTC{offset_hours:+.1f})"
            }
        
        # Fallback: estimate longitude from UTC offset (15° per hour)
        estimated_lon = offset_hours * 15
        return {
            "lat": None,
            "lon": estimated_lon,
            "source": f"Estimated from timezone (UTC{offset_hours:+.1f})"
        }
        
    except Exception as e:
        # Ultimate fallback
        return {"lat": None, "lon": 0, "source": f"UTC (fallback: {e})"}

def get_local_noon_milidies(lat, lon, date=None):
    """Calculate when solar noon occurs at given longitude, in miliDies.
    
    The reference meridian is -168.975° (168°58'30"W), where solar noon 
    occurs at 23:15:54 UTC, which is 000 miliDies (start of Dies).
    
    Solar noon shifts by 4 minutes (240 seconds) per degree of longitude.
    East of reference = earlier solar noon
    West of reference = later solar noon
    
    Example: Belgrade at 20.45°E
    - Difference: 20.45 - (-168.975) = 189.425° (east of reference)
    - Time offset: 189.425 × 4 min = 757.7 min = 45,462 sec
    - In miliDies: 45,462 / 86.4 = 526.18 miliDies
    - East = earlier, so: 000 - 526 = -526
    - Wrap around: -526 + 1000 = 474 miliDies
    
    So solar noon in Belgrade occurs at 474 miliDies (earlier in the Dies).
    """
    from ..core.astro_time_core import LONGITUDE_REF_DEG
    
    if lon is None:
        lon = 0
    
    # Calculate longitude difference from reference meridian
    # Positive difference = location is east of reference
    lon_diff = lon - LONGITUDE_REF_DEG
    
    # Solar noon shifts by 4 minutes (240 seconds) per degree of longitude
    offset_seconds = lon_diff * 240
    
    # Convert to miliDies (1 miliDies = 86.4 seconds)
    milidies_offset = offset_seconds / 86.4
    
    # Base is 000 miliDies (solar noon at reference meridian = start of Dies)
    # East of reference means earlier time, so subtract
    result = (0 - milidies_offset) % 1000
    
    return int(round(result))

def equation_of_time_curve(year):
    days = list(range(366))
    eqt = []
    for d in days:
        eq = 7.5 * math.sin(2*math.pi*d/365 - 1.9) + 16.4 * math.sin(4*math.pi*d/365 - 0.4)
        eqt.append(eq)
    eqt_milidies = [int(round(v * 60 / 86.4)) for v in eqt]
    return days, eqt, eqt_milidies

class CalculationCard(tk.Toplevel):
    def __init__(self, master=None, lang="en"):
        super().__init__(master)
        self.lang = lang
        self.title(f"Calculations — Astronomical Watch")
        self.geometry("600x690")
        self.minsize(500, 570)
        
        # Get sky theme for gradient
        self.theme = get_sky_theme(datetime.now(timezone.utc))
        
        # Create canvas for gradient background
        self.canvas = tk.Canvas(self, width=600, height=690, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._draw_gradient()
        
        # Get text color from theme
        self.text_color = self.theme.text_color
        self.bg_color = self.theme.bottom_color
        
        self.location = None
        
        print("🔧 CalculationCard: Initializing...")
        self._make_widgets()
        print("🔧 CalculationCard: Widgets created")
        
        # Force update to ensure window is drawn
        self.update_idletasks()
        
        # Auto-request location on startup
        self.after(100, self._request_location)
        print("🔧 CalculationCard: Scheduled location request")
    
    def _draw_gradient(self):
        """Draw gradient background on canvas"""
        width = 600
        height = 690
        
        # Create gradient colors
        colors = create_gradient_colors(self.theme, steps=height)
        
        # Draw gradient as horizontal lines
        for i, color in enumerate(colors):
            self.canvas.create_line(0, i, width, i, fill=color, width=1)

    def _make_widgets(self):
        font_label = ("Arial", 11)
        
        # Main container frame with theme background
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Title
        tk.Label(main_frame, text="Astronomical Calculations", 
                font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.text_color).pack(pady=(18,12))
        
        # Location section
        tk.Label(main_frame, text="📍 Location Information", 
                font=("Arial", 13, "bold"), bg=self.bg_color, fg=self.text_color).pack(pady=(6,6))
        self.loc_label = tk.Label(main_frame, text="Calculating...", 
                                  font=font_label, bg=self.bg_color, fg=self.text_color)
        self.loc_label.pack(pady=(0,6))
        
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=(0,10))
        self.refresh_btn = tk.Button(button_frame, text="Refresh", 
                                     command=self._request_location, font=font_label)
        self.refresh_btn.pack(padx=5)
        
        tk.Frame(main_frame, height=2, bg="#cccccc").pack(fill="x", pady=12)
        
        # Meridian section
        tk.Label(main_frame, text="🕛 Local Solar Noon", 
                font=("Arial", 13, "bold"), bg=self.bg_color, fg=self.text_color).pack(pady=(12,2))
        self.merid_label = tk.Label(main_frame, text="Solar noon occurs at:", 
                                    font=font_label, bg=self.bg_color, fg=self.text_color)
        self.merid_label.pack(pady=(0,2))
        self.merid_val = tk.Label(main_frame, text="Calculating...", 
                                  font=("Arial", 16, "bold"), fg="#2060b0", bg=self.bg_color)
        self.merid_val.pack(pady=(0,10))
        
        tk.Frame(main_frame, height=2, bg="#cccccc").pack(fill="x", pady=12)
        
        # Graph section
        tk.Label(main_frame, text="📊 Equation of Time", 
                font=("Arial", 13, "bold"), bg=self.bg_color, fg=self.text_color).pack(pady=(12,6))
        
        if MATHPLOTLIB_AVAILABLE:
            self.graph_frame = tk.Frame(main_frame, relief="sunken", borderwidth=1, bg="white")
            self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0,12))
            
            self.eqt_y_val = tk.Label(main_frame, text="Loading graph...", 
                                     font=font_label, fg="#b02c06", bg=self.bg_color)
            self.eqt_y_val.pack(pady=(0,6))
            
            info_text = "Red line: current day | Green lines: seasonal markers\nShows solar time offset throughout the year"
            tk.Label(main_frame, text=info_text, font=("Arial", 9), 
                    fg="#666666", bg=self.bg_color).pack(pady=(0,12))
        else:
            tk.Label(main_frame, text="⚠️ Matplotlib not available - graph cannot be displayed", 
                    font=font_label, fg="red", bg=self.bg_color).pack(pady=18)
        
        # Close button
        tk.Button(main_frame, text="Close", command=self.destroy, font=("Arial", 11), 
                 padx=20, pady=8, bg="#4CAF50", fg="white").pack(pady=12)

    def _request_location(self):
        print("🔧 _request_location: Starting...")
        try:
            self.location = get_location()
            print(f"🔧 _request_location: Got location: {self.location}")
            
            if self.location["lon"] is not None:
                self.loc_label.config(text=f"Longitude: {self.location['lon']:.2f}° (from {self.location['source']})")
            else:
                self.loc_label.config(text="Using UTC reference (0° longitude)")
            
            print("🔧 _request_location: Calling _update_meridian...")
            self._update_meridian()
            
            print("🔧 _request_location: Calling _update_graph...")
            self._update_graph()
            
            print("🔧 _request_location: Completed successfully")
        except Exception as e:
            self.loc_label.config(text=f"Error: {str(e)}")
            print(f"❌ Location error: {e}")
            import traceback
            traceback.print_exc()

    def _update_meridian(self):
        try:
            milidies = get_local_noon_milidies(self.location.get("lat"), self.location.get("lon"))
            # Convert miliDies to hours:minutes
            total_seconds = milidies * 86.4
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            self.merid_val.config(text=f"{milidies:03d} miliDies (~{hours:02d}:{minutes:02d})")
        except Exception as e:
            self.merid_val.config(text=f"Error: {str(e)}")
            print(f"Meridian error: {e}")

    def _update_graph(self):
        if not MATHPLOTLIB_AVAILABLE or not hasattr(self, 'graph_frame') or self.graph_frame is None:
            return
        
        try:
            year = datetime.now().year
            days, eqt, eqt_milidies = equation_of_time_curve(year)
            fig = Figure(figsize=(5.5, 3.2), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(days, eqt, color="#e02f2f", lw=2, label="Minutes offset")
            ax.plot(days, eqt_milidies, color="#3685d1", lw=2, label="miliDies offset")
            ax.set_ylabel("Time offset")
            ax.set_xlabel("Day of year")
            ax.axhline(0, color="grey", ls="dashed", lw=1)
            today = datetime.now().timetuple().tm_yday
            ax.axvline(today, color="red", lw=2, label="Today")
            
            # Seasonal markers
            markers = {
                "Vernal Eq": 80,
                "Summer Sol": 172,
                "Autumn Eq": 266,
                "Winter Sol": 355,
                "Jan 1": 1
            }
            for name, d in markers.items():
                ax.axvline(d, color="green", lw=1, alpha=0.5)
                ax.text(d+2, ax.get_ylim()[1]*0.85, name, color="green", fontsize=7, rotation=90)
            
            ax.set_xlim(today-182, today+182)
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            
            # Clear previous graph
            for child in self.graph_frame.winfo_children():
                child.destroy()
            
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            eqt_today = eqt[today % len(eqt)]
            eqt_today_md = eqt_milidies[today % len(eqt)]
            self.eqt_y_val.config(text=f"Today's offset: {eqt_today:.1f} minutes = {eqt_today_md} miliDies")
        except Exception as e:
            if hasattr(self, 'eqt_y_val'):
                self.eqt_y_val.config(text=f"Graph error: {str(e)}")
            print(f"Graph error: {e}")
            import traceback
            traceback.print_exc()

def create_calculation_card(master=None, lang="en"):
    """Factory function to create CalculationCard instance."""
    return CalculationCard(master, lang)