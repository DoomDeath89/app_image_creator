import os
import shutil
from pathlib import Path
from typing import Callable, Optional

from app.utils.constants import (
    BIN_DIR,
    ICON_DIR,
    APPLICATIONS_DIR,
    LIB_DIR,
    DEFAULT_APP_VERSION,
)
from app.utils.types import BuildConfig


class AppDirBuilder:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.appdir_path: Optional[Path] = None

    def create(self, config: BuildConfig) -> Path:
        name = config.name
        self.appdir_path = self.base_dir / f"{name}.AppDir"

        if self.appdir_path.exists():
            shutil.rmtree(self.appdir_path)

        (self.appdir_path / BIN_DIR).mkdir(parents=True, exist_ok=True)
        (self.appdir_path / ICON_DIR).mkdir(parents=True, exist_ok=True)
        (self.appdir_path / APPLICATIONS_DIR).mkdir(parents=True, exist_ok=True)
        (self.appdir_path / LIB_DIR).mkdir(parents=True, exist_ok=True)

        return self.appdir_path

    def cleanup(self) -> None:
        if self.appdir_path and self.appdir_path.exists():
            shutil.rmtree(self.appdir_path)
            self.appdir_path = None

    def add_executable(self, src: Path) -> Path:
        dest = self.appdir_path / BIN_DIR / src.name
        shutil.copy2(src, dest)
        return dest

    def add_icon(self, src: Path, name: str) -> Path:
        dest = self.appdir_path / ICON_DIR / f"{name}.png"
        shutil.copy2(src, dest)
        return dest

    def create_desktop_file(self, config: BuildConfig, content: str) -> Path:
        desktop_path = self.appdir_path / APPLICATIONS_DIR / f"{config.name}.desktop"
        desktop_path.write_text(content, encoding='utf-8')
        return desktop_path

    def create_apprun_script(self, executable_name: str) -> Path:
        apprun_content = (
            "#!/bin/bash\n"
            'HERE="$(dirname "$(readlink -f "${0}")")"\n'
            'export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"\n'
            f'exec "$HERE/usr/bin/{executable_name}" "$@"\n'
        )
        apprun_path = self.appdir_path / "AppRun"
        apprun_path.write_text(apprun_content, encoding='utf-8')
        apprun_path.chmod(0o755)
        return apprun_path
