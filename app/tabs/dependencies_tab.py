import tkinter as tk
from tkinter import ttk
import os

class DependenciesTab:
    def __init__(self, notebook, mediator):
        self.mediator = mediator
        self.frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.frame, text="Dependencies")

        entry_frame = ttk.Frame(self.frame)
        entry_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(entry_frame, text="Add Dependency:").pack(side=tk.LEFT, padx=(0, 5))
        self.deps_entry = ttk.Entry(entry_frame, width=40)
        self.deps_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(entry_frame, text="Add", command=self.select_dependencies).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(entry_frame, text="Sort", command=self.sort_dependencies).pack(side=tk.LEFT, padx=(5, 0))

        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 5))
        ttk.Label(list_frame, text="Dependency List:").pack(anchor=tk.W)
        self.deps_listbox = tk.Listbox(list_frame, width=60, height=8, selectmode=tk.EXTENDED)
        self.deps_listbox.pack(fill=tk.BOTH, expand=True)
        btns_frame = ttk.Frame(list_frame)
        btns_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btns_frame, text="Remove Selected", command=self.remove_selected_dependency).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btns_frame, text="Clear All", command=self.clear_dependencies).pack(side=tk.LEFT)

    def select_dependencies(self):
        files = tk.filedialog.askopenfilenames(title="Select dependency files")
        for f in files:
            fname = os.path.basename(f)
            if fname and fname not in self.get_dependencies():
                self.deps_listbox.insert(tk.END, fname)

    def remove_selected_dependency(self):
        selected = self.deps_listbox.curselection()
        for idx in reversed(selected):
            self.deps_listbox.delete(idx)

    def clear_dependencies(self):
        self.deps_listbox.delete(0, tk.END)

    def sort_dependencies(self):
        deps = list(self.deps_listbox.get(0, tk.END))
        self.clear_dependencies()
        for dep in sorted(deps):
            self.deps_listbox.insert(tk.END, dep)

    def get_dependencies(self):
        return list(self.deps_listbox.get(0, tk.END))
