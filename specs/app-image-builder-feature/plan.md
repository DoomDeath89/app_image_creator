# Implementation Plan: AppImage Builder Improvements

**Branch**: `feature/appimage-builder-improvements` | **Date**: 2026-08-26 | **Spec**: specs/app-image-builder-feature/spec.md

**Input**: Feature specification from `/specs/app-image-builder-feature/spec.md`

## Summary

Improve AppImage Builder with non-blocking builds via threading, proper dependency integration, robust error handling, and UX enhancements. The build process runs in a background thread with cancel support, dependencies are included in the AppDir, and all error paths provide user-friendly feedback.

## Technical Context

**Language/Version**: Python 3.8+
**Primary Dependencies**: tkinter, ttk, subprocess, threading, json
**Storage**: File system (AppDir, config JSON)
**Testing**: pytest with unittest mocks
**Target Platform**: Linux (X11/Wayland)
**Project Type**: Desktop GUI application
**Performance Goals**: UI responsive during build (<100ms frame updates)
**Constraints**: Must work with python3-tk package on most Linux distros
**Scale/Scope**: Single-user desktop tool, ~300 lines in main tab

## Constitution Check

- UI-First Architecture: Tab is pure UI, services handle logic ✓
- Thread Safety: Build runs in background thread ✓
- Graceful Degradation: Cleanup on failure/cancel ✓
- Test-First: Tests written for all new features ✓
- Mediator Pattern: Cross-tab via mediator ✓

## Project Structure

```text
app/
├── core/
│   ├── main.py              # Window setup, notebook, mediator
│   └── mediator.py          # Cross-tab communication
├── tabs/
│   ├── build_tab.py         # Main build UI (THIS FILE - major changes)
│   ├── validator_tab.py     # Desktop file validator
│   └── dependencies_tab.py  # Dependency list manager
├── services/
│   ├── app_dir_builder.py   # AppDir creation
│   ├── desktop_file_handler.py  # .desktop file logic
│   └── linux_deploy_manager.py  # linuxdeploy management
└── utils/
    ├── constants.py         # App constants
    └── types.py             # Dataclasses

tests/
├── test_build_tab.py        # BuildTab tests
├── test_dependencies_tab.py # DependenciesTab tests
├── test_mediator.py         # Mediator tests
├── test_services.py         # Service tests
└── test_validator_tab.py    # ValidatorTab tests
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| threading.Thread | Build blocks UI for minutes | Subprocess timeout insufficient - need real-time log |
| frame.after() | Thread-safe UI updates | Queue-based updates too complex for simple case |
| shutil.copy2 for deps | Must copy libs to AppDir | Symlinks break in AppImage |
