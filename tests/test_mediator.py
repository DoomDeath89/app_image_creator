import unittest
from unittest.mock import MagicMock
from app.core.main import AppImageBuilderMediator

class DummyTab:
    def __init__(self):
        self.desktop_text = MagicMock()
        self.desktop_text.get = MagicMock(return_value="[Desktop Entry]\nName=Test\nExec=test\nType=Application\nCategories=Utility;")
        self.validate_desktop_file = MagicMock(return_value=True)
        self.get_dependencies = MagicMock(return_value=["libn64.so", "libaudio.so"])
        self.called = False
    def custom_action(self):
        self.called = True
        return "done"

class TestMediator(unittest.TestCase):
    def setUp(self):
        self.mediator = AppImageBuilderMediator()
        self.build_tab = DummyTab()
        self.validator_tab = DummyTab()
        self.dependencies_tab = DummyTab()
        self.mediator.register_build_tab(self.build_tab)
        self.mediator.register_validator_tab(self.validator_tab)
        self.mediator.register_dependencies_tab(self.dependencies_tab)

    def test_get_desktop_content(self):
        # Prueba que el Mediator obtiene el contenido del archivo desktop
        content = self.mediator.get_desktop_content()
        self.assertIn("[Desktop Entry]", content)
        self.assertIn("Name=Test", content)

    def test_validate_desktop_file(self):
        # Prueba que el Mediator valida correctamente el archivo desktop
        result = self.mediator.validate_desktop_file()
        self.assertTrue(result)

    def test_get_dependencies(self):
        # Prueba que el Mediator obtiene la lista de dependencias
        deps = self.mediator.get_dependencies()
        self.assertEqual(deps, ["libn64.so", "libaudio.so"])

    def test_update_status(self):
        # Prueba que el Mediator actualiza el estado global
        status_var = MagicMock()
        self.mediator.status_var = status_var
        self.mediator.update_status("Ready")
        status_var.set.assert_called_with("Ready")

    def test_no_validator_tab(self):
        # Prueba el comportamiento cuando no hay validator_tab
        self.mediator.validator_tab = None
        self.assertEqual(self.mediator.get_desktop_content(), "")
        self.assertFalse(self.mediator.validate_desktop_file())

    def test_no_dependencies_tab(self):
        # Prueba el comportamiento cuando no hay dependencies_tab
        self.mediator.dependencies_tab = None
        self.assertEqual(self.mediator.get_dependencies(), [])

    def test_no_status_var(self):
        # Prueba el comportamiento cuando no hay status_var
        self.mediator.status_var = None
        self.mediator.update_status("Should not fail")
        # No exception should be raised

    def test_register_tabs(self):
        # Prueba el registro de las pestañas en el Mediator
        mediator2 = AppImageBuilderMediator()
        mediator2.register_build_tab(self.build_tab)
        mediator2.register_validator_tab(self.validator_tab)
        mediator2.register_dependencies_tab(self.dependencies_tab)
        self.assertIs(mediator2.build_tab, self.build_tab)
        self.assertIs(mediator2.validator_tab, self.validator_tab)
        self.assertIs(mediator2.dependencies_tab, self.dependencies_tab)

    def test_custom_action_on_tab(self):
        # Prueba una acción personalizada en una pestaña
        self.build_tab.called = False
        result = self.build_tab.custom_action()
        self.assertTrue(self.build_tab.called)
        self.assertEqual(result, "done")

    def test_validator_tab_desktop_text(self):
        # Prueba que el Mediator obtiene el contenido actualizado del desktop
        self.validator_tab.desktop_text.get = MagicMock(return_value="[Desktop Entry]\nName=Changed")
        content = self.mediator.get_desktop_content()
        self.assertIn("Name=Changed", content)

    def test_dependencies_tab_empty(self):
        # Prueba que el Mediator maneja dependencias vacías
        self.dependencies_tab.get_dependencies = MagicMock(return_value=[])
        deps = self.mediator.get_dependencies()
        self.assertEqual(deps, [])

    def test_validator_tab_invalid(self):
        # Prueba que el Mediator detecta un desktop inválido
        self.validator_tab.validate_desktop_file = MagicMock(return_value=False)
        result = self.mediator.validate_desktop_file()
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
