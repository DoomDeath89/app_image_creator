import tkinter as tk
from app.core.main import AppImageBuilderTk


def main():
    root = tk.Tk()
    AppImageBuilderTk(root)
    root.mainloop()


if __name__ == "__main__":
    main()
