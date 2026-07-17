import unittest
from pathlib import Path
from app.services.desktop_file_handler import DesktopFileHandler
from app.services.linux_deploy_manager import LinuxDeployManager
from app.services.app_dir_builder import AppDirBuilder
from app.utils.types import BuildConfig, ValidationResult


class TestDesktopFileHandler(unittest.TestCase):
    def setUp(self):
        self.handler = DesktopFileHandler()

    def test_generate_desktop_file(self):
        config = BuildConfig(
            name="MyApp",
            version="1.0",
            category="Utility",
            comment="Test app",
            executable_path=Path("/usr/bin/myapp"),
        )
        content = self.handler.generate(config)
        self.assertIn("[Desktop Entry]", content)
        self.assertIn("Name=MyApp", content)
        self.assertIn("Exec=MyApp", content)
        self.assertIn("Categories=Utility;", content)

    def test_validate_valid_content(self):
        content = (
            "[Desktop Entry]\n"
            "Name=Test\n"
            "Exec=test\n"
            "Type=Application\n"
            "Categories=Utility;\n"
        )
        result = self.handler.validate(content)
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_missing_fields(self):
        content = "[Desktop Entry]\nName=Test\n"
        result = self.handler.validate(content)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 3)

    def test_validate_invalid_category(self):
        content = (
            "[Desktop Entry]\n"
            "Name=Test\n"
            "Exec=test\n"
            "Type=Application\n"
            "Categories=InvalidCategory;\n"
        )
        result = self.handler.validate(content)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.warnings), 1)

    def test_get_sample(self):
        sample = self.handler.get_sample()
        self.assertIn("[Desktop Entry]", sample)
        self.assertIn("Name=My Application", sample)


class TestLinuxDeployManager(unittest.TestCase):
    def setUp(self):
        self.manager = LinuxDeployManager()

    def test_get_url_arm64(self):
        url = self.manager.get_url("aarch64")
        self.assertIn("linuxdeploy", url)
        self.assertIn("aarch64", url)

    def test_get_url_amd64(self):
        url = self.manager.get_url("x86_64")
        self.assertIn("linuxdeploy", url)
        self.assertIn("x86_64", url)

    def test_get_url_unsupported(self):
        url = self.manager.get_url("mips")
        self.assertIsNone(url)

    def test_get_url_normalizes_arch(self):
        url1 = self.manager.get_url("arm64")
        url2 = self.manager.get_url("aarch64")
        self.assertEqual(url1, url2)


class TestAppDirBuilder(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path("/tmp/test_appdir")
        self.builder = AppDirBuilder(self.tmp_dir)

    def test_create_appdir(self):
        config = BuildConfig(
            name="TestApp",
            version="1.0",
            category="Utility",
            comment="Test",
            executable_path=Path("/usr/bin/test"),
        )
        result = self.builder.create(config)
        self.assertEqual(result.name, "TestApp.AppDir")

    def test_build_config_dataclass(self):
        config = BuildConfig(
            name="MyApp",
            version="2.0",
            category="Game",
            comment="A game",
            executable_path=Path("/usr/bin/game"),
        )
        self.assertEqual(config.name, "MyApp")
        self.assertEqual(config.version, "2.0")
        self.assertEqual(config.category, "Game")

    def test_validation_result_summary(self):
        result = ValidationResult(is_valid=True)
        self.assertEqual(result.summary, "Validation PASSED")

    def test_validation_result_with_errors(self):
        result = ValidationResult(is_valid=False, errors=["Missing field"])
        self.assertEqual(result.summary, "Validation FAILED: Missing field")

    def test_validation_result_with_warnings(self):
        result = ValidationResult(is_valid=True, warnings=["Unknown category"])
        self.assertEqual(result.summary, "Validation PASSED with warnings: Unknown category")


if __name__ == "__main__":
    unittest.main()
