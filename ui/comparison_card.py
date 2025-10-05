from tkinter import Toplevel, Label, Frame, Entry, Button
from datetime import datetime, timezone, timedelta
from core.astro_time_core import get_current_equinox, AstronomicalYear, get_next_equinox
from ui.translations import tr

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
            eq = get_current_equinox(dt)
            astro_year = AstronomicalYear(eq)
            astro_year.update(dt)
            day = astro_year.day_index
            milidies = astro_year.milidan
            self.std_result.config(text=tr("astro_result", self.lang, day=day, milidies=milidies))
        except Exception as e:
            self.std_result.config(text=tr("error_text", self.lang, error=str(e)))

    def _convert_astro_to_std(self):
        try:
            day = int(self.astro_day_entry.get())
            milidies = int(self.astro_milidies_entry.get())
            eq = get_current_equinox(datetime.now(timezone.utc))
            base_day = eq + timedelta(days=day)
            astro_year = AstronomicalYear(eq)
            base_noon = astro_year._last_noon(base_day)
            std_dt = base_noon + timedelta(seconds=milidies * 86.4)
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
        now = datetime.now(timezone.utc)
        next_eq = get_next_equinox(now)
        if next_eq:
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
                text=tr("astro_equinox_countdown_result", self.lang, dies=dies_diff, milidies=milidies_diff)
            )

            delta = next_eq - now
            days = delta.days
            hours = delta.seconds // 3600
            mins = (delta.seconds % 3600) // 60
            secs = delta.seconds % 60
            self.std_equinox_countdown.config(
                text=tr("std_equinox_countdown_result", self.lang, days=days, hours=hours, mins=mins, secs=secs)
            )
        else:
            self.astro_equinox_countdown.config(text=tr("no_equinox_info", self.lang))
            self.std_equinox_countdown.config(text="")
        self.after(1000, self._update_equinox_countdown)
