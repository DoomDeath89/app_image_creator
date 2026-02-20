import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import shutil
from app.tabs.dependencies_tab import DependenciesTab
from app.tabs.build_tab import BuildTab
from app.tabs.validator_tab import ValidatorTab

class AppImageBuilderMediator:
    def __init__(self):
        self.build_tab = None
        self.validator_tab = None
        self.dependencies_tab = None
        self.status_var = None

    def register_build_tab(self, build_tab):
        self.build_tab = build_tab

    def register_validator_tab(self, validator_tab):
        self.validator_tab = validator_tab

    def register_dependencies_tab(self, dependencies_tab):
        self.dependencies_tab = dependencies_tab

    def update_status(self, message):
        if self.status_var:
            self.status_var.set(message)

    def get_desktop_content(self):
        if self.validator_tab:
            return self.validator_tab.desktop_text.get("1.0", tk.END)
        return ""

    def validate_desktop_file(self):
        if self.validator_tab:
            return self.validator_tab.validate_desktop_file()
        return False

    def get_dependencies(self):
        if self.dependencies_tab:
            return self.dependencies_tab.get_dependencies()
        return []

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

        # Mediator
        self.mediator = AppImageBuilderMediator()

        # Build Tab (modular)
        self.build_tab = BuildTab(notebook, self.mediator)
        self.mediator.register_build_tab(self.build_tab)

        # Desktop File Validator Tab (modular)
        self.validator_tab = ValidatorTab(notebook, self.mediator)
        self.mediator.register_validator_tab(self.validator_tab)

        # Dependencies Tab (modular)
        self.dependencies_tab = DependenciesTab(notebook, self.mediator)
        self.mediator.register_dependencies_tab(self.dependencies_tab)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.mediator.status_var = self.status_var
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppImageBuilderTk(root)
    root.mainloop()
