# WINDOWS TROUBLESHOOTING GUIDE

## If installation seems to "close" or "do nothing"

This usually happens when PowerShell has restricted execution policy.

### SOLUTION - Use the New Installers:

1. **Delete** the old shortcut from Desktop if you made one manually
2. **Use one of these installers** instead:

## Option 1: INSTALL_EASY.bat ⭐ RECOMMENDED

This now works WITHOUT PowerShell!

```
Double-click: INSTALL_EASY.bat
```

This will:
- Install the package
- Create desktop shortcut with icon
- Show all steps clearly
- No PowerShell required!

## Option 2: QUICK_TEST.bat (If already installed)

If you already ran `pip install .`, use this to test:

```
Double-click: QUICK_TEST.bat
```

This will:
- Check if Python works
- Check if package is installed
- Try to launch the app
- Show ANY error messages

## Option 3: Manual Step-by-Step

If everything fails, do this manually:

### Step 1: Install the package

```cmd
cd C:\Users\YourName\Downloads\Astronomical-watch
pip install .
```

### Step 2: Test if it works

```cmd
python -m astronomical_watch.ui.main
```

If you see errors, screenshot them and we'll fix it!

### Step 3: If it works, create shortcut manually

1. Right-click Desktop → New → Shortcut
2. Location: `pythonw -m astronomical_watch.ui.main`
3. Name: Astronomical Watch
4. Right-click shortcut → Properties → Change Icon
5. Browse to: `C:\Users\YourName\Downloads\Astronomical-watch\icons\astronomical_watch.ico`

## Common Errors and Fixes

### "No module named 'astronomical_watch'"
**Problem**: Package not installed
**Fix**: Run `pip install .` from the Astronomical-watch folder

### "No module named 'tkinter'"
**Problem**: Tkinter not installed with Python
**Fix**: Reinstall Python from python.org, make sure "tcl/tk and IDLE" is checked

### "Python was not found"
**Problem**: Python not in PATH
**Fix**: Reinstall Python, check "Add Python to PATH" during installation

### Shortcut does nothing
**Problem**: pythonw.exe not in PATH
**Fix**: 
1. Find your Python installation (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\`)
2. Edit shortcut Target to full path:
   ```
   C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\pythonw.exe -m astronomical_watch.ui.main
   ```

## Still Not Working?

1. Run `QUICK_TEST.bat` - it will show the exact error
2. Or open Command Prompt and run:
   ```cmd
   cd C:\Users\YourName\Downloads\Astronomical-watch
   python -m astronomical_watch.ui.main
   ```
3. Screenshot any error messages
4. The error message will tell us exactly what's wrong!

## Files in This Package

- `INSTALL_EASY.bat` ⭐ - Best installer (no PowerShell)
- `install.bat` - Original installer (also creates shortcut now)
- `install.ps1` - PowerShell version (might need admin)
- `QUICK_TEST.bat` - Test if everything works
- `TEST_LAUNCH.bat` - Launch with error messages visible
- `uninstall.bat` - Remove the application

## Contact

If none of this works, we need to see:
1. Output of: `python --version`
2. Output of: `pip list | findstr astronomical`
3. Output of: `python -m astronomical_watch.ui.main`

This will help diagnose the exact problem!
