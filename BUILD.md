# Building Distribution Packages

This guide explains how to create distribution packages for Astronomical Watch.

## Prerequisites

Install build tools:

```bash
pip install --upgrade build twine
```

## Building Packages

### Build Wheel and Source Distribution

```bash
# From the project root directory
python -m build
```

This creates:
- `dist/astronomical_watch-1.0.0-py3-none-any.whl` (wheel package)
- `dist/astronomical-watch-1.0.0.tar.gz` (source distribution)

### Building Only Wheel

```bash
python -m build --wheel
```

### Building Only Source Distribution

```bash
python -m build --sdist
```

## Installing from Built Package

```bash
# Install the wheel
pip install dist/astronomical_watch-1.0.0-py3-none-any.whl

# Or install from source tarball
pip install dist/astronomical-watch-1.0.0.tar.gz
```

## Publishing to PyPI (Optional)

**Note**: Only for official releases by maintainers.

### Test PyPI (for testing)

```bash
python -m twine upload --repository testpypi dist/*
```

### Production PyPI

```bash
python -m twine upload dist/*
```

## Creating Platform-Specific Packages

### Debian/Ubuntu Package (.deb)

Install required tools:

```bash
sudo apt install python3-stdeb dh-python
```

Build the package:

```bash
python3 setup.py --command-packages=stdeb.command bdist_deb
```

The `.deb` file will be in `deb_dist/`.

Install:

```bash
sudo dpkg -i deb_dist/astronomical-watch_1.0.0-1_all.deb
```

### RPM Package (Fedora, RHEL, etc.)

Install required tools:

```bash
sudo dnf install rpm-build python3-setuptools
```

Build the package:

```bash
python3 setup.py bdist_rpm
```

The `.rpm` file will be in `dist/`.

### Windows Executable (.exe)

Install PyInstaller:

```bash
pip install pyinstaller
```

Build standalone executable:

```bash
pyinstaller --onefile --windowed \
    --name "Astronomical Watch" \
    --icon icons/astronomical_watch.ico \
    src/astronomical_watch/ui/main.py
```

The `.exe` will be in `dist/`.

### macOS Application Bundle (.app)

Install py2app:

```bash
pip install py2app
```

Create setup file and build:

```bash
py2applet --make-setup astronomical_watch_desktop.py
python3 setup.py py2app
```

The `.app` bundle will be in `dist/`.

## Distribution Checklist

Before releasing:

- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG.md
- [ ] Run all tests: `pytest`
- [ ] Test installation from built package
- [ ] Test on different platforms (Linux, macOS, Windows)
- [ ] Update documentation
- [ ] Create Git tag: `git tag v1.0.0`
- [ ] Push tag: `git push origin v1.0.0`

## Cleaning Build Artifacts

```bash
# Remove build directories
rm -rf build/ dist/ *.egg-info/

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

## Automated Release Process

For maintainers, GitHub Actions can automate building and publishing:

1. Create `.github/workflows/release.yml`
2. Configure PyPI API token in GitHub secrets
3. Tag a release: `git tag v1.0.0 && git push origin v1.0.0`
4. Workflow builds and publishes automatically

## Versioning

Follow Semantic Versioning (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible features
- **PATCH** version for backwards-compatible bug fixes

Example: `1.0.0` → `1.1.0` (new feature) → `1.1.1` (bug fix) → `2.0.0` (breaking change)
