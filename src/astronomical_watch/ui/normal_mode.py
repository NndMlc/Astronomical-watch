"""
Astronomical Watch Normal Mode - Full window detailed display
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timezone
from typing import Optional
import json
import os
from .gradient import get_sky_theme
from .translations import TRANSLATIONS

from src.astronomical_watch.core.astro_time_core import AstroYear

# Simple language list for language menu - all 20 languages from translations.py
LANGUAGES = [
    ("English", "en"),
    ("Српски (Serbian)", "sr"),
    ("Español", "es"),
    ("中文 (Chinese)", "zh"),
    ("العربية (Arabic)", "ar"),
    ("Português", "pt"),
    ("Français", "fr"),
    ("Deutsch", "de"),
    ("Русский (Russian)", "ru"),
    ("日本語 (Japanese)", "ja"),
    ("हिन्दी (Hindi)", "hi"),
    ("فارسی (Persian)", "fa"),
    ("Bahasa Indonesia", "id"),
    ("Kiswahili", "sw"),
    ("Hausa", "ha"),
    ("Türkçe", "tr"),
    ("Ελληνικά (Greek)", "el"),
    ("Polski", "pl"),
    ("Italiano", "it"),
    ("Nederlands", "nl")
]

def tr(key: str, lang: str = "en") -> str:
    """Simple translation function."""
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS.get("en", {}).get(key, key))

SETTINGS_FILE = "astronomical_watch_settings.json"

def load_language():
    """Load saved language preference."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                return settings.get("language", "en")
        except:
            return "en"
    return "en"

def save_language(lang_code):
    """Save language preference."""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"language": lang_code}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Error saving language:", e)

