APP_NAME = "AppImage Builder"
APP_VERSION = "1.0.0"
DEFAULT_APP_VERSION = "1.0"

LINUXDEPLOY_URLS = {
    'arm64': 'https://github.com/linuxdeploy/linuxdeploy/releases/download/1-alpha-20250213-2/linuxdeploy-aarch64.AppImage',
    'amd64': 'https://github.com/linuxdeploy/linuxdeploy/releases/download/1-alpha-20250213-2/linuxdeploy-x86_64.AppImage',
}

VALID_CATEGORIES = [
    'AudioVideo', 'Audio', 'Video', 'Graphics', 'Office',
    'Development', 'Education', 'Game', 'Network', 'Settings',
    'System', 'Utility'
]

REQUIRED_DESKTOP_FIELDS = ['Name', 'Exec', 'Type', 'Categories']

DEFAULT_COMMENT = "App created with AppImage Builder"

ICON_SIZE = '256x256'
ICON_DIR = f'usr/share/icons/hicolor/{ICON_SIZE}/apps'
BIN_DIR = 'usr/bin'
APPLICATIONS_DIR = 'usr/share/applications'
LIB_DIR = 'usr/lib'
