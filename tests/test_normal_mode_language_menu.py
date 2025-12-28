

import sys
import os
import pytest
import tkinter as tk
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from astronomical_watch.ui.normal_mode import ModernNormalMode

def _can_open_tk():
    try:
        root = tk.Tk()
        root.destroy()
        return True
    except tk.TclError:
        return False

@pytest.mark.ui
def test_language_menu_single_instance(monkeypatch):
    """Test da li je moguće otvoriti samo jedan prozor za izbor jezika u Normal Mode-u."""
    if not _can_open_tk():
        pytest.skip("Nema grafičkog okruženja (DISPLAY), preskačem test.")
    root = tk.Tk()
    root.withdraw()  # Ne prikazuj glavni prozor
    normal_mode = ModernNormalMode(root)

    # Prvi put otvaramo meni
    normal_mode._show_language_menu()
    first_ref = normal_mode._lang_window_ref
    assert first_ref is not None
    assert first_ref.winfo_exists()

    # Pokušavamo da otvorimo još jednom
    normal_mode._show_language_menu()
    # Referenca mora biti ista, prozor nije dupliran
    assert normal_mode._lang_window_ref is first_ref
    assert first_ref.winfo_exists()

    # Zatvaramo prozor
    first_ref.destroy()
    root.update()  # Očisti event loop
    # Referenca mora biti None
    assert normal_mode._lang_window_ref is None or not first_ref.winfo_exists()

    root.destroy()
