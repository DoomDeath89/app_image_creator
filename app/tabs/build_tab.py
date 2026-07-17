import json
import os
import subprocess
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
        ttk.Button(button_frame, text="Generate AppImage", command=self.build_appimage).pack(side=tk.LEFT)

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

        ttk.Label(self.frame, text="Build Log:").pack(anchor=tk.W, pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(self.frame, width=85, height=15)
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
        self.frame.update()
        self.mediator.update_status(message)

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
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)

    def _load_config(self):
        path = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json")],
        )
        if path:
            self._load_config_from_file(path)

    def _load_config_from_file(self, path):
        with open(path, 'r') as f:
            config = json.load(f)

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, config.get('name', ''))

        self.version_entry.delete(0, tk.END)
        self.version_entry.insert(0, config.get('version', ''))

        self.category_var.set(config.get('category', ''))

        self.comment_entry.delete(0, tk.END)
        self.comment_entry.insert(0, config.get('comment', ''))

        self.exe_entry.delete(0, tk.END)
        self.exe_entry.insert(0, config.get('executable_path', ''))

        self.icon_entry.delete(0, tk.END)
        self.icon_entry.insert(0, config.get('icon_path', ''))

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

    def build_appimage(self):
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

        config = BuildConfig(
            name=name,
            version=version,
            category=category,
            comment=comment,
            executable_path=Path(exe),
            icon_path=Path(icon),
        )

        desktop_content = self.desktop_handler.generate(config)
        self.mediator.set_desktop_content(desktop_content)

        validation = self.mediator.validate_desktop_file()
        if not validation.is_valid:
            messagebox.showerror("Error", "Desktop file validation failed. Please fix the errors before building.")
            return

        dependencies = self.mediator.get_dependencies()

        builder = AppDirBuilder(base_dir=Path.cwd())
        appdir = builder.create(config)

        self.log_message(f"Creating AppDir in {appdir}")

        builder.add_executable(config.executable_path)
        builder.add_icon(config.icon_path, name)
        desktop_path = builder.create_desktop_file(config, desktop_content)
        self.log_message(f"Desktop file created at {desktop_path}")

        apprun_path = builder.create_apprun_script(config.executable_path.name)
        self.log_message(f"AppRun created at {apprun_path}")

        if not self.linuxdeploy.ensure_available(log_callback=self.log_message):
            messagebox.showerror("Error", "linuxdeploy not found. Please install it to create AppImages.")
            return

        self.log_message("Running linuxdeploy to detect dependencies...")
        cmd = [
            "linuxdeploy",
            "--appdir", str(appdir),
            "--output", "appimage",
            "--executable", str(appdir / "usr/bin" / config.executable_path.name),
            "--icon-file", str(appdir / "usr/share/icons/hicolor/256x256/apps" / f"{name}.png"),
        ]

        self.log_message(f"Executing: {' '.join(cmd)}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = ""
        for line in iter(process.stdout.readline, ''):
            if line:
                output += line
                self.log_message(line.strip())
        process.stdout.close()
        process.wait()

        if process.returncode != 0:
            self.log_message("Error during AppImage creation.")
            if "contains an unregistered value" in output:
                self.log_message("It seems there's an issue with the desktop file categories.")
                self.log_message("Please check the Desktop File Validator tab for details.")
            return

        self.log_message("AppImage generated successfully!")
        messagebox.showinfo("Success", "AppImage generated successfully!")