class AstronomicalNormalMode:
    def __init__(self, master: tk.Widget = None, on_back=None, on_language=None):
        self.master = master or tk.Tk()
        self.master.title("Astronomical Watch - Normal Mode")
        self.master.geometry("800x600")
        self.on_back = on_back
        self.on_language = on_language
        
        # Current language
        self.current_language = load_language()
        
        # Current astronomical time values
        self.current_time = None
        self.day_index = 0
        self.milliDies = 0
        self.progress_percent = 0.0
        
        # Update job reference
        self.update_job = None
        
        self._create_widgets()
        self._apply_theme()
        
    def _create_widgets(self):
        """Create the main UI elements."""
        # Main frame
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text=tr("title", self.current_language),
            font=("Arial", 24, "bold"),
            fg="white"
        )
        self.title_label.pack(pady=(0, 20))
        
        # Current time display
        self.time_frame = tk.Frame(self.main_frame)
        self.time_frame.pack(pady=20)
        
        self.time_label = tk.Label(
            self.time_frame,
            text="000·000",
            font=("Courier New", 48, "bold"),
            fg="white"
        )
        self.time_label.pack()
        
        # Progress bar
        self.progress_frame = tk.Frame(self.main_frame)
        self.progress_frame.pack(pady=20, fill="x")
        
        tk.Label(
            self.progress_frame,
            text=tr("progress_through_day", self.current_language),
            font=("Arial", 12),
            fg="white"
        ).pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=5)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="0.0%",
            font=("Arial", 10),
            fg="white"
        )
        self.progress_label.pack()
        
        # Information section
        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.pack(pady=20, fill="x")
        
        self.info_text = tk.Text(
            self.info_frame,
            height=8,
            font=("Arial", 10),
            bg="rgba(255,255,255,0.1)",
            fg="white",
            wrap="word"
        )
        self.info_text.pack(fill="x")
        
        # Controls frame
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(pady=20, fill="x")
        
        # Language selector
        tk.Label(
            self.controls_frame,
            text=tr("language", self.current_language),
            font=("Arial", 12),
            fg="white"
        ).pack(side="left")
        
        self.language_var = tk.StringVar(value=self.current_language)
        self.language_combo = ttk.Combobox(
            self.controls_frame,
            textvariable=self.language_var,
            values=[code for _, code in LANGUAGES],
            state="readonly",
            width=8
        )
        self.language_combo.pack(side="left", padx=(5, 20))
        self.language_combo.bind('<<ComboboxSelected>>', self._on_language_change)
        
        # Explanation button
        self.explanation_button = tk.Button(
            self.controls_frame,
            text=tr("explanation", self.current_language),
            command=self._show_explanation,
            font=("Arial", 12),
            bg="#2d5a87",
            fg="white",
            relief="flat",
            padx=20
        )
        self.explanation_button.pack(side="left", padx=(0, 10))
        
        # Close button
        self.close_button = tk.Button(
            self.controls_frame,
            text=tr("close", self.current_language),
            command=self.master.destroy,
            font=("Arial", 12),
            bg="#4a5568",
            fg="white",
            relief="flat",
            padx=20
        )
        self.close_button.pack(side="right")
        
    def _on_language_change(self, event=None):
        """Handle language change."""
        new_lang = self.language_var.get()
        if new_lang != self.current_language:
            self.current_language = new_lang
            save_language(new_lang)
            self._update_text_labels()
            if self.on_language:
                self.on_language(new_lang)
                
    def _show_explanation(self):
        """Show explanation window with content based on current language."""
        try:
            # Import explanation content based on current language
            explanation_module = f"astronomical_watch.translate.explanation_{self.current_language}_card"
            
            # Dynamic import of explanation module
            import importlib
            module = importlib.import_module(explanation_module)
            explanation_text = module.EXPLANATION_TEXT
            
            # Create explanation window
            explanation_window = tk.Toplevel(self.master)
            explanation_window.title(f"{tr('explanation', self.current_language)} — {tr('title', self.current_language)}")
            explanation_window.geometry("700x600")
            explanation_window.minsize(600, 500)
            
            # Apply theme
            self._apply_explanation_theme(explanation_window)
            
            # Create scrollable text widget
            text_frame = tk.Frame(explanation_window)
            text_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Text widget with scrollbar
            text_widget = tk.Text(
                text_frame,
                wrap="word",
                font=("Arial", 11),
                bg="rgba(255,255,255,0.9)",
                fg="#2c3e50",
                padx=15,
                pady=15
            )
            
            scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            # Pack text and scrollbar
            text_widget.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Insert explanation text
            text_widget.insert("1.0", explanation_text)
            text_widget.config(state="disabled")  # Make read-only
            
            # Close button
            close_frame = tk.Frame(explanation_window)
            close_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            close_button = tk.Button(
                close_frame,
                text=tr("close", self.current_language),
                command=explanation_window.destroy,
                font=("Arial", 12),
                bg="#4a5568",
                fg="white",
                relief="flat",
                padx=20
            )
            close_button.pack(side="right")
            
        except ImportError:
            # Fallback if explanation file doesn't exist
            tk.messagebox.showwarning(
                tr("warning", self.current_language),
                f"Explanation not available for language: {self.current_language}"
            )
        except Exception as e:
            tk.messagebox.showerror(
                tr("error", self.current_language),
                f"Error loading explanation: {str(e)}"
            )
            
    def _apply_explanation_theme(self, window):
        """Apply theme to explanation window."""
        now_utc = datetime.now(timezone.utc)
        theme = get_sky_theme(now_utc)
        window.configure(bg=theme["bg_gradient"])
                
    def _update_text_labels(self):
        """Update all text labels with current language."""
        self.title_label.config(text=tr("title", self.current_language))
        
        # Update other labels as needed
        # This would be expanded with more UI elements
        
    def _apply_theme(self):
        """Apply sky gradient theme based on current time."""
        now_utc = datetime.now(timezone.utc)
        theme = get_sky_theme(now_utc)
        
        self.master.configure(bg=theme["bg_gradient"])
        self.main_frame.configure(bg=theme["bg_gradient"])
        self.time_frame.configure(bg=theme["bg_gradient"])
        self.progress_frame.configure(bg=theme["bg_gradient"])
        self.info_frame.configure(bg=theme["bg_gradient"])
        self.controls_frame.configure(bg=theme["bg_gradient"])
        
    def _update_display(self):
        """Update the astronomical time display."""
        try:
            # Get current time
            now_utc = datetime.now(timezone.utc)
            
            # Use hardcoded equinox values for now (same as widget.py)
            current_equinox = datetime(2025, 3, 20, 9, 1, 28, tzinfo=timezone.utc)
            next_equinox = datetime(2026, 3, 20, 14, 45, 50, tzinfo=timezone.utc)
            
            # Create AstroYear and get reading
            astro_year = AstroYear(current_equinox, next_equinox)
            reading = astro_year.reading(now_utc)
            
            # Update display values
            self.day_index = reading.day_index
            self.milliDies = reading.miliDies
            self.progress_percent = (reading.miliDies / 1000.0) * 100
            
            # Update UI
            time_str = f"{self.day_index:03d}·{self.milliDies:03d}"
            self.time_label.config(text=time_str)
            
            self.progress_bar['value'] = self.progress_percent
            self.progress_label.config(text=f"{self.progress_percent:.1f}%")
            
            # Update info text
            info_text = f"""
{tr("current_time", self.current_language)}: {now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}
{tr("astronomical_time", self.current_language)}: {time_str}
{tr("day_index", self.current_language)}: {self.day_index}
{tr("miliDies", self.current_language)}: {self.milliDies}
{tr("progress_through_day", self.current_language)}: {self.progress_percent:.1f}%

{tr("explanation", self.current_language)}
            """.strip()
            
            self.info_text.delete('1.0', tk.END)
            self.info_text.insert('1.0', info_text)
            
            # Update theme
            self._apply_theme()
            
        except Exception as e:
            print(f"Update error: {e}")
            # Fallback display
            self.time_label.config(text="ERR·000")
            
    def start_updates(self):
        """Start the periodic update cycle."""
        self._update_display()
        # Schedule next update in 1 second
        self.update_job = self.master.after(1000, self.start_updates)
        
    def stop_updates(self):
        """Stop the periodic updates."""
        if self.update_job:
            self.master.after_cancel(self.update_job)
            self.update_job = None

def create_normal_mode(master: tk.Widget = None, on_back=None, on_language=None) -> AstronomicalNormalMode:
    """Factory function to create normal mode instance."""
    return AstronomicalNormalMode(master, on_back, on_language)