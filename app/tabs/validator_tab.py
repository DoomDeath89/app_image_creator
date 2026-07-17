import tkinter as tk
from tkinter import ttk, scrolledtext

from app.services.desktop_file_handler import DesktopFileHandler
from app.utils.types import ValidationResult


class ValidatorTab:
    def __init__(self, notebook, mediator):
        self.mediator = mediator
        self.handler = DesktopFileHandler()
        self.frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.frame, text="Desktop File Validator")

        ttk.Label(self.frame, text="Desktop File Content:").pack(anchor=tk.W, pady=(0, 5))
        self.desktop_text = scrolledtext.ScrolledText(self.frame, width=85, height=12)
        self.desktop_text.pack(fill=tk.BOTH, expand=True)
        self.desktop_text.insert(tk.END, self.handler.get_sample())

        validator_btn_frame = ttk.Frame(self.frame)
        validator_btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(
            validator_btn_frame,
            text="Validate Desktop File",
            command=self._on_validate,
        ).pack(side=tk.LEFT)
        self.validation_result = ttk.Label(validator_btn_frame, text="", foreground="red")
        self.validation_result.pack(side=tk.LEFT, padx=10)

    def get_content(self) -> str:
        return self.desktop_text.get("1.0", tk.END)

    def set_content(self, content: str) -> None:
        self.desktop_text.delete("1.0", tk.END)
        self.desktop_text.insert(tk.END, content)

    def validate(self) -> ValidationResult:
        content = self.get_content()
        result = self.handler.validate(content)
        self.validation_result.config(text=result.summary, foreground=result.color)
        return result

    def _on_validate(self) -> None:
        self.validate()
