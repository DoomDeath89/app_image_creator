import pytest
from unittest.mock import MagicMock
from app.core.mediator import Mediator


class MockValidatorTab:
    def __init__(self):
        self._content = ""
        self.validation_result = None

    def get_content(self):
        return self._content

    def set_content(self, content):
        self._content = content

    def validate(self):
        return self.validation_result


class MockDependenciesTab:
    def __init__(self, deps=None):
        self._deps = deps or []

    def get_dependencies(self):
        return self._deps

    def set_dependencies(self, deps):
        self._deps = deps


class MockBuildTab:
    pass


@pytest.fixture
def mediator():
    return Mediator()


@pytest.fixture
def mediator_with_tabs():
    m = Mediator()
    m.register_build_tab(MockBuildTab())
    m.register_validator_tab(MockValidatorTab())
    m.register_dependencies_tab(MockDependenciesTab(["liba.so", "libb.so"]))
    return m


@pytest.fixture
def mock_validator_tab():
    return MockValidatorTab()


@pytest.fixture
def mock_dependencies_tab():
    return MockDependenciesTab()
