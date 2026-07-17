import platform
import shutil
import subprocess
from typing import Callable, Optional

from app.utils.constants import LINUXDEPLOY_URLS


class LinuxDeployManager:
    def is_available(self) -> bool:
        return shutil.which("linuxdeploy") is not None

    def get_version(self) -> Optional[str]:
        if not self.is_available():
            return None
        try:
            result = subprocess.run(
                ["linuxdeploy", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout.strip() or result.stderr.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def get_url(self, arch: str = None) -> Optional[str]:
        if arch is None:
            arch = platform.machine().lower()

        arch_map = {
            'aarch64': 'arm64',
            'arm64': 'arm64',
            'x86_64': 'amd64',
            'amd64': 'amd64',
        }

        normalized = arch_map.get(arch)
        return LINUXDEPLOY_URLS.get(normalized)

    def install(self, log_callback: Callable[[str], None] = None) -> bool:
        url = self.get_url()
        if not url:
            if log_callback:
                log_callback("Unsupported CPU architecture for automatic install.")
            return False

        if not shutil.which("pkexec"):
            if log_callback:
                log_callback("pkexec not found. Install policykit or run install_appimage_tools.sh manually.")
            return False

        if log_callback:
            log_callback("Installing linuxdeploy...")

        install_cmd = [
            "pkexec",
            "bash",
            "-c",
            "set -e; TMP_DIR=$(mktemp -d); cd \"$TMP_DIR\"; "
            f"wget -c \"{url}\" -O linuxdeploy.AppImage; "
            "chmod +x linuxdeploy.AppImage; "
            "mv linuxdeploy.AppImage /usr/local/bin/linuxdeploy; "
            "cd ~; rm -rf \"$TMP_DIR\""
        ]

        try:
            process = subprocess.Popen(
                install_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            output = ""
            for line in iter(process.stdout.readline, ''):
                if line:
                    output += line
                    if log_callback:
                        log_callback(line.strip())
            process.stdout.close()
            process.wait()

            if process.returncode != 0:
                if log_callback:
                    log_callback("linuxdeploy installation failed.")
                return False

            if log_callback:
                log_callback("linuxdeploy installed successfully.")
            return True

        except Exception as e:
            if log_callback:
                log_callback(f"Installation error: {e}")
            return False

    def ensure_available(self, log_callback: Callable[[str], None] = None) -> bool:
        if self.is_available():
            return True
        return self.install(log_callback)
