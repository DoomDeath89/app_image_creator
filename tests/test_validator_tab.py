import unittest
from unittest.mock import MagicMock
import tkinter as tk
from tkinter import ttk
from app.tabs.validator_tab import ValidatorTab

class DummyMediator:
    def update_status(self, msg):
        pass

class TestValidatorTab(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.notebook = ttk.Notebook(self.root)
        self.mediator = DummyMediator()
        self.tab = ValidatorTab(self.notebook, self.mediator)

    def tearDown(self):
        self.root.destroy()

    def test_insert_sample_desktop(self):
        # Prueba que se inserta el archivo desktop de ejemplo
        content = self.tab.desktop_text.get("1.0", "end")
        self.assertIn("[Desktop Entry]", content)
        self.assertIn("Name=My Application", content)

    def test_validate_desktop_file_valid(self):
        # Prueba la validación de un archivo desktop válido
        self.tab.desktop_text.delete("1.0", "end")
        self.tab.desktop_text.insert("1.0", "[Desktop Entry]\nName=Test\nExec=test\nType=Application\nCategories=Utility;")
        result = self.tab.validate_desktop_file()
        self.assertTrue(result)

    def test_validate_desktop_file_missing_field(self):
        # Prueba la validación de un archivo desktop con campos faltantes
        self.tab.desktop_text.delete("1.0", "end")
        self.tab.desktop_text.insert("1.0", "[Desktop Entry]\nExec=test\nType=Application\nCategories=Utility;")
        result = self.tab.validate_desktop_file()
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
