
# AppImage Builder

Tkinter GUI to create AppImages using linuxdeploy. Includes a simple .desktop file validator and a button to install linuxdeploy if not available.

## Download

- Release arm64 (PyInstaller onefile): https://github.com/DoomDeath89/app_image_creator/releases/tag/1.0.0
- SHA256 checksum: https://github.com/DoomDeath89/app_image_creator/releases/tag/1.0.0

## Screenshots

Add screenshots in `docs/screenshots/` and link them here when ready.

## Requirements

- Python 3
- Tkinter (usually included with Python installation on Linux)
- linuxdeploy (can be installed from the GUI or with the script)

## Run from source code

If you want to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
python3 main.py
```

Or run directly:

```bash
python3 main.py
```


## Launcher Script: run_appimager.sh

This script ensures a Python virtual environment exists in ./venv, creates it if missing, activates it, and runs run_app.py.

Usage:

```bash
./run_appimager.sh
```

Steps:
- Checks for ./venv directory.
- Creates venv if not found.
- Activates the virtual environment.
- Runs run_app.py with Python.

## Executable (arm64)

Download the binary from the release and give it permissions:

```bash
chmod +x AppImageBuilder
./AppImageBuilder
```

## Install linuxdeploy

Option 1: from the GUI

- If not installed, the "Install linuxdeploy" button allows you to download and install with confirmation.

Option 2: with the script

```bash
./install_appimage_tools.sh
```

## Publishing in directories

- Consider publishing in AppImageHub/AppImage Catalog when you have a public AppImage.


## Notes

- The AppDir is created as `<AppName>.AppDir` and will be overwritten if it already exists.
- The default version is 1.0 if not specified.

## License

MIT. See LICENSE.
