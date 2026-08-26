import json
import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
import tkinter as tk
from tkinter import ttk
from app.tabs.build_tab import BuildTab
from app.core.mediator import Mediator


class TestBuildTab(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack()
        self.mediator = MagicMock(spec=Mediator)
        self.tab = BuildTab(self.notebook, self.mediator)

    def tearDown(self):
        self.root.destroy()

    def test_select_executable(self):
        self.tab.exe_entry.insert(0, "test.exe")
        self.tab.name_entry.delete(0, "end")
        self.tab.select_executable = MagicMock()
        self.tab.select_executable()
        self.tab.select_executable.assert_called()

    def test_select_icon(self):
        self.tab.icon_entry.insert(0, "test.png")
        self.tab.select_icon = MagicMock()
        self.tab.select_icon()
        self.tab.select_icon.assert_called()

    def test_log_message(self):
        self.tab.log_message("Test log")
        content = self.tab.log_text.get("1.0", tk.END)
        self.assertIn("Test log", content)
        self.mediator.update_status.assert_called_with("Test log")

    def test_update_linuxdeploy_status(self):
        self.tab._update_linuxdeploy_status()
        status_text = self.tab.linuxdeploy_status_label.cget("text")
        self.assertIn("linuxdeploy", status_text)

    def test_clear_log(self):
        self.tab.log_message("test line")
        self.tab._clear_log()
        content = self.tab.log_text.get("1.0", tk.END).strip()
        self.assertEqual(content, "")

    def test_set_build_state(self):
        self.tab._set_build_state(True)
        self.assertEqual(str(self.tab.generate_button.cget("state")), "disabled")
        self.assertEqual(str(self.tab.cancel_button.cget("state")), "normal")

        self.tab._set_build_state(False)
        self.assertEqual(str(self.tab.generate_button.cget("state")), "normal")
        self.assertEqual(str(self.tab.cancel_button.cget("state")), "disabled")


class TestSaveLoadConfig(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack()
        self.mediator = MagicMock(spec=Mediator)
        self.tab = BuildTab(self.notebook, self.mediator)

    def tearDown(self):
        self.root.destroy()

    def test_save_config_creates_valid_json(self):
        self.tab.name_entry.insert(0, "MyApp")
        self.tab.version_entry.insert(0, "1.0")
        self.tab.category_combo.set("Game")
        self.tab.comment_entry.delete(0, tk.END)
        self.tab.comment_entry.insert(0, "Test comment")
        self.tab.exe_entry.insert(0, "/usr/bin/myapp")
        self.tab.icon_entry.insert(0, "/usr/share/icon.png")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmp_path = f.name

        try:
            self.tab._save_config_to_file(tmp_path)

            with open(tmp_path, 'r') as f:
                data = json.load(f)

            self.assertEqual(data['name'], 'MyApp')
            self.assertEqual(data['version'], '1.0')
            self.assertEqual(data['category'], 'Game')
            self.assertEqual(data['comment'], 'Test comment')
            self.assertEqual(data['executable_path'], '/usr/bin/myapp')
            self.assertEqual(data['icon_path'], '/usr/share/icon.png')
        finally:
            os.unlink(tmp_path)

    def test_load_config_populates_fields(self):
        config = {
            'name': 'LoadedApp',
            'version': '2.0',
            'category': 'Utility',
            'comment': 'Loaded comment',
            'executable_path': '/usr/bin/loaded',
            'icon_path': '/usr/share/loaded.png'
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            tmp_path = f.name

        try:
            self.tab._load_config_from_file(tmp_path)

            self.assertEqual(self.tab.name_entry.get(), 'LoadedApp')
            self.assertEqual(self.tab.version_entry.get(), '2.0')
            self.assertEqual(self.tab.category_var.get(), 'Utility')
            self.assertEqual(self.tab.comment_entry.get(), 'Loaded comment')
            self.assertEqual(self.tab.exe_entry.get(), '/usr/bin/loaded')
            self.assertEqual(self.tab.icon_entry.get(), '/usr/share/loaded.png')
        finally:
            os.unlink(tmp_path)

    def test_load_config_handles_missing_fields(self):
        config = {'name': 'PartialApp'}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            tmp_path = f.name

        try:
            self.tab._load_config_from_file(tmp_path)

            self.assertEqual(self.tab.name_entry.get(), 'PartialApp')
            self.assertEqual(self.tab.version_entry.get(), '')
        finally:
            os.unlink(tmp_path)

    def test_load_config_handles_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("not valid json {{{")
            tmp_path = f.name

        try:
            with patch('app.tabs.build_tab.messagebox') as mock_mb:
                self.tab._load_config_from_file(tmp_path)
                mock_mb.showerror.assert_called_once()
        finally:
            os.unlink(tmp_path)

    def test_save_config_handles_write_error(self):
        with patch('builtins.open', side_effect=OSError("Permission denied")):
            with patch('app.tabs.build_tab.messagebox') as mock_mb:
                self.tab._save_config_to_file("/impossible/path.json")
                mock_mb.showerror.assert_called_once()


if __name__ == "__main__":
    unittest.main()
