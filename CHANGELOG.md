# Changelog

All notable changes to Astronomical Watch will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-07

### Added
- Complete installation system for Linux, macOS, and Windows
- Desktop entry file for Linux application menus
- Installation scripts (install.sh, install.bat)
- Comprehensive documentation (INSTALL.md, USER_GUIDE.md, BUILD.md)
- Package manifest (MANIFEST.in) for distribution
- Entry points: `astronomical-watch` and `awatch` commands
- Gray checkbox background for better visibility on all themes
- Underline hover effect for checkboxes instead of color change
- Fixed entry field colors in comparison card (now use theme colors)
- Auto-activation of input fields in comparison card
- Support for both NumLock ON and OFF numpad states

### Fixed
- Russian explanation card syntax error (em dash character)
- Vietnamese explanation card unterminated string
- Checkbox visibility issues with dark/light themes
- Entry field text visibility (white on white background)
- Input field activation in comparison card

### Changed
- Updated pyproject.toml version to 1.0.0
- Improved entry points for better command-line usage
- Enhanced theme manager with automatic color updates
- All UI components now use solid theme colors
- Checkbox backgrounds set to neutral gray (#808080)
- Settings card checkboxes dynamically update with theme

### Documentation
- Added INSTALL.md with complete installation instructions
- Added QUICK_INSTALL.md for quick reference
- Added USER_GUIDE.md with usage instructions
- Added BUILD.md for creating distribution packages
- Added INSTALLATION_SUMMARY.md with overview
- Updated README.md with installation links

## [0.0.1] - 2025-12-06

### Initial Release
- Core astronomical calculations (VSOP87D, equinox solving)
- Widget mode (180x110 borderless display)
- Normal mode with 4 cards (Explanation, Comparison, Settings, Standard Time)
- 28 language support with full translations
- Real-time theme updates based on solar position
- Interactive calendar with Dies display
- Time converter (miliDies ↔ HH:MM)
- Settings persistence
- Drag-and-drop window positioning
- Transparent background support (Windows)
- Always on top option
- Auto-start configuration

---

[1.0.0]: https://github.com/NndMlc/Astronomical-watch/releases/tag/v1.0.0
[0.0.1]: https://github.com/NndMlc/Astronomical-watch/releases/tag/v0.0.1
