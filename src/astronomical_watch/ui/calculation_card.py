import tkinter as tk
from datetime import datetime, timezone, timedelta
import math
import sys
import os
from .translations import tr

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

def get_location():
    if is_mobile():
        # TODO: implement real geolocation for mobile
        # Stub: Example for Belgrade (connect with GPS API)
        return {"lat": 44.7866, "lon": 20.4489, "source": "Device geolocation"}
    else:
        # No geolocation (desktop), use local system time
        return {"lat": None, "lon": None, "source": "Local system time"}

def get_local_noon_milidies(lat, lon, date=None):
    if lat is None or lon is None:
        return 500  # midpoint of the day
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
    eqt_milidies = [int(round(v * 60 / 86.4)) for v in eqt]
    return days, eqt, eqt_milidies

class CalculationCard(tk.Toplevel):
    def __init__(self, master=None, lang="en"):
        super().__init__(master)
        self.lang = lang
        self.title(f"{tr('calculations', self.lang)} — {tr('title', self.lang)}")
        self.geometry("600x690")
        self.minsize(500, 570)
        self.location = None
        self._make_widgets()
        self._request_location()

    def _make_widgets(self):
        font_label = ("Arial", 11)
        self.loc_label = tk.Label(self, text=tr("location_not_set", self.lang), font=font_label)
        self.loc_label.pack(pady=(18,6))
        self.allow_btn = tk.Button(self, text=tr("allow_location_button", self.lang), command=self._request_location, font=font_label)
        self.allow_btn.pack(pady=(0,10))
        self.refresh_btn = tk.Button(self, text=tr("refresh_location_button", self.lang), command=self._request_location, font=font_label)
        self.refresh_btn.pack(pady=(0,10))
        self.merid_label = tk.Label(self, text=tr("meridian_label", self.lang), font=font_label)
        self.merid_label.pack(pady=(12,2))
        self.merid_val = tk.Label(self, text="---", font=("Arial", 13, "bold"), fg="#2060b0")
        self.merid_val.pack()
        if MATHPLOTLIB_AVAILABLE:
            self.graph_frame = tk.Frame(self)
            self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=18)
        else:
            self.graph_frame = None
            tk.Label(self, text=tr("graph_unavailable", self.lang), font=font_label, fg="red").pack(pady=18)
        self.eqt_label = tk.Label(self, text=tr("eqt_curve_label", self.lang), font=font_label)
        self.eqt_label.pack()
        self.eqt_y_val = tk.Label(self, text=tr("eqt_offset_label", self.lang), font=font_label, fg="#b02c06")
        self.eqt_y_val.pack(pady=(4,10))
        tk.Label(self, text=tr("eqt_y_axis_label", self.lang), font=("Arial", 10)).pack(pady=(2,6))
        tk.Label(self, text=tr("year_markers_label", self.lang), font=("Arial", 10)).pack(pady=(2,10))
        tk.Button(self, text=tr("close_button", self.lang), command=self.destroy, font=("Arial", 10), padx=12, pady=5).pack(pady=12)

    def _request_location(self):
        self.location = get_location()
        if self.location["lat"] is None or self.location["lon"] is None:
            self.loc_label.config(text=tr("location_fallback_label", self.lang))
        else:
            self.loc_label.config(text=tr("location_set_label", self.lang, lat=self.location["lat"], lon=self.location["lon"], source=self.location["source"]))
        self.allow_btn.config(state=tk.DISABLED)
        self.refresh_btn.config(state=tk.NORMAL)
        self._update_meridian()
        self._update_graph()

    def _update_meridian(self):
        milidies = get_local_noon_milidies(self.location.get("lat"), self.location.get("lon"))
        self.merid_val.config(text=tr("meridian_value_label", self.lang, milidies=milidies))

    def _update_graph(self):
        if not MATHPLOTLIB_AVAILABLE or self.graph_frame is None:
            return
        year = datetime.now().year
        days, eqt, eqt_milidies = equation_of_time_curve(year)
        fig = Figure(figsize=(7,3.6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(days, eqt, color="#e02f2f", lw=2, label="Minutes")
        ax.plot(days, eqt_milidies, color="#3685d1", lw=2, label="miliDies")
        ax.set_ylabel(tr("eqt_graph_ylabel", self.lang))
        ax.set_xlabel(tr("eqt_graph_xlabel", self.lang))
        ax.axhline(0, color="grey", ls="dashed", lw=1)
        today = datetime.now().timetuple().tm_yday
        ax.axvline(today, color="red", lw=2, label=tr("eqt_today_label", self.lang))
        markers = {
            tr("marker_vernal_equinox", self.lang): 80,
            tr("marker_summer_solstice", self.lang): 172,
            tr("marker_autumn_equinox", self.lang): 266,
            tr("marker_winter_solstice", self.lang): 355,
            tr("marker_jan1", self.lang): 1
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
        eqt_today = eqt[today % len(eqt)]
        eqt_today_md = eqt_milidies[today % len(eqt)]
        self.eqt_y_val.config(text=tr("eqt_offset_value_label", self.lang, eqt_today=eqt_today, eqt_today_md=eqt_today_md))

def create_calculation_card(master=None, lang="en"):
    """Factory function to create CalculationCard instance."""
    return CalculationCard(master, lang)