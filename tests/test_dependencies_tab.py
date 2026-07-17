import unittest
from unittest.mock import MagicMock
import tkinter as tk
from tkinter import ttk
from app.tabs.dependencies_tab import DependenciesTab
from app.core.mediator import Mediator


class TestDependenciesTab(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.notebook = ttk.Notebook(self.root)
        self.mediator = MagicMock(spec=Mediator)
        self.tab = DependenciesTab(self.notebook, self.mediator)

    def tearDown(self):
        self.root.destroy()

    def test_add_dependency(self):
        self.tab.deps_listbox.insert(0, "libn64.so")
        deps = self.tab.get_dependencies()
        self.assertIn("libn64.so", deps)

    def test_clear_dependencies(self):
        self.tab.deps_listbox.insert(0, "libn64.so")
        self.tab.clear_dependencies()
        deps = self.tab.get_dependencies()
        self.assertEqual(deps, [])

    def test_sort_dependencies(self):
        self.tab.deps_listbox.insert(0, "libz.so")
        self.tab.deps_listbox.insert(0, "liba.so")
        self.tab.sort_dependencies()
        deps = self.tab.get_dependencies()
        self.assertEqual(deps, sorted(deps))

    def test_set_dependencies(self):
        self.tab.set_dependencies(["liba.so", "libb.so"])
        deps = self.tab.get_dependencies()
        self.assertEqual(deps, ["liba.so", "libb.so"])

    def test_remove_selected(self):
        self.tab.deps_listbox.insert(0, "liba.so")
        self.tab.deps_listbox.insert(0, "libb.so")
        self.tab.deps_listbox.select_set(0)
        self.tab.remove_selected_dependency()
        deps = self.tab.get_dependencies()
        self.assertEqual(deps, ["liba.so"])


if __name__ == "__main__":
    unittest.main()
