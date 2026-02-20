import tkinter as tk
from tkinter import ttk, scrolledtext

class ValidatorTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.frame, text="Desktop File Validator")

        ttk.Label(self.frame, text="Desktop File Content:").pack(anchor=tk.W, pady=(0, 5))
        self.desktop_text = scrolledtext.ScrolledText(self.frame, width=85, height=12)
        self.desktop_text.pack(fill=tk.BOTH, expand=True)

        # Add sample desktop file
        sample_desktop = """[Desktop Entry]\nName=My Application\nExec=myapp\nIcon=myapp\nType=Application\nCategories=Utility;\nComment=A sample application\n"""
        self.desktop_text.insert(tk.END, sample_desktop)

        # Validation button and result
        validator_btn_frame = ttk.Frame(self.frame)
        validator_btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(validator_btn_frame, text="Validate Desktop File",
                   command=self.validate_desktop_file).pack(side=tk.LEFT)
        self.validation_result = ttk.Label(validator_btn_frame, text="", foreground="red")
        self.validation_result.pack(side=tk.LEFT, padx=10)

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
