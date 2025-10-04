import tkinter as tk
from datetime import datetime, timezone, timedelta
from core.astro_time_core import get_current_equinox, AstronomicalYear, get_next_equinox

def milidies_to_hm(milidies):
    total_seconds = milidies * 86.4  # 1 milidies = 86.4 sekunde
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

def hm_to_milidies(h, m, s=0):
    seconds = h*3600 + m*60 + s
    milidies = int(round(seconds / 86.4))
    return milidies

class ComparisonCard(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Comparison — Astronomical Watch")
        self.geometry("510x560")
        self.minsize(470, 400)

        self._make_widgets()
        self._update_equinox_countdown()

    def _make_widgets(self):
        font_label = ("Arial", 11)
        font_entry = ("Arial", 11)
        # Standard → Astronomical
        tk.Label(self, text="Standard date/time → Astronomical:", font=font_label).pack(pady=(16, 2))
        frame1 = tk.Frame(self)
        frame1.pack(pady=(0, 4))
        self.std_entry = tk.Entry(frame1, font=font_entry, width=22)
        self.std_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.std_entry.pack(side=tk.LEFT)
        tk.Button(frame1, text="Convert", command=self._convert_std_to_astro).pack(side=tk.LEFT, padx=8)
        self.std_result = tk.Label(self, text="", font=font_label, fg="#2060b0")
        self.std_result.pack()

        # Astronomical → Standard
        tk.Label(self, text="Astronomical (day/milidies) → Standard:", font=font_label).pack(pady=(18,2))
        frame2 = tk.Frame(self)
        frame2.pack(pady=(0,4))
        self.astro_day_entry = tk.Entry(frame2, font=font_entry, width=7)
        self.astro_day_entry.insert(0, "0")
        self.astro_day_entry.pack(side=tk.LEFT)
        tk.Label(frame2, text="Dies", font=font_label).pack(side=tk.LEFT)
        self.astro_milidies_entry = tk.Entry(frame2, font=font_entry, width=7)
        self.astro_milidies_entry.insert(0, "0")
        self.astro_milidies_entry.pack(side=tk.LEFT)
        tk.Label(frame2, text="miliDies", font=font_label).pack(side=tk.LEFT)
        tk.Button(frame2, text="Convert", command=self._convert_astro_to_std).pack(side=tk.LEFT, padx=8)
        self.astro_result = tk.Label(self, text="", font=font_label, fg="#2060b0")
        self.astro_result.pack()

        # Milidies ↔ hh:mm
        tk.Label(self, text="Convert milidies ↔ hh:mm:", font=font_label).pack(pady=(18,2))
        frame3 = tk.Frame(self)
        frame3.pack(pady=(0,4))
        self.milidies_entry = tk.Entry(frame3, font=font_entry, width=7)
        self.milidies_entry.insert(0, "0")
        self.milidies_entry.pack(side=tk.LEFT)
        tk.Button(frame3, text="→ Time", command=self._milidies_to_time).pack(side=tk.LEFT, padx=4)
        self.time_entry_h = tk.Entry(frame3, font=font_entry, width=3)
        self.time_entry_h.insert(0, "00")
        self.time_entry_h.pack(side=tk.LEFT)
        tk.Label(frame3, text=":", font=font_label).pack(side=tk.LEFT)
        self.time_entry_m = tk.Entry(frame3, font=font_entry, width=3)
        self.time_entry_m.insert(0, "00")
        self.time_entry_m.pack(side=tk.LEFT)
        tk.Button(frame3, text="→ Milidies", command=self._time_to_milidies).pack(side=tk.LEFT, padx=4)
        self.milidies_result = tk.Label(self, text="", font=font_label, fg="#2060b0")
        self.milidies_result.pack()

        # Countdown do sledeće prolećne ravnodnevnice
        tk.Label(self, text="Time until next vernal equinox:", font=font_label).pack(pady=(18,2))
        self.astro_equinox_countdown = tk.Label(self, text="", font=font_label, fg="#b02c06")
        self.astro_equinox_countdown.pack()
        self.std_equinox_countdown = tk.Label(self, text="", font=font_label, fg="#b02c06")
        self.std_equinox_countdown.pack()

        tk.Button(self, text="Close", command=self.destroy, font=("Arial", 10), padx=12, pady=5).pack(pady=14)

    def _convert_std_to_astro(self):
        try:
            dt_str = self.std_entry.get().strip()
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            dt = dt.replace(tzinfo=timezone.utc)
            eq = get_current_equinox(dt)
            astro_year = AstronomicalYear(eq)
            astro_year.update(dt)
            day = astro_year.day_index
            milidies = astro_year.milidan
            self.std_result.config(text=f"Astronomical: {day} Dies, {milidies} miliDies")
        except Exception as e:
            self.std_result.config(text=f"Error: {e}")

    def _convert_astro_to_std(self):
        try:
            day = int(self.astro_day_entry.get())
            milidies = int(self.astro_milidies_entry.get())
            eq = get_current_equinox(datetime.now(timezone.utc))
            # Početak dana: poslednji podne od ekvinoksa + dan*24h
            base_day = eq + timedelta(days=day)
            # Pronađi podne tog dana
            astro_year = AstronomicalYear(eq)
            base_noon = astro_year._last_noon(base_day)
            std_dt = base_noon + timedelta(seconds=milidies * 86.4)
            self.astro_result.config(text=f"Standard: {std_dt.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        except Exception as e:
            self.astro_result.config(text=f"Error: {e}")

    def _milidies_to_time(self):
        try:
            milidies = int(self.milidies_entry.get())
            hm = milidies_to_hm(milidies)
            self.milidies_result.config(text=f"{milidies} miliDies = {hm} (hh:mm:ss)")
            self.time_entry_h.delete(0, tk.END)
            self.time_entry_h.insert(0, hm[:2])
            self.time_entry_m.delete(0, tk.END)
            self.time_entry_m.insert(0, hm[3:5])
        except Exception as e:
            self.milidies_result.config(text=f"Error: {e}")

    def _time_to_milidies(self):
        try:
            h = int(self.time_entry_h.get())
            m = int(self.time_entry_m.get())
            milidies = hm_to_milidies(h, m)
            self.milidies_result.config(text=f"{h:02}:{m:02} = {milidies} miliDies")
            self.milidies_entry.delete(0, tk.END)
            self.milidies_entry.insert(0, str(milidies))
        except Exception as e:
            self.milidies_result.config(text=f"Error: {e}")

    def _update_equinox_countdown(self):
        now = datetime.now(timezone.utc)
        next_eq = get_next_equinox(now)
        if next_eq:
            # Astronomsko vreme: broj Dies i miliDies do sledećeg ekvinoksa
            eq = get_current_equinox(now)
            astro_year = AstronomicalYear(eq)
            astro_year.update(now)
            dies_now = astro_year.day_index
            milidies_now = astro_year.milidan

            astro_year.update(next_eq)
            dies_next = astro_year.day_index
            milidies_next = astro_year.milidan

            dies_diff = dies_next - dies_now
            milidies_diff = milidies_next - milidies_now
            if milidies_diff < 0:
                dies_diff -= 1
                milidies_diff += 1000

            self.astro_equinox_countdown.config(
                text=f"Astronomical: {dies_diff} Dies, {milidies_diff} miliDies"
            )

            # Standardno vreme
            delta = next_eq - now
            days = delta.days
            hours = delta.seconds // 3600
            mins = (delta.seconds % 3600) // 60
            secs = delta.seconds % 60
            self.std_equinox_countdown.config(
                text=f"Standard: {days}d {hours}h {mins}m {secs}s"
            )
        else:
            self.astro_equinox_countdown.config(text="No equinox info")
            self.std_equinox_countdown.config(text="")
        self.after(1000, self._update_equinox_countdown)