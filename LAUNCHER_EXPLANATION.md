# Desktop Launcher - Zašto je potreban?

## Razlog za `astronomical_watch_desktop.py`

### 1. **Složena struktura projekta**
```
src/astronomical_watch/    # Glavni paket
cli/                       # CLI alternative  
tests/                     # Test files
```

### 2. **User Experience**
```bash
# Jednostavno za korisnika:
python astronomical_watch_desktop.py

# Alternativa bez launcher-a (kompleksnije):
cd src && python -m astronomical_watch.ui.main
# ili
pip install -e . && astronomical-watch-gui
```

### 3. **Path Management**
Launcher automatski rešava PYTHONPATH probleme:
```python
# U launcher-u:
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")  
sys.path.insert(0, src_dir)  # Dodaje src/ u path
```

### 4. **Praksa u realnim projektima**
- **VSCode**: `code.sh` launcher script
- **PyCharm**: `pycharm.sh` launcher  
- **Blender**: `blender` launcher script
- **Many desktop apps**: Imaju launcher koji postavlja environment

## Alternativni pristup

### Opcija A: Zadržati launcher (PREPORUČENO)
```bash
python astronomical_watch_desktop.py   # Jednostavno i pouzdano
```

### Opcija B: Proper pip installation
```bash
pip install -e .                       # Instalacija
astronomical-watch-gui                 # Entry point
```

### Opcija C: Direct execution
```bash  
cd src && python -m astronomical_watch.ui.main   # Iz src/
```

## Preporuka: ZADRŽATI LAUNCHER

Razlozi:
- ✅ **User-friendly** - jedan jednostavan command
- ✅ **Self-contained** - ne zahteva pip install
- ✅ **Path safe** - automatski path management  
- ✅ **Cross-platform** - radi svugde isto
- ✅ **Development friendly** - odmah radi bez setup-a

Launcher je **dobra praksa** za desktop aplikacije!