from tkinter import Toplevel, Label, Frame, Entry, Button
from datetime import datetime, timezone, timedelta
from ..core.astro_time_core import AstroYear
from ..core.equinox import compute_vernal_equinox
from .translations import tr

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

class ComparisonCard(Toplevel):
    def __init__(self, master=None, lang="en"):
        super().__init__(master)
        self.lang = lang
        self.title(f"{tr('comparison', self.lang)} — {tr('title', self.lang)}")
        self.geometry("510x560")
        self.minsize(470, 400)

        self._make_widgets()
        self._update_equinox_countdown()

    def _make_widgets(self):
        font_label = ("Arial", 11)
        font_entry = ("Arial", 11)

        # Standard → Astronomical
        Label(self, text=tr("std_to_astro_label", self.lang), font=font_label).pack(pady=(16, 2))
        frame1 = Frame(self)
        frame1.pack(pady=(0, 4))
        self.std_entry = Entry(frame1, font=font_entry, width=22)
        self.std_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.std_entry.pack(side="left")
        Button(frame1, text=tr("convert_button", self.lang), command=self._convert_std_to_astro).pack(side="left", padx=8)
        self.std_result = Label(self, text="", font=font_label, fg="#2060b0")
        self.std_result.pack()

        # Astronomical → Standard
        Label(self, text=tr("astro_to_std_label", self.lang), font=font_label).pack(pady=(18,2))
        frame2 = Frame(self)
        frame2.pack(pady=(0,4))
        self.astro_day_entry = Entry(frame2, font=font_entry, width=7)
        self.astro_day_entry.insert(0, "0")
        self.astro_day_entry.pack(side="left")
        Label(frame2, text=tr("dies", self.lang), font=font_label).pack(side="left")
        self.astro_milidies_entry = Entry(frame2, font=font_entry, width=7)
        self.astro_milidies_entry.insert(0, "0")
        self.astro_milidies_entry.pack(side="left")
        Label(frame2, text=tr("milidies", self.lang), font=font_label).pack(side="left")
        Button(frame2, text=tr("convert_button", self.lang), command=self._convert_astro_to_std).pack(side="left", padx=8)
        self.astro_result = Label(self, text="", font=font_label, fg="#2060b0")
        self.astro_result.pack()

        # Milidies ↔ hh:mm
        Label(self, text=tr("milidies_hm_label", self.lang), font=font_label).pack(pady=(18,2))
        frame3 = Frame(self)
        frame3.pack(pady=(0,4))
        self.milidies_entry = Entry(frame3, font=font_entry, width=7)
        self.milidies_entry.insert(0, "0")
        self.milidies_entry.pack(side="left")
        Button(frame3, text=tr("to_time_button", self.lang), command=self._milidies_to_time).pack(side="left", padx=4)
        self.time_entry_h = Entry(frame3, font=font_entry, width=3)
        self.time_entry_h.insert(0, "00")
        self.time_entry_h.pack(side="left")
        Label(frame3, text=":", font=font_label).pack(side="left")
        self.time_entry_m = Entry(frame3, font=font_entry, width=3)
        self.time_entry_m.insert(0, "00")
        self.time_entry_m.pack(side="left")
        Button(frame3, text=tr("to_milidies_button", self.lang), command=self._time_to_milidies).pack(side="left", padx=4)
        self.milidies_result = Label(self, text="", font=font_label, fg="#2060b0")
        self.milidies_result.pack()

        # Countdown do sledeće prolećne ravnodnevnice
        Label(self, text=tr("countdown_next_equinox_label", self.lang), font=font_label).pack(pady=(18,2))
        self.astro_equinox_countdown = Label(self, text="", font=font_label, fg="#b02c06")
        self.astro_equinox_countdown.pack()
        self.std_equinox_countdown = Label(self, text="", font=font_label, fg="#b02c06")
        self.std_equinox_countdown.pack()

        Button(self, text=tr("close_button", self.lang), command=self.destroy, font=("Arial", 10), padx=12, pady=5).pack(pady=14)

    def _convert_std_to_astro(self):
        try:
            dt_str = self.std_entry.get().strip()
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            dt = dt.replace(tzinfo=timezone.utc)
            
            # Use precise equinox calculation
            current_year = dt.year
            equinox = compute_vernal_equinox(current_year)
            
            # Check if we need previous or next year's equinox
            if dt < equinox:
                equinox = compute_vernal_equinox(current_year - 1)
            
            astro_year = AstroYear(equinox)
            reading = astro_year.reading(dt)
            dies = reading.dies
            milidies = reading.miliDies
            
            self.std_result.config(text=tr("astro_result", self.lang, day=dies, milidies=milidies))
        except Exception as e:
            self.std_result.config(text=tr("error_text", self.lang, error=str(e)))

    def _convert_astro_to_std(self):
        try:
            day = int(self.astro_day_entry.get())
            milidies = int(self.astro_milidies_entry.get())
            
            # Use current year's equinox
            now = datetime.now(timezone.utc)
            current_year = now.year
            current_equinox = compute_vernal_equinox(current_year)
            
            # Check if we're before this year's equinox
            if now < current_equinox:
                current_equinox = compute_vernal_equinox(current_year - 1)
            
            # Use AstroYear's built-in conversion method for accuracy
            astro_year = AstroYear(current_equinox)
            
            # Special handling for Dies 0 to improve precision
            # Dies 0 miliDies are counted from the last noon before equinox
            if day == 0:
                # Calculate last noon before equinox
                from ..core.astro_time_core import NOON_UTC_HOUR, NOON_UTC_MINUTE, NOON_UTC_SECOND
                eq_date = current_equinox.date()
                noon_candidate = datetime(
                    eq_date.year, eq_date.month, eq_date.day,
                    NOON_UTC_HOUR, NOON_UTC_MINUTE, NOON_UTC_SECOND,
                    tzinfo=timezone.utc
                )
                if noon_candidate > current_equinox:
                    last_noon_before_eq = noon_candidate - timedelta(days=1)
                else:
                    last_noon_before_eq = noon_candidate
                
                # Calculate from that noon
                std_dt = last_noon_before_eq + timedelta(seconds=milidies * 86.4)
            else:
                # For Dies >= 1, use AstroYear's method
                std_dt = astro_year.approximate_utc_from_day_miliDies(day, milidies)
            
            self.astro_result.config(
                text=tr("std_result", self.lang, std_time=std_dt.strftime('%Y-%m-%d %H:%M:%S'))
            )
        except Exception as e:
            self.astro_result.config(text=tr("error_text", self.lang, error=str(e)))

    def _milidies_to_time(self):
        try:
            milidies = int(self.milidies_entry.get())
            hm = milidies_to_hm(milidies)
            self.milidies_result.config(text=tr("milidies_to_time_result", self.lang, milidies=milidies, hm=hm))
            self.time_entry_h.delete(0, "end")
            self.time_entry_h.insert(0, hm[:2])
            self.time_entry_m.delete(0, "end")
            self.time_entry_m.insert(0, hm[3:5])
        except Exception as e:
            self.milidies_result.config(text=tr("error_text", self.lang, error=str(e)))

    def _time_to_milidies(self):
        try:
            h = int(self.time_entry_h.get())
            m = int(self.time_entry_m.get())
            milidies = hm_to_milidies(h, m)
            self.milidies_result.config(text=tr("time_to_milidies_result", self.lang, h=h, m=m, milidies=milidies))
            self.milidies_entry.delete(0, "end")
            self.milidies_entry.insert(0, str(milidies))
        except Exception as e:
            self.milidies_result.config(text=tr("error_text", self.lang, error=str(e)))

    def _update_equinox_countdown(self):
        try:
            now = datetime.now(timezone.utc)
            
            # Use precise equinox calculation
            current_year = now.year
            current_equinox = compute_vernal_equinox(current_year)
            next_equinox = compute_vernal_equinox(current_year + 1)
            
            # Check if we're before this year's equinox
            if now < current_equinox:
                current_equinox = compute_vernal_equinox(current_year - 1)
                next_equinox = compute_vernal_equinox(current_year)
            
            # Get current astronomical time
            astro_year = AstroYear(current_equinox)
            current_reading = astro_year.reading(now)
            
            # Calculate time until next equinox
            delta = next_equinox - now
            if delta.total_seconds() > 0:
                days = delta.days
                hours = delta.seconds // 3600
                mins = (delta.seconds % 3600) // 60
                secs = delta.seconds % 60
                
                # Calculate remaining astronomical time in current year
                year_length_seconds = (next_equinox - current_equinox).total_seconds()
                year_length_dies = year_length_seconds / 86400.0  # Precise Dies calculation
                
                remaining_dies = int(year_length_dies) - current_reading.dies
                remaining_milidies = 1000 - current_reading.miliDies
                
                # Adjust if we're at exact boundary
                if remaining_milidies == 1000:
                    remaining_milidies = 0
                    remaining_dies += 1
                
                self.astro_equinox_countdown.config(
                    text=tr("astro_equinox_countdown_result", self.lang, dies=remaining_dies, milidies=remaining_milidies)
                )
                
                self.std_equinox_countdown.config(
                    text=tr("std_equinox_countdown_result", self.lang, days=days, hours=hours, mins=mins, secs=secs)
                )
            else:
                self.astro_equinox_countdown.config(text=tr("equinox_passed", self.lang))
                self.std_equinox_countdown.config(text="")
                
        except Exception as e:
            self.astro_equinox_countdown.config(text=tr("error_text", self.lang, error=str(e)))
            self.std_equinox_countdown.config(text="")
            
        self.after(1000, self._update_equinox_countdown)

def create_comparison_card(master=None, lang="en"):
    """Factory function to create ComparisonCard instance."""
    return ComparisonCard(master, lang)
