# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitFlow workflow documentation in constitution
- CHANGELOG.md
- README.md with comprehensive project documentation
- Specs directory with feature documentation

### Changed
- Adopt GitFlow branching strategy

---

## [1.1.0] - 2026-08-26

### Added
- **Thread-safe build process**: linuxdeploy now runs in a background thread, preventing UI freeze
- **Cancel button**: Users can abort running builds at any time
- **Dependency integration**: Dependencies tab now actually includes libraries in the AppDir
- **Log management**: Auto-clear log between builds, manual Clear button
- **Error handling**: All errors now show user-friendly dialogs instead of crashing
- **Config resilience**: Save/load handles corrupted JSON and permission errors gracefully

### Fixed
- UI freezing during build process (was blocking for 2+ minutes)
- Dependencies being ignored during build
- Test failures due to MagicMock notebook (5 tests were failing)
- No cleanup of partial AppDir on build failure

### Changed
- Build button is now disabled during build to prevent double-clicks
- Cancel button is enabled only during active builds
- Log updates use `frame.after()` for thread-safe UI updates
- Config values are converted to strings during load to handle non-string types

### Technical
- Added `threading.Thread` for background build execution
- Added `subprocess.Popen.terminate()` and `.kill()` for process cancellation
- Added `shutil.copy2()` for dependency file copying
- Added `--library` flags to linuxdeploy command for each dependency
- Tests updated to use real `ttk.Notebook` instead of `MagicMock`
- All 49 tests now pass

---

## [1.0.0] - 2026-08-25

### Added
- Initial release
- Tkinter GUI for creating AppImages
- Build tab with executable/icon selection
- Desktop file validation
- Dependency list management
- Save/load configuration
- linuxdeploy auto-install
- Mediator pattern for cross-tab communication
- Basic test suite

### Technical
- Python 3.8+ compatibility
- tkinter with ttk widgets
- Service layer architecture
- unittest with MagicMock

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.1.0 | 2026-08-26 | Threading, error handling, UX improvements |
| 1.0.0 | 2026-08-25 | Initial release |

---

## Release Notes

### v1.1.0

**Breaking Changes**: None

**New Features**:
- Build process no longer blocks the UI
- Users can cancel running builds
- Dependencies are now included in AppImages
- Better error messages and recovery

**Bug Fixes**:
- Fixed UI freeze during build
- Fixed dependencies being ignored
- Fixed test failures
- Fixed no cleanup on failure

**Upgrade Path**: Drop-in replacement, no config changes needed.

### v1.0.0

**Initial Release**:
- Core AppImage building functionality
- Desktop file validation
- Configuration save/load
- Basic test coverage

---

## Links

- [GitHub Repository](https://github.com/DoomDeath89/app_image_creator)
- [Issue Tracker](https://github.com/DoomDeath89/app_image_creator/issues)
- [Releases](https://github.com/DoomDeath89/app_image_creator/releases)
