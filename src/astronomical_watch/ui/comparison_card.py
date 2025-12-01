from tkinter import Toplevel, Label, Frame, Entry, Button
from datetime import datetime, timezone, timedelta
import time
import calendar as cal_module
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
        self.geometry("600x850")
        self.minsize(580, 820)
        
        # Configure window to only show close button (disable minimize/maximize)
        self.resizable(False, False)

        # Detect system timezone
        self.local_tz = datetime.now().astimezone().tzinfo
        self.tz_name = self._get_timezone_name()
        
        # Conversion state tracking
        self.active_field = None  # 'milidies' or 'time'
        
        # Calendar state
        self.current_cal_month = datetime.now().month
        self.current_cal_year = datetime.now().year
        
        self._make_widgets()
    
    def _get_timezone_name(self):
        """Get full timezone name from system"""
        try:
            # Try to get IANA timezone name from TZ environment
            import os
            if 'TZ' in os.environ and os.environ['TZ']:
                return os.environ['TZ']
            
            # Fallback to UTC offset format
            now = datetime.now()
            local = now.astimezone()
            offset = local.strftime('%z')
            # Format: UTC+01:00
            if offset:
                sign = '+' if offset[0] == '+' else '-'
                hours = offset[1:3]
                minutes = offset[3:5]
                return f"UTC{sign}{hours}:{minutes}"
            return "UTC+00:00"
        except:
            return "UTC+00:00"

    def _prev_month(self):
        """Navigate to previous month"""
        self.current_cal_month -= 1
        if self.current_cal_month < 1:
            self.current_cal_month = 12
            self.current_cal_year -= 1
        self._update_calendar()
    
    def _next_month(self):
        """Navigate to next month"""
        self.current_cal_month += 1
        if self.current_cal_month > 12:
            self.current_cal_month = 1
            self.current_cal_year += 1
        self._update_calendar()
    
    def _update_calendar(self):
        """Update calendar display with Dies for each day - read-only"""
        # Clear existing calendar
        for widget in self.calendar_grid.winfo_children():
            widget.destroy()
        
        # Update month/year label
        month_names = {
            "en": ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"],
            "sr": ["Januar", "Februar", "Mart", "April", "Maj", "Jun",
                   "Jul", "Avgust", "Septembar", "Oktobar", "Novembar", "Decembar"]
        }
        lang_months = month_names.get(self.lang, month_names["en"])
        self.month_year_label.config(text=f"{lang_months[self.current_cal_month-1]} {self.current_cal_year}")
        
        # Day headers
        day_names = {
            "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "sr": ["Pon", "Uto", "Sre", "Čet", "Pet", "Sub", "Ned"]
        }
        lang_days = day_names.get(self.lang, day_names["en"])
        
        for i, day_name in enumerate(lang_days):
            Label(self.calendar_grid, text=day_name, font=("Arial", 9, "bold"), 
                  bg="#d0d0d0", width=7, height=1).grid(row=0, column=i, padx=1, pady=1, sticky="nsew")
        
        # Get calendar for month
        cal = cal_module.monthcalendar(self.current_cal_year, self.current_cal_month)
        
        # Create labels for each day (read-only, no interaction)
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell
                    Label(self.calendar_grid, text="", bg="#f8f9fa", width=7, height=3).grid(
                        row=week_num+1, column=day_num, padx=1, pady=1, sticky="nsew")
                else:
                    # Calculate Dies for this day (at noon)
                    try:
                        day_dt = datetime(self.current_cal_year, self.current_cal_month, day, 12, 0, tzinfo=timezone.utc)
                        
                        # Get correct equinox for THIS SPECIFIC DAY
                        equinox = compute_vernal_equinox(self.current_cal_year)
                        if day_dt < equinox:
                            equinox = compute_vernal_equinox(self.current_cal_year - 1)
                        
                        astro_year = AstroYear(equinox)
                        reading = astro_year.reading(day_dt)
                        dies = reading.dies
                        
                        # Create label with day (black) and Dies (blue)
                        day_frame = Frame(self.calendar_grid, bg="#ffffff", relief="solid", borderwidth=1)
                        day_frame.grid(row=week_num+1, column=day_num, padx=1, pady=1, sticky="nsew")
                        
                        # Standard calendar day - black, larger
                        Label(day_frame, text=f"{day}", font=("Arial", 14, "bold"), 
                              bg="#ffffff", fg="#000000").pack(expand=True)
                        
                        # Dies number - blue, larger  
                        Label(day_frame, text=f"{dies:03d}", font=("Arial", 12), 
                              bg="#ffffff", fg="#1565c0").pack(expand=True)
                        
                        # Highlight today with light background
                        today = datetime.now()
                        if (day == today.day and self.current_cal_month == today.month 
                            and self.current_cal_year == today.year):
                            day_frame.config(bg="#fff3e0")
                            for child in day_frame.winfo_children():
                                child.config(bg="#fff3e0")
                            
                    except Exception as e:
                        # Fallback for errors
                        Label(self.calendar_grid, text=f"{day}\n---", font=("Arial", 10),
                              bg="#ffcccc", width=7, height=3).grid(row=week_num+1, column=day_num, 
                                                                     padx=1, pady=1, sticky="nsew")
    
    def _select_date(self, day, dies):
        """Handle date selection from calendar"""
        self.selected_date = datetime(self.current_cal_year, self.current_cal_month, day, 12, 0)
        
        # Display selected date
        date_str = self.selected_date.strftime("%Y-%m-%d")
        self.selected_date_label.config(
            text=f"{tr('selected_date', self.lang)}: {date_str}"
        )
        
        # Automatically show astronomical time for selected date
        dt_local = self.selected_date.replace(tzinfo=self.local_tz)
        dt_utc = dt_local.astimezone(timezone.utc)
        
        # Get correct equinox for THIS SPECIFIC DATE
        equinox = compute_vernal_equinox(self.current_cal_year)
        if dt_utc < equinox:
            equinox = compute_vernal_equinox(self.current_cal_year - 1)
        
        astro_year = AstroYear(equinox)
        reading = astro_year.reading(dt_utc)
        
        self.std_result.config(
            text=tr("astro_result", self.lang, day=reading.dies, milidies=reading.miliDies)
        )

    def _make_widgets(self):
        font_label = ("Arial", 11)
        font_entry = ("Arial", 11)
        font_info = ("Arial", 10, "italic")
        
        # Timezone information at the top
        tz_frame = Frame(self, bg="#e8f4f8", relief="solid", borderwidth=1)
        tz_frame.pack(pady=(12, 8), padx=12, fill="x")
        
        tz_label = Label(
            tz_frame, 
            text=f"⏰ {tr('timezone_label', self.lang)}: {self.tz_name}",
            font=("Arial", 11, "bold"),
            bg="#e8f4f8",
            fg="#1a5490"
        )
        tz_label.pack(pady=6)
        
        tz_note = Label(
            tz_frame,
            text=tr('timezone_note', self.lang),
            font=font_info,
            bg="#e8f4f8",
            fg="#555555"
        )
        tz_note.pack(pady=(0, 6))

        # Calendar Widget - Read-only display with Dies
        Label(self, text=tr("calendar_select_label", self.lang), font=("Arial", 11, "bold")).pack(pady=(12, 6))
        
        # Calendar frame
        self.calendar_frame = Frame(self, relief="solid", borderwidth=1, bg="#f8f9fa")
        self.calendar_frame.pack(pady=(0, 8), padx=12, fill="x")
        
        # Month/Year selector
        month_frame = Frame(self.calendar_frame, bg="#f8f9fa")
        month_frame.pack(pady=6)
        
        Button(month_frame, text="◀", command=self._prev_month, font=("Arial", 9), width=3).pack(side="left", padx=2)
        self.month_year_label = Label(month_frame, text="", font=("Arial", 10, "bold"), bg="#f8f9fa", width=18)
        self.month_year_label.pack(side="left", padx=4)
        Button(month_frame, text="▶", command=self._next_month, font=("Arial", 9), width=3).pack(side="left", padx=2)
        
        # Calendar grid
        self.calendar_grid = Frame(self.calendar_frame, bg="#f8f9fa")
        self.calendar_grid.pack(pady=(0, 6), padx=4)
        
        # Initialize calendar
        self._update_calendar()

        # MiliDies Time Table - 2 rows x 5 columns grid layout
        Label(self, text=tr("milidies_time_table_label", self.lang), font=("Arial", 11, "bold")).pack(pady=(18, 8))
        
        # Grid container
        grid_frame = Frame(self, bg="#f8f9fa")
        grid_frame.pack(pady=(0, 12), padx=12)
        
        # Create 2 rows x 5 columns grid
        for row in range(2):
            for col in range(5):
                index = row * 5 + col
                if index >= 10:
                    break
                
                milidies_value = index * 100
                
                # Calculate actual local time using AstroYear with regular Dies (not Dies 0)
                # Use Dies 100 to get standard reference noon timing
                try:
                    test_dt = self.astro_year.approximate_utc_from_day_miliDies(100, milidies_value)
                    local_dt = test_dt.astimezone()
                    time_str = local_dt.strftime("%H:%M")
                except:
                    # Fallback - reference noon is 23:15:54 UTC = 00:15:54 local (Belgrade)
                    # Round to 00:16 for display
                    base_minutes = 16  # 00:16 local start
                    total_minutes = base_minutes + (milidies_value * 1.44)
                    hours = int(total_minutes // 60) % 24
                    minutes = int(total_minutes % 60)
                    time_str = f"{hours:02d}:{minutes:02d}"
                
                # Cell frame with border - smaller dimensions
                cell_frame = Frame(grid_frame, bg='#f0f0f0', relief="solid", borderwidth=1,
                                  width=95, height=55)
                cell_frame.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
                cell_frame.pack_propagate(False)
                
                # MiliDies value (blue, top)
                milidies_label = Label(
                    cell_frame, 
                    text=f"{milidies_value:03d}",
                    font=('Arial', 14, 'bold'),
                    fg='#0066cc',  # Blue
                    bg='#f0f0f0'
                )
                milidies_label.pack(pady=(6, 0))
                
                # Time value (black, bottom)
                time_label = Label(
                    cell_frame,
                    text=time_str,
                    font=('Arial', 11),
                    fg='#000000',  # Black
                    bg='#f0f0f0'
                )
                time_label.pack(pady=(1, 6))

        # Conversion tool
        Label(self, text=tr("converter_label", self.lang), font=("Arial", 12, "bold")).pack(pady=(20, 10))
        
        converter_frame = Frame(self, bg="#f8f9fa", relief="solid", borderwidth=2)
        converter_frame.pack(pady=(0, 15), padx=15, fill="x")
        
        # Inner frame for better layout with more vertical space
        inner_frame = Frame(converter_frame, bg="#f8f9fa")
        inner_frame.pack(pady=20, padx=15, fill="x")
        
        # Left: MiliDies input
        left_frame = Frame(inner_frame, bg="#f8f9fa")
        left_frame.pack(side="left", padx=(0, 20))
        Label(left_frame, text="MiliDies:", font=("Arial", 11, "bold"), bg="#f8f9fa").pack(pady=(0, 8))
        self.milidies_entry = Entry(left_frame, width=5, font=("Arial", 20, "bold"), justify="center")
        self.milidies_entry.config(highlightthickness=3, highlightbackground="#0066cc", relief="solid", bd=2)
        self.milidies_entry.pack(ipady=18)
        self.milidies_entry.bind('<KeyRelease>', self._validate_milidies)
        self.milidies_entry.bind('<Button-1>', lambda e: self._on_field_click('milidies'))
        self.milidies_entry.bind('<KeyPress>', self._handle_keypress)
        
        # Middle: Convert button
        middle_frame = Frame(inner_frame, bg="#f8f9fa")
        middle_frame.pack(side="left", padx=20)
        Label(middle_frame, text="", font=("Arial", 10), bg="#f8f9fa").pack()  # Spacer for alignment
        Button(middle_frame, text=tr("convert_button", self.lang), 
               command=self._convert_bidirectional,
               font=("Arial", 12, "bold"), padx=30, pady=22).pack()
        
        # Right: Hours and Minutes inputs
        right_frame = Frame(inner_frame, bg="#f8f9fa")
        right_frame.pack(side="left", padx=(20, 0))
        Label(right_frame, text="HH:MM:", font=("Arial", 11, "bold"), bg="#f8f9fa").pack(pady=(0, 8))
        
        time_input_frame = Frame(right_frame, bg="#f8f9fa")
        time_input_frame.pack()
        
        self.hours_entry = Entry(time_input_frame, width=3, font=("Arial", 20, "bold"), justify="center")
        self.hours_entry.config(highlightthickness=3, highlightbackground="#0066cc", relief="solid", bd=2)
        self.hours_entry.pack(side="left", ipady=18)
        self.hours_entry.bind('<KeyRelease>', self._validate_hours_and_move)
        self.hours_entry.bind('<Button-1>', lambda e: self._on_field_click('time'))
        self.hours_entry.bind('<KeyPress>', self._handle_keypress)
        
        Label(time_input_frame, text=":", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(side="left", padx=6)
        
        self.minutes_entry = Entry(time_input_frame, width=3, font=("Arial", 20, "bold"), justify="center")
        self.minutes_entry.config(highlightthickness=3, highlightbackground="#0066cc", relief="solid", bd=2)
        self.minutes_entry.pack(side="left", ipady=18)
        self.minutes_entry.bind('<KeyRelease>', self._validate_minutes)
        self.minutes_entry.bind('<Button-1>', lambda e: self._on_field_click('time'))
        self.minutes_entry.bind('<KeyPress>', self._handle_keypress)
        
        # Result/error message
        self.converter_result = Label(converter_frame, text="", font=("Arial", 10), 
                                     bg="#f8f9fa", fg="#666666")
        self.converter_result.pack(pady=(5, 12))

    def _handle_keypress(self, event):
        """Handle keypress - block input to inactive fields and handle numpad"""
        widget = event.widget
        
        # Check if this widget is allowed to receive input
        if self.active_field == 'milidies' and widget in (self.hours_entry, self.minutes_entry):
            return 'break'  # Block input to time fields
        elif self.active_field == 'time' and widget == self.milidies_entry:
            return 'break'  # Block input to miliDies field
        
        # Map numpad keys to regular digit keys
        numpad_map = {
            'KP_0': '0', 'KP_1': '1', 'KP_2': '2', 'KP_3': '3', 'KP_4': '4',
            'KP_5': '5', 'KP_6': '6', 'KP_7': '7', 'KP_8': '8', 'KP_9': '9'
        }
        
        if event.keysym in numpad_map:
            # Insert the digit and prevent default behavior
            widget.insert('insert', numpad_map[event.keysym])
            return 'break'  # Prevent default handling
    
    def _on_field_click(self, field_type):
        """Handle click on a field - clear all and set active field"""
        # Clear all fields
        self.milidies_entry.delete(0, 'end')
        self.hours_entry.delete(0, 'end')
        self.minutes_entry.delete(0, 'end')
        self.converter_result.config(text="")
        
        # Set active field
        self.active_field = field_type
    
    def _clear_all_fields(self, event=None):
        """Clear all input fields when user clicks on any field after a conversion"""
        # Only clear if there's a result showing (conversion was done)
        if self.converter_result.cget('text'):
            self.milidies_entry.delete(0, 'end')
            self.hours_entry.delete(0, 'end')
            self.minutes_entry.delete(0, 'end')
            self.converter_result.config(text="")
    
    def _validate_milidies(self, event=None):
        """Allow only 3-digit numbers in miliDies field"""
        text = self.milidies_entry.get()
        # Remove non-digit characters
        cleaned = ''.join(c for c in text if c.isdigit())
        # Limit to 3 digits
        if len(cleaned) > 3:
            cleaned = cleaned[:3]
        if text != cleaned:
            self.milidies_entry.delete(0, 'end')
            self.milidies_entry.insert(0, cleaned)
    
    def _validate_hours(self, event=None):
        """Allow only 2-digit numbers (00-23) in hours field"""
        text = self.hours_entry.get()
        cleaned = ''.join(c for c in text if c.isdigit())
        if len(cleaned) > 2:
            cleaned = cleaned[:2]
        if cleaned and int(cleaned) > 23:
            cleaned = '23'
        if text != cleaned:
            self.hours_entry.delete(0, 'end')
            self.hours_entry.insert(0, cleaned)
    
    def _validate_hours_and_move(self, event=None):
        """Validate hours and auto-move to minutes after 2 digits"""
        self._validate_hours(event)
        text = self.hours_entry.get()
        if len(text) == 2:
            # Move focus to minutes field
            self.minutes_entry.focus_set()
    
    def _validate_minutes(self, event=None):
        """Allow only 2-digit numbers (00-59) in minutes field"""
        text = self.minutes_entry.get()
        cleaned = ''.join(c for c in text if c.isdigit())
        if len(cleaned) > 2:
            cleaned = cleaned[:2]
        if cleaned and int(cleaned) > 59:
            cleaned = '59'
        if text != cleaned:
            self.minutes_entry.delete(0, 'end')
            self.minutes_entry.insert(0, cleaned)
    
    def _convert_bidirectional(self):
        """Convert between miliDies and HH:MM based on which field has input"""
        milidies_text = self.milidies_entry.get().strip()
        hours_text = self.hours_entry.get().strip()
        minutes_text = self.minutes_entry.get().strip()
        
        try:
            # If miliDies has input, convert to time
            if milidies_text:
                milidies = int(milidies_text)
                if milidies > 999:
                    self.converter_result.config(text="MiliDies mora biti 0-999", fg="#d32f2f")
                    return
                
                # Use AstroYear to get accurate time based on timezone
                try:
                    test_dt = self.astro_year.approximate_utc_from_day_miliDies(100, milidies)
                    local_dt = test_dt.astimezone()
                    hours = local_dt.hour
                    minutes = local_dt.minute
                except:
                    # Fallback calculation
                    total_minutes = 16 + (milidies * 1.44)  # Start at 00:16 local
                    hours = int(total_minutes // 60) % 24
                    minutes = int(total_minutes % 60)
                
                self.hours_entry.delete(0, 'end')
                self.hours_entry.insert(0, f"{hours:02d}")
                self.minutes_entry.delete(0, 'end')
                self.minutes_entry.insert(0, f"{minutes:02d}")
                self.converter_result.config(text=f"{milidies:03d} mD = {hours:02d}:{minutes:02d} ({self.tz_name})", fg="#2e7d32")
                
            # If time has input, convert to miliDies
            elif hours_text and minutes_text:
                hours = int(hours_text)
                minutes = int(minutes_text)
                
                if hours > 23 or minutes > 59:
                    self.converter_result.config(text="Vreme mora biti HH (0-23) : MM (0-59)", fg="#d32f2f")
                    return
                
                # Calculate miliDies from local time
                # Local Dies starts at 00:15:54 (round to 00:16)
                # Convert input time to minutes from Dies start
                input_minutes = hours * 60 + minutes
                dies_start_minutes = 0 * 60 + 16  # 00:16
                
                # Handle day wrap
                if input_minutes < dies_start_minutes:
                    input_minutes += 24 * 60  # Add 24 hours
                
                minutes_from_start = input_minutes - dies_start_minutes
                milidies = int(round(minutes_from_start / 1.44))
                
                # Clamp to 0-999
                if milidies < 0:
                    milidies = 0
                if milidies > 999:
                    milidies = 999
                
                self.milidies_entry.delete(0, 'end')
                self.milidies_entry.insert(0, f"{milidies:03d}")
                self.converter_result.config(text=f"{hours:02d}:{minutes:02d} = {milidies:03d} mD ({self.tz_name})", fg="#2e7d32")
            else:
                self.converter_result.config(text="Unesite miliDies ILI sate i minute", fg="#ff6f00")
                
        except Exception as e:
            self.converter_result.config(text=f"Greška: {str(e)}", fg="#d32f2f")


def create_comparison_card(master=None, lang="en"):
    """Factory function to create ComparisonCard instance."""
    return ComparisonCard(master, lang)
