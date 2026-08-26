import json
import os
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk

from app.core.mediator import Mediator
from app.services.app_dir_builder import AppDirBuilder
from app.services.linux_deploy_manager import LinuxDeployManager
from app.services.desktop_file_handler import DesktopFileHandler
from app.utils.constants import VALID_CATEGORIES, DEFAULT_COMMENT, DEFAULT_APP_VERSION
from app.utils.types import BuildConfig
from pathlib import Path


class BuildTab:
    def __init__(self, notebook, mediator: Mediator):
        self.mediator = mediator
        self.linuxdeploy = LinuxDeployManager()
        self.desktop_handler = DesktopFileHandler()
        self.frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.frame, text="Build AppImage")

        self._build_process = None
        self._build_thread = None
        self._builder = None
        self._appdir_path = None

        self._build_ui()
        self.exe_entry.focus()
        self._update_linuxdeploy_status()

    def _build_ui(self):
        exe_frame = ttk.Frame(self.frame)
        exe_frame.pack(fill=tk.X, pady=5)
        ttk.Label(exe_frame, text="Executable:").pack(anchor=tk.W)
        self.exe_entry = ttk.Entry(exe_frame, width=70)
        self.exe_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(exe_frame, text="Browse", command=self.select_executable).pack(side=tk.RIGHT)

        icon_frame = ttk.Frame(self.frame)
        icon_frame.pack(fill=tk.X, pady=5)
        ttk.Label(icon_frame, text="Icon (.png):").pack(anchor=tk.W)
        self.icon_entry = ttk.Entry(icon_frame, width=70)
        self.icon_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(icon_frame, text="Browse", command=self.select_icon).pack(side=tk.RIGHT)

        metadata_frame = ttk.Frame(self.frame)
        metadata_frame.pack(fill=tk.X, pady=5)

        ttk.Label(metadata_frame, text="App Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(metadata_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(5, 20))

        ttk.Label(metadata_frame, text="Version:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.version_entry = ttk.Entry(metadata_frame, width=15)
        self.version_entry.grid(row=0, column=3, sticky=tk.W, pady=2, padx=5)

        ttk.Label(metadata_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            metadata_frame, width=28, textvariable=self.category_var,
            values=VALID_CATEGORIES,
        )
        self.category_combo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(5, 20))
        self.category_combo.set("Game")

        ttk.Label(metadata_frame, text="Comment:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.comment_entry = ttk.Entry(metadata_frame, width=15)
        self.comment_entry.grid(row=1, column=3, sticky=tk.W, pady=2, padx=5)
        self.comment_entry.insert(0, DEFAULT_COMMENT)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Save Config", command=self._save_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Load Config", command=self._load_config).pack(side=tk.LEFT, padx=(0, 5))
        self.generate_button = ttk.Button(button_frame, text="Generate AppImage", command=self.build_appimage)
        self.generate_button.pack(side=tk.LEFT, padx=(0, 5))
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self._cancel_build, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT)

        linuxdeploy_frame = ttk.Frame(self.frame)
        linuxdeploy_frame.pack(fill=tk.X, pady=5)
        self.linuxdeploy_status_label = ttk.Label(linuxdeploy_frame, text="")
        self.linuxdeploy_status_label.pack(side=tk.LEFT)
        self.install_linuxdeploy_button = ttk.Button(
            linuxdeploy_frame,
            text="Install linuxdeploy",
            command=self._prompt_install_linuxdeploy,
        )
        self.install_linuxdeploy_button.pack(side=tk.RIGHT)

        log_frame = ttk.Frame(self.frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 5))
        log_header = ttk.Frame(log_frame)
        log_header.pack(fill=tk.X)
        ttk.Label(log_header, text="Build Log:").pack(side=tk.LEFT)
        ttk.Button(log_header, text="Clear", command=self._clear_log).pack(side=tk.RIGHT)
        self.log_text = scrolledtext.ScrolledText(log_frame, width=85, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def select_executable(self):
        path = filedialog.askopenfilename(title="Select executable", filetypes=[("All files", "*")])
        if path:
            self.exe_entry.delete(0, tk.END)
            self.exe_entry.insert(0, path)
            if not self.name_entry.get():
                name = os.path.splitext(os.path.basename(path))[0]
                self.name_entry.insert(0, name)

    def select_icon(self):
        path = filedialog.askopenfilename(title="Select icon", filetypes=[("PNG files", "*.png")])
        if path:
            self.icon_entry.delete(0, tk.END)
            self.icon_entry.insert(0, path)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.frame.update_idletasks()
        self.mediator.update_status(message)

    def _clear_log(self):
        self.log_text.delete("1.0", tk.END)

    def _update_linuxdeploy_status(self):
        if self.linuxdeploy.is_available():
            self.linuxdeploy_status_label.config(text="linuxdeploy: available", foreground="green")
            self.install_linuxdeploy_button.config(state=tk.DISABLED)
        else:
            self.linuxdeploy_status_label.config(text="linuxdeploy: not found", foreground="red")
            self.install_linuxdeploy_button.config(state=tk.NORMAL)

    def _save_config(self):
        path = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
        )
        if path:
            self._save_config_to_file(path)

    def _save_config_to_file(self, path):
        config = {
            'name': self.name_entry.get(),
            'version': self.version_entry.get(),
            'category': self.category_var.get(),
            'comment': self.comment_entry.get(),
            'executable_path': self.exe_entry.get(),
            'icon_path': self.icon_entry.get(),
        }
        try:
            with open(path, 'w') as f:
                json.dump(config, f, indent=2)
            self.log_message(f"Configuration saved to {path}")
        except (OSError, IOError) as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{e}")

    def _load_config(self):
        path = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json")],
        )
        if path:
            self._load_config_from_file(path)

    def _load_config_from_file(self, path):
        try:
            with open(path, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            messagebox.showerror("Error", f"Invalid JSON file:\n{e}")
            return
        except (OSError, IOError) as e:
            messagebox.showerror("Error", f"Failed to read file:\n{e}")
            return

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, str(config.get('name', '')))

        self.version_entry.delete(0, tk.END)
        self.version_entry.insert(0, str(config.get('version', '')))

        self.category_var.set(config.get('category', ''))

        self.comment_entry.delete(0, tk.END)
        self.comment_entry.insert(0, str(config.get('comment', '')))

        self.exe_entry.delete(0, tk.END)
        self.exe_entry.insert(0, str(config.get('executable_path', '')))

        self.icon_entry.delete(0, tk.END)
        self.icon_entry.insert(0, str(config.get('icon_path', '')))

        self.log_message(f"Configuration loaded from {path}")

    def _prompt_install_linuxdeploy(self):
        if self.linuxdeploy.is_available():
            messagebox.showinfo("Info", "linuxdeploy is already installed.")
            self._update_linuxdeploy_status()
            return

        if not messagebox.askyesno(
            "Install linuxdeploy",
            "linuxdeploy is not installed. Download and install it now?"
        ):
            return

        success = self.linuxdeploy.install(log_callback=self.log_message)
        if not success:
            messagebox.showerror("Error", "linuxdeploy installation failed. Check the log for details.")
        self._update_linuxdeploy_status()

    def _set_build_state(self, building: bool):
        state = tk.DISABLED if building else tk.NORMAL
        self.generate_button.config(state=state)
        self.cancel_button.config(state=tk.NORMAL if building else tk.DISABLED)

    def _cancel_build(self):
        if self._build_process and self._build_process.poll() is None:
            self.log_message("Cancelling build...")
            self._build_process.terminate()
            try:
                self._build_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._build_process.kill()
        if self._builder:
            self._builder.cleanup()
            self._builder = None
        self._build_process = None
        self._set_build_state(False)
        self.log_message("Build cancelled.")

    def _run_build(self):
        try:
            self._execute_build()
        except Exception as e:
            self.log_message(f"Unexpected error: {e}")
            messagebox.showerror("Error", f"Build failed:\n{e}")
        finally:
            self._build_process = None
            self._build_thread = None
            self.frame.after(0, lambda: self._set_build_state(False))

    def build_appimage(self):
        if self._build_thread and self._build_thread.is_alive():
            return

        exe = self.exe_entry.get().strip()
        icon = self.icon_entry.get().strip()
        name = self.name_entry.get().strip()
        version = self.version_entry.get().strip() or DEFAULT_APP_VERSION
        category = self.category_var.get().strip()
        comment = self.comment_entry.get().strip()

        if not all([exe, icon, name, category]):
            messagebox.showerror("Error", "Please complete all required fields.")
            return

        if not os.path.exists(exe):
            messagebox.showerror("Error", f"Executable file not found: {exe}")
            return
        if not os.path.exists(icon):
            messagebox.showerror("Error", f"Icon file not found: {icon}")
            return

        self._clear_log()
        self._set_build_state(True)

        self._build_thread = threading.Thread(target=self._run_build, daemon=True)
        self._build_thread.start()

    def _execute_build(self):
        exe = self.exe_entry.get().strip()
        icon = self.icon_entry.get().strip()
        name = self.name_entry.get().strip()
        version = self.version_entry.get().strip() or DEFAULT_APP_VERSION
        category = self.category_var.get().strip()
        comment = self.comment_entry.get().strip()

        config = BuildConfig(
            name=name,
            version=version,
            category=category,
            comment=comment,
            executable_path=Path(exe),
            icon_path=Path(icon),
        )

        desktop_content = self.desktop_handler.generate(config)
        self.frame.after(0, lambda: self.mediator.set_desktop_content(desktop_content))

        validation = self.desktop_handler.validate(desktop_content)
        if not validation.is_valid:
            self.log_message(f"Desktop file validation failed: {validation.summary}")
            return

        dependencies = self.mediator.get_dependencies()

        self._builder = AppDirBuilder(base_dir=Path.cwd())
        self._appdir_path = self._builder.create(config)

        self.log_message(f"Creating AppDir in {self._appdir_path}")

        self._builder.add_executable(config.executable_path)
        self._builder.add_icon(config.icon_path, name)
        desktop_path = self._builder.create_desktop_file(config, desktop_content)
        self.log_message(f"Desktop file created at {desktop_path}")

        apprun_path = self._builder.create_apprun_script(config.executable_path.name)
        self.log_message(f"AppRun created at {apprun_path}")

        for dep in dependencies:
            dep_path = Path(dep)
            if dep_path.exists():
                dest = self._builder.appdir_path / "usr" / "lib" / dep_path.name
                shutil.copy2(dep_path, dest)
                self.log_message(f"Added dependency: {dep_path.name}")

        if not self.linuxdeploy.ensure_available(log_callback=self.log_message):
            self.log_message("linuxdeploy not found. Please install it to create AppImages.")
            self._builder.cleanup()
            self._builder = None
            return

        self.log_message("Running linuxdeploy to detect dependencies...")
        cmd = [
            "linuxdeploy",
            "--appdir", str(self._appdir_path),
            "--output", "appimage",
            "--executable", str(self._appdir_path / "usr/bin" / config.executable_path.name),
            "--icon-file", str(self._appdir_path / "usr/share/icons/hicolor/256x256/apps" / f"{name}.png"),
        ]

        for dep in dependencies:
            dep_path = Path(dep)
            if dep_path.exists():
                cmd.extend(["--library", str(dep_path)])

        self.log_message(f"Executing: {' '.join(cmd)}")
        self._build_process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        )

        output = ""
        for line in iter(self._build_process.stdout.readline, ''):
            if line:
                output += line
                self.frame.after(0, lambda m=line.strip(): self.log_message(m))
        self._build_process.stdout.close()
        self._build_process.wait()

        if self._build_process.returncode != 0:
            self.log_message("Error during AppImage creation.")
            if "contains an unregistered value" in output:
                self.log_message("It seems there's an issue with the desktop file categories.")
                self.log_message("Please check the Desktop File Validator tab for details.")
            self._builder.cleanup()
            self._builder = None
            return

        self.log_message("AppImage generated successfully!")
        self.frame.after(0, lambda: messagebox.showinfo("Success", "AppImage generated successfully!"))
        self._builder = None
