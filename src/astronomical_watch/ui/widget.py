import tkinter as tk
from tkinter import ttk
from datetime import datetime, timezone

from src.astronomical_watch.core.astro_time_core import AstronomicalYear, get_current_equinox, get_next_equinox

class AstronomicalWidgetMode:
    def __init__(self, master: tk.Widget = None):
        self.master = master or tk.Tk()
        self.master.title("Astronomical Watch - Widget Mode")
        self.master.geometry("210x140")
        self.master.minsize(160, 120)

        self._firework_shown = False

        self.frame = tk.Frame(self.master, bg='', bd=0)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.title_label = tk.Label(self.frame, text="Astronomical Watch", font=("Arial", 9, "bold"), bg='', bd=0)
        self.title_label.pack(pady=(2, 2))

        self.value_label = tk.Label(self.frame, text="---·---", font=("Arial", 22, "bold"), bg='', bd=0)
        self.value_label.pack(pady=(2, 2))

        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", length=130, mode="determinate", maximum=99, variable=self.progress_var)
        self.progress_bar.pack(pady=(2, 2))

        self.countdown_frame = tk.Frame(self.frame, bg="#d5ffd5", bd=0)
        self.countdown_label = tk.Label(self.countdown_frame, text="", font=("Arial", 10, "bold"), bg="#d5ffd5", fg="#225c17")
        self.countdown_label.pack(padx=4, pady=2)
        self.countdown_frame.pack(fill=tk.X, pady=(6,0))
        self.countdown_frame.pack_forget()

        # Klik/tap na widget otvara normal mod
        self.frame.bind("<Button-1>", self._open_normal_mode)
        self.value_label.bind("<Button-1>", self._open_normal_mode)
        self.progress_bar.bind("<Button-1>", self._open_normal_mode)

        self._update_display()

    def _update_display(self):
        now = datetime.now(timezone.utc)
        eq = get_current_equinox(now)
        astro_year = AstronomicalYear(eq)
        astro_year.update(now)
        dies = astro_year.day_index
        milidies = astro_year.milidan

        self.value_label.config(text=f"{dies}·{milidies}")
        self.progress_var.set(milidies % 100)

        next_eq = get_next_equinox(now)
        if next_eq:
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

            if dies_diff < 11 and dies_diff >= 0:
                if dies_diff == 0:
                    stotinke = milidies_diff % 100
                    centi_str = f".{stotinke:02}"
                    countdown_str = f"{dies_diff}·{milidies_diff}{centi_str}"
                    self.countdown_label.config(
                        text=f"Vernal Equinox in: {countdown_str}",
                        font=("Arial", 10, "bold"),
                        fg="#b02c06" if stotinke == 0 else "#008c00"
                    )
                else:
                    countdown_str = f"{dies_diff}·{milidies_diff}"
                    self.countdown_label.config(
                        text=f"Vernal Equinox in: {countdown_str}",
                        font=("Arial", 10, "bold"),
                        fg="#008c00"
                    )
                self.countdown_frame.pack(fill=tk.X, pady=(6,0))
                if dies_diff == 0 and milidies_diff == 0 and not self._firework_shown:
                    self._firework_shown = True
                    self._fireworks()
            else:
                self.countdown_frame.pack_forget()
                self._firework_shown = False
        else:
            self.countdown_frame.pack_forget()
            self._firework_shown = False

        self.master.after(200, self._update_display)

    def _fireworks(self):
        win = tk.Toplevel(self.master)
        win.title("Vernal Equinox!")
        win.geometry("210x150")
        canvas = tk.Canvas(win, width=210, height=120, bg="black")
        canvas.pack()
        import random
        for _ in range(18):
            x, y = random.randint(30, 180), random.randint(20, 100)
            color = random.choice(["red", "yellow", "lime", "blue", "magenta", "cyan", "orange", "white"])
            r = random.randint(10, 22)
            canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, width=3)
            win.update()
            win.after(80)
        win.after(1800, win.destroy)

    def _open_normal_mode(self, event=None):
        try:
            from ui.normal_mode import AstronomicalNormalMode
            AstronomicalNormalMode(self.master)
        except ImportError:
            pass  # Optionally show error dialog

if __name__ == "__main__":
    app = AstronomicalWidgetMode()
    app.master.mainloop()
