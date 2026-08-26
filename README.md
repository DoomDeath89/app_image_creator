# App Image Creator

A tkinter-based desktop GUI application for creating AppImages on Linux. Simplifies the AppImage creation process with an intuitive interface, automatic dependency detection, and configuration management.

## Features

- **Build AppImages**: Create AppImages from any Linux executable
- **Desktop File Validator**: Validate .desktop files before building
- **Dependencies Manager**: Add extra library dependencies
- **Save/Load Configuration**: Export and import build configurations as JSON
- **Auto-install linuxdeploy**: Install linuxdeploy directly from the GUI
- **Non-blocking Builds**: Build process runs in background thread
- **Cancel Support**: Abort running builds at any time
- **Error Handling**: User-friendly error messages and recovery

## Installation

### Quick Start

```bash
git clone https://github.com/DoomDeath89/app_image_creator.git
cd app_image_creator
python3 run_app.py
```

### With Virtual Environment (Recommended)

```bash
git clone https://github.com/DoomDeath89/app_image_creator.git
cd app_image_creator
python3 -m venv venv
source venv/bin/activate
python run_app.py
```

### System Requirements

- Python 3.8+
- tkinter (usually included with Python on Linux)
- Linux with X11 or Wayland display server

## Usage

### Build Tab

1. **Select Executable**: Click "Browse" to select your Linux binary
2. **Select Icon**: Click "Browse" to select a .png icon file
3. **Fill Metadata**: Enter app name, version, category, and comment
4. **Add Dependencies** (optional): Switch to Dependencies tab to add libraries
5. **Generate**: Click "Generate AppImage" to start the build process

### Desktop File Validator Tab

- View and edit the generated .desktop file content
- Click "Validate Desktop File" to check for errors
- Fix any issues before building

### Dependencies Tab

- Click "Add" to select library files (.so)
- Select and click "Remove" to delete selected dependencies
- Click "Clear" to remove all dependencies
- Click "Sort" to alphabetize the list

### Configuration

- **Save Config**: Export current settings to JSON file
- **Load Config**: Import settings from JSON file
- Configs include: executable path, icon path, name, version, category, comment

## Architecture

```
app/
├── core/
│   ├── main.py              # Window setup, notebook, mediator
│   └── mediator.py          # Cross-tab communication
├── tabs/
│   ├── build_tab.py         # Main build UI
│   ├── validator_tab.py     # Desktop file validator
│   └── dependencies_tab.py  # Dependency list manager
├── services/
│   ├── app_dir_builder.py   # AppDir creation
│   ├── desktop_file_handler.py  # .desktop file logic
│   └── linux_deploy_manager.py  # linuxdeploy management
└── utils/
    ├── constants.py         # App constants
    └── types.py             # Dataclasses
```

### Design Patterns

- **Mediator Pattern**: Tabs communicate through a central mediator
- **Service Layer**: Business logic separated from UI components
- **Thread Safety**: Build process runs in background thread

## Development

### Git Workflow (GitFlow)

This project follows GitFlow branching strategy:

- **main**: Production-ready code
- **develop**: Integration branch
- **feature/***: New features
- **release/***: Release preparation
- **hotfix/***: Emergency fixes

### Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: resolve bug
docs: update documentation
test: add tests
chore: maintenance tasks
```

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_build_tab.py -v

# Run with coverage
python -m pytest tests/ --cov=app
```

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings for public methods
- Keep functions focused and small

## Configuration

### Build Config JSON

```json
{
  "name": "MyApp",
  "version": "1.0",
  "category": "Game",
  "comment": "My awesome app",
  "executable_path": "/usr/bin/myapp",
  "icon_path": "/usr/share/icon.png"
}
```

### linuxdeploy

The app automatically detects and installs linuxdeploy:
- **x86_64**: Downloads amd64 version
- **ARM64**: Downloads arm64 version
- Requires `pkexec` for installation (polkit)

## Troubleshooting

### Build Fails

1. Check the Build Log for error messages
2. Verify executable exists and is runnable
3. Verify icon is a valid .png file
4. Ensure linuxdeploy is installed (check status in Build tab)

### UI Freezes

This should not happen in v1.1.0+. If it does:
1. Kill the process externally
2. Check for zombie processes: `ps aux | grep linuxdeploy`
3. Report issue with logs

### Dependencies Not Included

1. Ensure dependencies are added in Dependencies tab
2. Check Build Log for copy operations
3. Verify library files exist and are readable

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/DoomDeath89/app_image_creator.git
cd app_image_creator
python3 -m venv venv
source venv/bin/activate
pip install pytest
python -m pytest tests/ -v
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [AppImage](https://appimage.org/) - The AppImage format
- [linuxdeploy](https://github.com/linuxdeploy/linuxdeploy) - The build tool
- [AppImageKit](https://github.com/AppImage/AppImageKit) - Original AppImage tools

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.1.0 | 2026-08-26 | Threading, error handling, UX improvements |
| 1.0.0 | 2026-08-25 | Initial release |

## Support

- [GitHub Issues](https://github.com/DoomDeath89/app_image_creator/issues)
- [Documentation](https://github.com/DoomDeath89/app_image_creator/tree/main/docs)

## Roadmap

- [ ] Drag-and-drop support for files
- [ ] Progress bar during build
- [ ] Batch AppImage creation
- [ ] Custom linuxdeploy plugins
- [ ] Theme support (dark mode)
- [ ] Internationalization (i18n)
