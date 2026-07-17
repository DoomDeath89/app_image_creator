import unittest
from unittest.mock import MagicMock
import tkinter as tk
from tkinter import ttk
from app.tabs.validator_tab import ValidatorTab
from app.core.mediator import Mediator


class TestValidatorTab(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.notebook = ttk.Notebook(self.root)
        self.mediator = MagicMock(spec=Mediator)
        self.tab = ValidatorTab(self.notebook, self.mediator)

    def tearDown(self):
        self.root.destroy()

    def test_insert_sample_desktop(self):
        content = self.tab.get_content()
        self.assertIn("[Desktop Entry]", content)
        self.assertIn("Name=My Application", content)

    def test_set_content(self):
        new_content = "[Desktop Entry]\nName=NewApp\nExec=newapp\nType=Application\nCategories=Utility;"
        self.tab.set_content(new_content)
        content = self.tab.get_content()
        self.assertIn("Name=NewApp", content)

    def test_validate_valid(self):
        self.tab.set_content(
            "[Desktop Entry]\nName=Test\nExec=test\nType=Application\nCategories=Utility;"
        )
        result = self.tab.validate()
        self.assertTrue(result.is_valid)

    def test_validate_missing_field(self):
        self.tab.set_content("[Desktop Entry]\nExec=test\nType=Application\nCategories=Utility;")
        result = self.tab.validate()
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
