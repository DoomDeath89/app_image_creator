import tkinter as tk
from tkinter import ttk

from app.core.mediator import Mediator
from app.tabs.build_tab import BuildTab
from app.tabs.validator_tab import ValidatorTab
from app.tabs.dependencies_tab import DependenciesTab


class AppImageBuilderTk:
    def __init__(self, root):
        self.root = root
        self.root.title("AppImage Builder")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="AppImage Builder", style='Header.TLabel')
        title_label.pack(pady=(0, 10))

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        self.mediator = Mediator()

        self.build_tab = BuildTab(notebook, self.mediator)
        self.mediator.register_build_tab(self.build_tab)

        self.validator_tab = ValidatorTab(notebook, self.mediator)
        self.mediator.register_validator_tab(self.validator_tab)

        self.dependencies_tab = DependenciesTab(notebook, self.mediator)
        self.mediator.register_dependencies_tab(self.dependencies_tab)

        self.status_var = tk.StringVar(value="Ready")
        self.mediator.set_status_callback(self.status_var.set)

        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
