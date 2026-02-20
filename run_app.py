import os
import sys

# Añadir el directorio actual al PYTHONPATH
sys.path.insert(0, os.path.abspath('.'))

from app.core.main import AppImageBuilderTk
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = AppImageBuilderTk(root)
    root.mainloop()
