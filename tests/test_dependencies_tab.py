import unittest
from unittest.mock import MagicMock
import tkinter as tk
from tkinter import ttk
from app.tabs.dependencies_tab import DependenciesTab

class DummyMediator:
    pass

class TestDependenciesTab(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.notebook = ttk.Notebook(self.root)
        self.mediator = DummyMediator()
        self.tab = DependenciesTab(self.notebook, self.mediator)

    def tearDown(self):
        self.root.destroy()

    def test_add_dependency(self):
        # Prueba agregar una dependencia a la lista
        self.tab.deps_listbox.insert(0, "libn64.so")
        deps = self.tab.get_dependencies()
        self.assertIn("libn64.so", deps)

    def test_clear_dependencies(self):
        # Prueba limpiar todas las dependencias
        self.tab.deps_listbox.insert(0, "libn64.so")
        self.tab.clear_dependencies()
        deps = self.tab.get_dependencies()
        self.assertEqual(deps, [])

    def test_sort_dependencies(self):
        # Prueba ordenar la lista de dependencias
        self.tab.deps_listbox.insert(0, "libz.so")
        self.tab.deps_listbox.insert(0, "liba.so")
        self.tab.sort_dependencies()
        deps = self.tab.get_dependencies()
        self.assertEqual(deps, sorted(deps))

if __name__ == "__main__":
    unittest.main()
