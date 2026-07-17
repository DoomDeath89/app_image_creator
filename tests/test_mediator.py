import unittest
from unittest.mock import MagicMock
from app.core.mediator import Mediator
from app.utils.types import ValidationResult


class TestMediator(unittest.TestCase):
    def setUp(self):
        self.mediator = Mediator()

    def test_register_tabs(self):
        build_tab = MagicMock()
        validator_tab = MagicMock()
        dependencies_tab = MagicMock()

        self.mediator.register_build_tab(build_tab)
        self.mediator.register_validator_tab(validator_tab)
        self.mediator.register_dependencies_tab(dependencies_tab)

        self.assertIs(self.mediator._build_tab, build_tab)
        self.assertIs(self.mediator._validator_tab, validator_tab)
        self.assertIs(self.mediator._dependencies_tab, dependencies_tab)

    def test_update_status_with_callback(self):
        callback = MagicMock()
        self.mediator.set_status_callback(callback)
        self.mediator.update_status("Ready")
        callback.assert_called_once_with("Ready")

    def test_update_status_without_callback(self):
        self.mediator.update_status("Ready")

    def test_set_desktop_content(self):
        mock_tab = MagicMock()
        self.mediator.register_validator_tab(mock_tab)
        self.mediator.set_desktop_content("test content")
        mock_tab.set_content.assert_called_once_with("test content")

    def test_get_desktop_content(self):
        mock_tab = MagicMock()
        mock_tab.get_content.return_value = "[Desktop Entry]\nName=Test"
        self.mediator.register_validator_tab(mock_tab)
        result = self.mediator.get_desktop_content()
        self.assertEqual(result, "[Desktop Entry]\nName=Test")

    def test_get_desktop_content_no_tab(self):
        result = self.mediator.get_desktop_content()
        self.assertEqual(result, "")

    def test_validate_desktop_file(self):
        expected = ValidationResult(is_valid=True)
        mock_tab = MagicMock()
        mock_tab.validate.return_value = expected
        self.mediator.register_validator_tab(mock_tab)
        result = self.mediator.validate_desktop_file()
        self.assertTrue(result.is_valid)

    def test_validate_desktop_file_no_tab(self):
        result = self.mediator.validate_desktop_file()
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)

    def test_get_dependencies(self):
        mock_tab = MagicMock()
        mock_tab.get_dependencies.return_value = ["liba.so", "libb.so"]
        self.mediator.register_dependencies_tab(mock_tab)
        result = self.mediator.get_dependencies()
        self.assertEqual(result, ["liba.so", "libb.so"])

    def test_get_dependencies_no_tab(self):
        result = self.mediator.get_dependencies()
        self.assertEqual(result, [])

    def test_set_dependencies(self):
        mock_tab = MagicMock()
        self.mediator.register_dependencies_tab(mock_tab)
        self.mediator.set_dependencies(["liba.so"])
        mock_tab.set_dependencies.assert_called_once_with(["liba.so"])


if __name__ == "__main__":
    unittest.main()
