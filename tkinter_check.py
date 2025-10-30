# -*- coding: utf-8 -*-
"""
Astronomical Watch - Windows tkinter installer/checker
Automatski instaliraj tkinter ako ne postoji
"""
import sys
import subprocess

def install_tkinter():
    """Pokušaj da instaliraš tkinter"""
    print("Pokušavam da instaliram tkinter...")
    
    try:
        # Za Python 3.x, tkinter dolazi ugrađen
        # Ali možda treba da se reinstalira Python
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tk"])
        print("tkinter instaliran uspešno!")
        return True
    except:
        print("Automatska instalacija nije uspela.")
        return False

def check_and_import_tkinter():
    """Proveri i importuj tkinter"""
    
    # Pokušaj standardni import
    try:
        import tkinter as tk
        print("tkinter je dostupan!")
        return tk
    except ImportError:
        pass
    
    # Pokušaj alternativni import (Python 2 style)
    try:
        import Tkinter as tk
        print("tkinter (Tkinter) je dostupan!")
        return tk
    except ImportError:
        pass
    
    # Pokušaj da instaliraš
    print("tkinter nije pronađen. Pokušavam instalaciju...")
    if install_tkinter():
        try:
            import tkinter as tk
            return tk
        except ImportError:
            pass
    
    # Konačna greška
    print("GREŠKA: tkinter se ne može importovati!")
    print("")
    print("REŠENJA:")
    print("1. Reinstaliraj Python sa https://python.org/downloads/")
    print("   Tokom instalacije štikliraj 'tcl/tk and IDLE'")
    print("2. Ili pokreni: pip install tk")
    print("3. Ili pokreni: python -m tkinter (da testiraš)")
    print("")
    input("Pritisni Enter da izađeš...")
    return None

# Test imports
if __name__ == "__main__":
    print("=== TKINTER COMPATIBILITY CHECK ===")
    print("")
    
    tk = check_and_import_tkinter()
    
    if tk:
        print("TEST: Kreiram test window...")
        try:
            root = tk.Tk()
            root.title("tkinter Test")
            root.geometry("200x100")
            
            label = tk.Label(root, text="tkinter radi!")
            label.pack(pady=20)
            
            button = tk.Button(root, text="Zatvori", command=root.quit)
            button.pack()
            
            print("Test window kreiran. Zatvori ga da nastaviš.")
            root.mainloop()
            print("tkinter test USPEŠAN!")
            
        except Exception as e:
            print(f"Test neuspešan: {e}")
    else:
        print("tkinter test NEUSPEŠAN!")