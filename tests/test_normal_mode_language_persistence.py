

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
def test_language_change_persists(monkeypatch, tmp_path):
    """Test da li se izbor jezika trajno čuva u config fajlu i učitava pri novom pokretanju."""
    if not _can_open_tk():
        pytest.skip("Nema grafičkog okruženja (DISPLAY), preskačem test.")
    # Pripremi privremeni home direktorijum
    monkeypatch.setenv("HOME", str(tmp_path))
    root = tk.Tk()
    root.withdraw()
    normal_mode = ModernNormalMode(root)

    # Promeni jezik na npr. francuski
    normal_mode._change_language("fr")
    # Simuliraj ponovno pokretanje
    root2 = tk.Tk()
    root2.withdraw()
    normal_mode2 = ModernNormalMode(root2)
    assert normal_mode2.current_language == "fr"
    root.destroy()
    root2.destroy()
