import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import shutil


class AppImageBuilderTk:
    def __init__(self, root):
        self.root = root
        self.root.title("AppImage Builder")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))

        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="AppImage Builder", style='Header.TLabel')
        title_label.pack(pady=(0, 10))

        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # Build Tab
        build_frame = ttk.Frame(notebook, padding="10")
        notebook.add(build_frame, text="Build AppImage")

        # Executable
        exe_frame = ttk.Frame(build_frame)
        exe_frame.pack(fill=tk.X, pady=5)
        ttk.Label(exe_frame, text="Executable:").pack(anchor=tk.W)
        self.exe_entry = ttk.Entry(exe_frame, width=70)
        self.exe_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(exe_frame, text="Browse", command=self.select_executable).pack(side=tk.RIGHT)

        # Icon
        icon_frame = ttk.Frame(build_frame)
        icon_frame.pack(fill=tk.X, pady=5)
        ttk.Label(icon_frame, text="Icon (.png):").pack(anchor=tk.W)
        self.icon_entry = ttk.Entry(icon_frame, width=70)
        self.icon_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(icon_frame, text="Browse", command=self.select_icon).pack(side=tk.RIGHT)

        # Metadata
        metadata_frame = ttk.Frame(build_frame)
        metadata_frame.pack(fill=tk.X, pady=5)

        ttk.Label(metadata_frame, text="App Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(metadata_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(5, 20))

        ttk.Label(metadata_frame, text="Version:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.version_entry = ttk.Entry(metadata_frame, width=15)
        self.version_entry.grid(row=0, column=3, sticky=tk.W, pady=2, padx=5)

        ttk.Label(metadata_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(metadata_frame, width=28, textvariable=self.category_var,
                                           values=["Game", "Utility", "Development", "AudioVideo", "Audio", "Video",
                                                   "Graphics", "Office", "Network", "Education", "System"])
        self.category_combo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(5, 20))
        self.category_combo.set("Game")

        ttk.Label(metadata_frame, text="Comment:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.comment_entry = ttk.Entry(metadata_frame, width=15)
        self.comment_entry.grid(row=1, column=3, sticky=tk.W, pady=2, padx=5)
        self.comment_entry.insert(0, "App created with AppImage Builder")

        # Generate button
        button_frame = ttk.Frame(build_frame)
        button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Generate AppImage", command=self.build_appimage).pack()

        # linuxdeploy status and installer
        linuxdeploy_frame = ttk.Frame(build_frame)
        linuxdeploy_frame.pack(fill=tk.X, pady=5)
        self.linuxdeploy_status_label = ttk.Label(linuxdeploy_frame, text="")
        self.linuxdeploy_status_label.pack(side=tk.LEFT)
        self.install_linuxdeploy_button = ttk.Button(
            linuxdeploy_frame,
            text="Install linuxdeploy",
            command=self.prompt_install_linuxdeploy
        )
        self.install_linuxdeploy_button.pack(side=tk.RIGHT)

        # Log
        ttk.Label(build_frame, text="Build Log:").pack(anchor=tk.W, pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(build_frame, width=85, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Desktop File Validator Tab
        validator_frame = ttk.Frame(notebook, padding="10")
        notebook.add(validator_frame, text="Desktop File Validator")

        ttk.Label(validator_frame, text="Desktop File Content:").pack(anchor=tk.W, pady=(0, 5))
        self.desktop_text = scrolledtext.ScrolledText(validator_frame, width=85, height=12)
        self.desktop_text.pack(fill=tk.BOTH, expand=True)

        # Add sample desktop file
        sample_desktop = """[Desktop Entry]
Name=My Application
Exec=myapp
Icon=myapp
Type=Application
Categories=Utility;
Comment=A sample application
"""
        self.desktop_text.insert(tk.END, sample_desktop)

        # Validation button and result
        validator_btn_frame = ttk.Frame(validator_frame)
        validator_btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(validator_btn_frame, text="Validate Desktop File",
                   command=self.validate_desktop_file).pack(side=tk.LEFT)
        self.validation_result = ttk.Label(validator_btn_frame, text="", foreground="red")
        self.validation_result.pack(side=tk.LEFT, padx=10)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Set focus to first field
        self.exe_entry.focus()

        self.update_linuxdeploy_status()

    def select_executable(self):
        path = filedialog.askopenfilename(title="Select executable", filetypes=[("All files", "*")])
        if path:
            self.exe_entry.delete(0, tk.END)
            self.exe_entry.insert(0, path)

            # Suggest a name based on the executable filename
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
        self.root.update()
        self.status_var.set(message)

    def validate_desktop_file(self):
        content = self.desktop_text.get("1.0", tk.END)
        lines = content.split('\n')
        errors = []
        warnings = []

        # Check for required fields
        required_fields = ['Name', 'Exec', 'Type', 'Categories']
        present_fields = []

        for line in lines:
            line = line.strip()
            if '=' in line:
                key = line.split('=')[0].strip()
                if key in required_fields:
                    present_fields.append(key)

                # Validate Categories field
                if key == 'Categories':
                    value = line.split('=')[1].strip()
                    if value.endswith(';'):
                        value = value[:-1]
                    if value not in ['Game', 'Utility', 'Development', 'AudioVideo', 'Audio', 'Video',
                                     'Graphics', 'Office', 'Network', 'Education', 'System']:
                        warnings.append(
                            f"Category '{value}' is not a standard category. Consider using one of the standard categories.")

        # Check for missing required fields
        for field in required_fields:
            if field not in present_fields:
                errors.append(f"Missing required field: {field}")

        # Show results
        if errors:
            self.validation_result.config(text="Validation FAILED: " + "; ".join(errors), foreground="red")
        elif warnings:
            self.validation_result.config(text="Validation PASSED with warnings: " + "; ".join(warnings),
                                          foreground="orange")
        else:
            self.validation_result.config(text="Validation PASSED", foreground="green")

        return len(errors) == 0

    def run_command(self, cmd):
        self.log_message(f"Executing: {' '.join(cmd)}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = ""
        for line in iter(process.stdout.readline, ''):
            if line:
                output += line
                self.log_message(line.strip())
        process.stdout.close()
        process.wait()
        return process.returncode, output

    def update_linuxdeploy_status(self):
        available = shutil.which("linuxdeploy") is not None
        if available:
            self.linuxdeploy_status_label.config(text="linuxdeploy: available", foreground="green")
            self.install_linuxdeploy_button.config(state=tk.DISABLED)
        else:
            self.linuxdeploy_status_label.config(text="linuxdeploy: not found", foreground="red")
            self.install_linuxdeploy_button.config(state=tk.NORMAL)

    def get_linuxdeploy_url(self):
        arch = platform.machine().lower()
        if arch in {"aarch64", "arm64"}:
            return "https://github.com/linuxdeploy/linuxdeploy/releases/download/1-alpha-20250213-2/linuxdeploy-aarch64.AppImage"
        if arch in {"x86_64", "amd64"}:
            return "https://github.com/linuxdeploy/linuxdeploy/releases/download/1-alpha-20250213-2/linuxdeploy-x86_64.AppImage"
        return None

    def prompt_install_linuxdeploy(self):
        if self.ensure_linuxdeploy_available(show_already_installed=True):
            return

    def ensure_linuxdeploy_available(self, show_already_installed=False):
        if shutil.which("linuxdeploy"):
            if show_already_installed:
                messagebox.showinfo("Info", "linuxdeploy is already installed.")
            self.update_linuxdeploy_status()
            return True

        if not messagebox.askyesno(
            "Install linuxdeploy",
            "linuxdeploy is not installed. Download and install it now?"
        ):
            return False

        return self.install_linuxdeploy()

    def install_linuxdeploy(self):
        url = self.get_linuxdeploy_url()
        if not url:
            messagebox.showerror(
                "Error",
                "Unsupported CPU architecture for automatic install."
            )
            return False

        if not shutil.which("pkexec"):
            messagebox.showerror(
                "Error",
                "pkexec not found. Install policykit or run install_appimage_tools.sh manually."
            )
            return False

        self.log_message("Installing linuxdeploy...")
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
        ret, output = self.run_command(install_cmd)
        if ret != 0:
            self.log_message("linuxdeploy installation failed.")
            messagebox.showerror("Error", "linuxdeploy installation failed. Check the log for details.")
            return False

        self.log_message("linuxdeploy installed successfully.")
        self.update_linuxdeploy_status()
        return True

    def build_appimage(self):
        exe = self.exe_entry.get().strip()
        icon = self.icon_entry.get().strip()
        name = self.name_entry.get().strip()
        version = self.version_entry.get().strip() or "1.0"
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

        # Validate the desktop file content before proceeding
        desktop_content = f"""[Desktop Entry]
Name={name}
Exec={name}
Icon={name}
Type=Application
Categories={category};
Comment={comment}
Version={version}
"""
        self.desktop_text.delete("1.0", tk.END)
        self.desktop_text.insert(tk.END, desktop_content)

        if not self.validate_desktop_file():
            messagebox.showerror("Error", "Desktop file validation failed. Please fix the errors before building.")
            return

        appdir = f"{name}.AppDir"
        self.log_message(f"Creating AppDir in {appdir}")

        # Remove existing AppDir if it exists
        if os.path.exists(appdir):
            shutil.rmtree(appdir)

        os.makedirs(f"{appdir}/usr/bin", exist_ok=True)
        os.makedirs(f"{appdir}/usr/share/icons/hicolor/256x256/apps", exist_ok=True)
        os.makedirs(f"{appdir}/usr/share/applications", exist_ok=True)

        # Copy executable and icon
        exe_name = os.path.basename(exe)
        self.run_command(["cp", exe, f"{appdir}/usr/bin/"])
        self.run_command(["cp", icon, f"{appdir}/usr/share/icons/hicolor/256x256/apps/{name}.png"])

        # Create desktop file
        desktop_path = f"{appdir}/usr/share/applications/{name}.desktop"
        with open(desktop_path, "w") as f:
            f.write(desktop_content)
        self.log_message(f"Desktop file created at {desktop_path}")

        # Create AppRun
        apprun_content = f"""#!/bin/bash
HERE="$(dirname "$(readlink -f "${{0}}")")"
export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"
exec "$HERE/usr/bin/{exe_name}" "$@"
"""
        apprun_path = f"{appdir}/AppRun"
        with open(apprun_path, "w") as f:
            f.write(apprun_content)
        self.run_command(["chmod", "+x", apprun_path])
        self.log_message(f"AppRun created at {apprun_path}")

        # Check if linuxdeploy is available
        if not shutil.which("linuxdeploy"):
            self.log_message("linuxdeploy not found in PATH.")
            if not self.ensure_linuxdeploy_available():
                messagebox.showerror("Error", "linuxdeploy not found. Please install it to create AppImages.")
                return

        # Run linuxdeploy
        self.log_message("Running linuxdeploy to detect dependencies...")
        ret, output = self.run_command([
            "linuxdeploy",
            "--appdir", appdir,
            "--output", "appimage",
            "--executable", f"{appdir}/usr/bin/{exe_name}",
            "--icon-file", f"{appdir}/usr/share/icons/hicolor/256x256/apps/{name}.png"
        ])

        if ret != 0:
            self.log_message("Error during AppImage creation.")
            if "contains an unregistered value" in output:
                self.log_message("It seems there's an issue with the desktop file categories.")
                self.log_message("Please check the Desktop File Validator tab for details.")
            return

        self.log_message("AppImage generated successfully!")
        messagebox.showinfo("Success", "AppImage generated successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppImageBuilderTk(root)
    root.mainloop()
