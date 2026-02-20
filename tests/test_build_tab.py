import unittest
from unittest.mock import MagicMock
import tkinter as tk
from app.tabs.build_tab import BuildTab

class DummyApp:
    def __init__(self):
        self.status_var = MagicMock()
        self.dependencies_tab = MagicMock()
        self.dependencies_tab.get_dependencies = MagicMock(return_value=["libn64.so"])
        self.desktop_text = MagicMock()
        self.desktop_text.delete = MagicMock()
        self.desktop_text.insert = MagicMock()
        self.validate_desktop_file = MagicMock(return_value=True)

class TestBuildTab(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.notebook = MagicMock()
        self.app = DummyApp()
        self.tab = BuildTab(self.notebook, self.app)

    def tearDown(self):
        self.root.destroy()

    def test_select_executable(self):
        # Prueba la selección de ejecutable
        self.tab.exe_entry.insert(0, "test.exe")
        self.tab.name_entry.delete(0, "end")
        self.tab.select_executable = MagicMock()
        self.tab.select_executable()
        self.tab.select_executable.assert_called()

    def test_select_icon(self):
        # Prueba la selección de icono
        self.tab.icon_entry.insert(0, "test.png")
        self.tab.select_icon = MagicMock()
        self.tab.select_icon()
        self.tab.select_icon.assert_called()

    def test_log_message(self):
        # Prueba el registro de mensajes en el log
        self.tab.log_text.insert = MagicMock()
        self.tab.log_message("Test log")
        self.tab.log_text.insert.assert_called()

    def test_update_linuxdeploy_status(self):
        # Prueba la actualización del estado de linuxdeploy
        self.tab.linuxdeploy_status_label.config = MagicMock()
        self.tab.install_linuxdeploy_button.config = MagicMock()
        self.tab.update_linuxdeploy_status()
        self.tab.linuxdeploy_status_label.config.assert_called()

    def test_run_command(self):
        # Prueba la ejecución de comandos en el sistema
        self.tab.log_message = MagicMock()
        ret, output = self.tab.run_command(["echo", "hello"])
        self.tab.log_message.assert_called()
        self.assertEqual(ret, 0)
        self.assertIn("hello", output)

if __name__ == "__main__":
    unittest.main()
