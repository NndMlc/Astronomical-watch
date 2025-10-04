import tkinter as tk
from datetime import datetime, timezone, timedelta
import math
import sys
import os

def is_mobile():
    if sys.platform == 'android':
        return True
    if sys.platform == 'ios':
        return True
    if sys.platform == 'linux' and 'ANDROID_ARGUMENT' in os.environ:
        return True
    return False

def get_location():
    if is_mobile():
        # TODO: implement real geolocation for mobile
        # Stub: Primer za Beograd (možeš povezati sa GPS API)
        return {"lat": 44.7866, "lon": 20.4489, "source": "Device geolocation"}
    else:
        return {"lat": None, "lon": None, "source": "Local system time"}

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATHPLOTLIB_AVAILABLE = True
except ImportError:
    MATHPLOTLIB_AVAILABLE = False

# Platform check (stub, proširi po potrebi)
def is_mobile():
    # Ovo je stub: u pravoj aplikaciji koristi sys.platform, os, ili specifične module
    # Na desktopu: 'win'/'linux'/'darwin', na mobilnom: 'android'/'ios'
    # Za demo, koristi False (desktop)
    return False

# Za desktop koristi sistemsko vreme, za mobilno geolokaciju
def get_location():
    if is_mobile():
        # Prava geolokacija (stub, koristi native API na mobilnom)
        # Primer za Beograd
        return {"lat": 44.7866, "lon": 20.4489, "source": "Device geolocation"}
    else:
        # Desktop: nema geolokacije, koristi lokalno vreme
        return {"lat": None, "lon": None, "source": "Local system time"}

def get_local_noon_milidies(lat, lon, date=None):
    # Ako nema lat/lon, koristi baznu vrednost
    if lat is None or lon is None:
        return 500  # sredina dana
    offset_sec = lon * 4 * 60
    base_milidies = 500
    milidies_offset = int(round(offset_sec / 86.4))
    return (base_milidies + milidies_offset) % 1000

def equation_of_time_curve(year):
    days = list(range(366))
    eqt = []
    for d in days:
        eq = 7.5 * math.sin(2*math.pi*d/365 - 1.9) + 16.4 * math.sin(4*math.pi*d/365 - 0.4)
        eqt.append(eq)
    # Preračunaj u miliDies
    eqt_milidies = [int(round(v * 60 / 86.4)) for v in eqt]
    return days, eqt, eqt_milidies

class CalculationCard(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Calculations — Astronomical Watch")
        self.geometry("600x690")
        self.minsize(500, 570)
        self.location = None
        self._make_widgets()
        self._request_location()

    def _make_widgets(self):
        font_label = ("Arial", 11)
        self.loc_label = tk.Label(self, text="Location: (not set)", font=font_label)
        self.loc_label.pack(pady=(18,6))
        self.allow_btn = tk.Button(self, text="Allow location access", command=self._request_location, font=font_label)
        self.allow_btn.pack(pady=(0,10))
        self.refresh_btn = tk.Button(self, text="Refresh location", command=self._request_location, font=font_label)
        self.refresh_btn.pack(pady=(0,10))
        self.merid_label = tk.Label(self, text="Astronomical meridian (miliDies):", font=font_label)
        self.merid_label.pack(pady=(12,2))
        self.merid_val = tk.Label(self, text="---", font=("Arial", 13, "bold"), fg="#2060b0")
        self.merid_val.pack()
        # Equation of Time krivulja
        if MATHPLOTLIB_AVAILABLE:
            self.graph_frame = tk.Frame(self)
            self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=18)
        else:
            self.graph_frame = None
            tk.Label(self, text="Graph unavailable (matplotlib not installed)", font=font_label, fg="red").pack(pady=18)
        self.eqt_label = tk.Label(self, text="Equation of Time curve for your location", font=font_label)
        self.eqt_label.pack()
        self.eqt_y_val = tk.Label(self, text="Current EoT offset: -- min / -- miliDies", font=font_label, fg="#b02c06")
        self.eqt_y_val.pack(pady=(4,10))
        tk.Label(self, text="Y axis: red = minutes, blue = miliDies", font=("Arial", 10)).pack(pady=(2,6))
        tk.Label(self, text="Year markers: vernal equinox, autumnal equinox, summer/winter solstice, Jan 1", font=("Arial", 10)).pack(pady=(2,10))
        tk.Button(self, text="Close", command=self.destroy, font=("Arial", 10), padx=12, pady=5).pack(pady=12)

    def _request_location(self):
        self.location = get_location()
        if self.location["lat"] is None or self.location["lon"] is None:
            self.loc_label.config(text=f"Location: Local system time (no geolocation)")
        else:
            self.loc_label.config(text=f"Location: {self.location['lat']:.4f}°, {self.location['lon']:.4f}° (from {self.location['source']})")
        self.allow_btn.config(state=tk.DISABLED)
        self.refresh_btn.config(state=tk.NORMAL)
        self._update_meridian()
        self._update_graph()

    def _update_meridian(self):
        milidies = get_local_noon_milidies(self.location.get("lat"), self.location.get("lon"))
        self.merid_val.config(text=f"{milidies} miliDies")

    def _update_graph(self):
        if not MATHPLOTLIB_AVAILABLE or self.graph_frame is None:
            return
        year = datetime.now().year
        days, eqt, eqt_milidies = equation_of_time_curve(year)
        fig = Figure(figsize=(7,3.6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(days, eqt, color="#e02f2f", lw=2, label="Minutes")
        ax.plot(days, eqt_milidies, color="#3685d1", lw=2, label="miliDies")
        ax.set_ylabel("Equation of Time (min / miliDies)")
        ax.set_xlabel("Day of Year")
        ax.axhline(0, color="grey", ls="dashed", lw=1)
        today = datetime.now().timetuple().tm_yday
        ax.axvline(today, color="red", lw=2, label="Today")
        markers = {
            "Vernal Eq.": 80,
            "Summer Solstice": 172,
            "Autumn Eq.": 266,
            "Winter Solstice": 355,
            "Jan 1": 1
        }
        for name, d in markers.items():
            ax.axvline(d, color="green", lw=1)
            ax.text(d+2, ax.get_ylim()[1]*0.9, name, color="green", fontsize=8, rotation=90)
        ax.set_xlim(today-182, today+182)
        ax.legend()
        fig.tight_layout()
        for child in self.graph_frame.winfo_children():
            child.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # Prikaži trenutni offset
        eqt_today = eqt[today % len(eqt)]
        eqt_today_md = eqt_milidies[today % len(eqt)]
        self.eqt_y_val.config(text=f"Current EoT offset: {eqt_today:.2f} min / {eqt_today_md} miliDies")