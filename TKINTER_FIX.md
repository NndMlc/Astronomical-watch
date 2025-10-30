# 🔧 Rešavanje tkinter Problema na Windows-u

## Problem: "ImportError: No module named tkinter"

Ovo je čest problem na Windows sistemima. Evo kako da ga rešiš:

## 🚀 BRZA REŠENJA

### Rešenje 1: Console verzija (Odmah radi)
```cmd
# Pokreni console verziju koja ne traži tkinter
python awatch_console.py
```

### Rešenje 2: Smart launcher (Automatski)
```cmd
# Dupli klik na ovaj fajl - automatski bira pravu verziju
awatch_smart_launcher.bat
```

## 🔨 TRAJNO REŠAVANJE tkinter-a

### Opcija A: Reinstalacija Python-a (Preporučeno)

1. **Download Python**
   - Idi na https://python.org/downloads/
   - Download najnoviju verziju

2. **Tokom instalacije:**
   ```
   ☑️ Add Python to PATH
   ☑️ tcl/tk and IDLE (OBAVEZNO!)
   ☑️ Python test suite
   ```

3. **Test:**
   ```cmd
   python -m tkinter
   # Trebalo bi da se otvori mali tkinter test window
   ```

### Opcija B: Instalacija tkinter-a

```cmd
# Pokušaj ove komande
pip install tk

# Ili
python -m pip install tk

# Ili za Anaconda
conda install tk
```

### Opcija C: Alternative Python distributacije

- **Anaconda**: https://anaconda.com/products/distribution
- **WinPython**: https://winpython.github.io/
- Oba dolaze sa tkinter ugrađenim

## 📱 Dostupne Verzije

### 1. Console verzija - `awatch_console.py`
```
==================================================
       ASTRONOMICAL WATCH CONSOLE
       mikroDies Precision Display
==================================================

  ASTRONOMICAL TIME: 224.995.709
  Format: Dies.miliDies.mikroDies

  UTC Time:      2025-10-30 15:30:45
  Dies:          224
  miliDies:      995
  mikroDies:     709
  Precision:     0.123456

  miliDies [██████████████████████████░░░░] 85.5%

  Press Ctrl+C to exit
==================================================
```

### 2. GUI verzija - `awatch_windows.py` (zahteva tkinter)
```
┌─────────────────────────────────────┐
│        ASTRONOMICAL WATCH           │
│     mikroDies Precision Desktop     │
├─────────────────────────────────────┤
│           224.995.709               │
│      Dies . miliDies . mikroDies    │
├─────────────────────────────────────┤
│ UTC: 15:30:45                       │
├─────────────────────────────────────┤
│ Dies: 224            mikroDies: 709 │
│ Period: 2025-26      Status: Running│
└─────────────────────────────────────┘
```

## 🧪 Test Komande

```cmd
# Test Python
python --version

# Test tkinter
python -c "import tkinter; print('tkinter OK')"

# Test tkinter sa window
python -m tkinter

# Test Astronomical Watch
python awatch_console.py
```

## 📥 Fajlovi za Download

Kopiraj ove fajlove na Windows:

1. **`awatch_console.py`** - Console verzija (uvek radi)
2. **`awatch_windows.py`** - GUI verzija (ako tkinter radi)
3. **`awatch_smart_launcher.bat`** - Automatski launcher
4. **`tkinter_check.py`** - tkinter test i installer

## 🎯 Preporučeni Workflow

```cmd
# 1. Brzi test
python awatch_console.py

# 2. Ako hoćeš GUI, popravi tkinter
python tkinter_check.py

# 3. Koristi smart launcher
awatch_smart_launcher.bat
```

Console verzija radi na svakom Windows sistemu sa Python-om! 🎉