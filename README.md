# AppImage Builder

A Tkinter GUI application to create AppImages using linuxdeploy. Features include a .desktop file validator, dependency management, and configuration save/load.

## Features

- **Build AppImages**: Create AppImages from any Linux executable
- **Desktop File Validator**: Validate .desktop files before building
- **Dependencies Manager**: Add extra library dependencies
- **Save/Load Configuration**: Export and import build configurations as JSON
- **Auto-install linuxdeploy**: Install linuxdeploy directly from the GUI

## Requirements

- Python 3.8+
- Tkinter (usually included with Python on Linux)
- linuxdeploy (can be installed from the GUI)

## Installation

### Quick Start

```bash
git clone https://github.com/DoomDeath89/app_image_creator.git
cd app_image_creator
python run_app.py
```

### With Virtual Environment (Recommended)

```bash
git clone https://github.com/DoomDeath89/app_image_creator.git
cd app_image_creator
python3 -m venv venv
source venv/bin/activate
python run_app.py
```

## Usage Manual

### 1. Build Tab

The main tab for creating AppImages.

#### Required Fields

| Field | Description |
|-------|-------------|
| **Executable** | Path to your Linux binary. Click "Browse" to select. |
| **Icon** | Path to a .png icon file. Click "Browse" to select. |
| **App Name** | Name of your application (auto-filled from executable). |
| **Version** | Application version (default: 1.0). |
| **Category** | Application category from the dropdown. |
| **Comment** | Short description of your application. |

#### Buttons

- **Save Config**: Export current configuration to a .json file
- **Load Config**: Import configuration from a .json file
- **Generate AppImage**: Start the AppImage build process

#### Build Process

1. Fill in all required fields
2. Click "Generate AppImage"
3. Monitor progress in the Build Log
4. The AppImage will be created in the current directory

### 2. Desktop File Validator Tab

Validate your .desktop file content before building.

- Paste or edit your .desktop file content
- Click "Validate Desktop File"
- View validation results (errors in red, warnings in orange)

### 3. Dependencies Tab

Add extra library dependencies if needed.

- Click "Add" to select dependency files
- Use "Sort" to alphabetize the list
- Select items and click "Remove Selected" to delete
- Click "Clear All" to remove all dependencies

### 4. Save/Load Configuration

#### Save Configuration

1. Click "Save Config" in the Build tab
2. Choose a location and filename (.json)
3. Your current configuration is saved

#### Load Configuration

1. Click "Load Config" in the Build tab
2. Select a previously saved .json file
3. All fields are populated automatically

#### Configuration File Format

```json
{
  "name": "MyApp",
  "version": "1.0",
  "category": "Game",
  "comment": "My awesome application",
  "executable_path": "/path/to/executable",
  "icon_path": "/path/to/icon.png"
}
```

## Install linuxdeploy

### Option 1: From the GUI

1. If linuxdeploy is not installed, you'll see "linuxdeploy: not found" in red
2. Click "Install linuxdeploy"
3. Confirm the installation
4. Enter your password when prompted

### Option 2: Using the Script

```bash
./install_appimage_tools.sh
```

## Project Structure

```
app_image_creator/
├── app/
│   ├── core/           # Main app and mediator
│   ├── tabs/           # UI components
│   ├── services/       # Business logic
│   └── utils/          # Constants and types
├── tests/              # Test suite
├── docs/specs/         # Feature specifications
├── run_app.py          # Entry point
└── pyproject.toml      # Package configuration
```

## Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Testing

```bash
pip install pytest
pytest
```

## Supported Categories

- AudioVideo, Audio, Video, Graphics, Office
- Development, Education, Game, Network
- Settings, System, Utility

## License

MIT. See [LICENSE](LICENSE) for details.
