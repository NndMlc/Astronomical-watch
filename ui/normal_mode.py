import tkinter as tk
from tkinter import ttk
from datetime import datetime, timezone

from core.astro_time_core import AstronomicalYear, get_current_equinox
from ui.gradient import get_sky_theme
from ui.explanation_card import EXPLANATION_TEXT
from ui.comparison_card import ComparisonCard
from ui.calculation_card import CalculationCard

LANGUAGES = [
    ("English", "en"), ("Spanish", "es"), ("Chinese", "zh"),
    ("Arabic", "ar"), ("Portuguese", "pt"), ("French", "fr"),
    ("German", "de"), ("Russian", "ru"), ("Japanese", "ja"),
    ("Hindi", "hi"), ("Iranian", "fa"), ("Bahasa", "id"),
    ("Swahili", "sw"), ("Hausa", "ha"), ("Turkish", "tr"),
    ("Greek", "el"), ("Serbian", "sr"), ("Polish", "pl"),
    ("Italian", "it"), ("Dutch", "nl")
]

class AstronomicalNormalMode:
    def __init__(self, master: tk.Widget = None, on_back=None, on_language=None):
        self.master = master or tk.Tk()
        self.master.title("Astronomical Watch - Normal Mode")
        self.master.geometry("370x320")
        self.master.minsize(340, 270)

        now = datetime.now(timezone.utc)
        self.current_equinox = get_current_equinox(now)
        self.astro_year = AstronomicalYear(self.current_equinox)
        self.astro_year.update(now)

        # Canvas za gradient pozadinu
        self.bg_canvas = tk.Canvas(self.master, highlightthickness=0, bd=0)
        self.bg_canvas.pack(fill=tk.BOTH, expand=True)
        self.bg_canvas.bind('<Configure>', self._on_canvas_configure)

        # Glavni okvir na canvasu
        self.frame = tk.Frame(self.bg_canvas, bg='', bd=0)
        self.canvas_window = self.bg_canvas.create_window(0, 0, anchor=tk.NW, window=self.frame)

        # Gornji levi ugao: povratak na Widget Mode
        self.back_btn = tk.Button(self.bg_canvas, text="⟵", font=("Arial", 12), command=self._back, bd=0, relief=tk.FLAT, bg="#e6e6e6", activebackground="#d6d6d6")
        self.bg_canvas.create_window(10, 10, anchor=tk.NW, window=self.back_btn, tags="nav_back")

        # Gornji desni ugao: izbor jezika
        self.lang_btn = tk.Button(self.bg_canvas, text="🌐", font=("Arial", 12), command=self._show_language_menu, bd=0, relief=tk.FLAT, bg="#e6e6e6", activebackground="#d6d6d6")
        self.bg_canvas.create_window(0, 10, anchor=tk.NE, window=self.lang_btn, tags="nav_lang")

        # Naslov malim fontom
        self.title_label = tk.Label(self.frame, text="Astronomical Watch", font=("Arial", 10, "bold"), bg='', bd=0)
        self.title_label.pack(pady=(24, 10))

        # Dies i miliDies
        self.dies_label = tk.Label(self.frame, text="Dies", font=("Arial", 10), bg='', bd=0)
        self.dies_label.pack()
        self.day_value_label = tk.Label(self.frame, text="---", font=("Arial", 26, "bold"), bg='', bd=0)
        self.day_value_label.pack(pady=(0, 10))
        self.milidies_label = tk.Label(self.frame, text="miliDies", font=("Arial", 10), bg='', bd=0)
        self.milidies_label.pack()
        self.milidies_value_label = tk.Label(self.frame, text="---", font=("Arial", 26, "bold"), bg='', bd=0)
        self.milidies_value_label.pack(pady=(0, 12))

        # Progres bar
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", length=220, mode="determinate", maximum=99, variable=self.progress_var)
        self.progress_bar.pack(pady=(0, 2))

        # Standardno vreme ispod progres bara
        self.clock_label = tk.Label(self.frame, text="", font=("Arial", 10), bg='', bd=0)
        self.clock_label.pack(pady=(5, 12))

        # Dugmad za otvaranje kartica
        self.btn_frame = tk.Frame(self.frame, bg="", bd=0)
        self.btn_frame.pack(pady=(0, 10))
        self.explanation_btn = tk.Button(self.btn_frame, text="Explanation", font=("Arial", 10), width=12, bd=0, relief=tk.RAISED, command=self._show_explanation)
        self.comparison_btn = tk.Button(self.btn_frame, text="Comparison", font=("Arial", 10), width=12, bd=0, relief=tk.RAISED, command=self._show_comparison)
        self.calculations_btn = tk.Button(self.btn_frame, text="Calculations", font=("Arial", 10), width=12, bd=0, relief=tk.RAISED, command=self._show_calculations)
        self.explanation_btn.pack(side=tk.LEFT, padx=2)
        self.comparison_btn.pack(side=tk.LEFT, padx=2)
        self.calculations_btn.pack(side=tk.LEFT, padx=2)

        self.on_back = on_back
        self.on_language = on_language
        self.language_menu = None
        self.selected_language = LANGUAGES[0][1]  # default 'en'

        self._update_display()

    def _on_canvas_configure(self, event):
        self._draw_gradient()
        w = self.bg_canvas.winfo_width()
        self.bg_canvas.coords("nav_lang", w-10, 10)

    def _draw_gradient(self):
        theme = get_sky_theme(datetime.now(timezone.utc))
        w = self.bg_canvas.winfo_width()
        h = self.bg_canvas.winfo_height()
        if w < 1 or h < 1: return
        self.bg_canvas.delete("gradient")
        steps = 64
        for i in range(steps):
            r = i / (steps - 1)
            color = self._interpolate_color(theme.top_color, theme.bottom_color, r)
            y0 = int(h * (i / steps))
            y1 = int(h * ((i+1) / steps))
            self.bg_canvas.create_rectangle(0, y0, w, y1, fill=color, outline="", tags="gradient")
        self.bg_canvas.tag_raise(self.canvas_window)
        self.bg_canvas.tag_raise("nav_back")
        self.bg_canvas.tag_raise("nav_lang")

    def _interpolate_color(self, c1, c2, r):
        def hex_to_rgb(h): return tuple(int(h[i:i+2], 16) for i in (1,3,5))
        def rgb_to_hex(rgb): return "#%02x%02x%02x" % rgb
        rgb1 = hex_to_rgb(c1)
        rgb2 = hex_to_rgb(c2)
        rgb = tuple(int(a + (b-a)*r) for a,b in zip(rgb1, rgb2))
        return rgb_to_hex(rgb)

    def _update_display(self):
        now = datetime.now(timezone.utc)
        new_equinox = get_current_equinox(now)
        if new_equinox != self.current_equinox:
            self.current_equinox = new_equinox
            self.astro_year = AstronomicalYear(self.current_equinox)
        self.astro_year.update(now)
        day = self.astro_year.day_index
        milidies = self.astro_year.milidan
        self.day_value_label.config(text=f"{day}")
        self.milidies_value_label.config(text=f"{milidies}")
        self.progress_var.set(milidies % 100)
        # Standardno vreme
        local_now = datetime.now()
        self.clock_label.config(text=local_now.strftime("%H:%M %m/%d"))
        self._draw_gradient()
        self.master.after(200, self._update_display)

    def _show_language_menu(self):
        if self.language_menu is not None:
            self.language_menu.destroy()
            self.language_menu = None
            return
        self.language_menu = tk.Toplevel(self.master)
        self.language_menu.title("Choose language")
        self.language_menu.geometry("+{}+{}".format(self.master.winfo_x()+self.master.winfo_width()-180, self.master.winfo_y()+40))
        self.language_menu.resizable(False,False)
        tk.Label(self.language_menu, text="Select language:", font=("Arial", 10, "bold")).pack(pady=(8, 4))
        for name, code in LANGUAGES:
            btn = tk.Button(self.language_menu, text=name, font=("Arial", 10), width=20,
                            command=lambda c=code: self._select_language(c))
            btn.pack(pady=1)
        self.language_menu.transient(self.master)
        self.language_menu.grab_set()
        self.language_menu.protocol("WM_DELETE_WINDOW", self._close_language_menu)

    def _close_language_menu(self):
        if self.language_menu is not None:
            self.language_menu.destroy()
            self.language_menu = None

    def _select_language(self, code):
        self.selected_language = code
        self._close_language_menu()
        if self.on_language:
            self.on_language(code)

    def _back(self):
        if self.on_back:
            self.on_back()

    # Dugmad za kartice:
    def _show_explanation(self):
        win = tk.Toplevel(self.master)
        win.title("Explanation — Astronomical Watch")
        win.geometry("480x600")
        frame = tk.Frame(win)
        frame.pack(fill=tk.BOTH, expand=True)
        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 11), padx=12, pady=14, bg="#f8f8fa")
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, EXPLANATION_TEXT)
        text_widget.config(state=tk.DISABLED)
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        tk.Button(win, text="Close", command=win.destroy, font=("Arial", 10), padx=12, pady=5).pack(pady=8)

    def _show_comparison(self):
        ComparisonCard(self.master)

    def _show_calculations(self):
        CalculationCard(self.master)

def create_normal_mode(master: tk.Widget = None, on_back=None, on_language=None) -> AstronomicalNormalMode:
    return AstronomicalNormalMode(master, on_back=on_back, on_language=on_language)

if __name__ == "__main__":
    app = AstronomicalNormalMode()
    app.master.mainloop()