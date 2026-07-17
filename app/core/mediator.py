from typing import List, Optional, TYPE_CHECKING

from app.utils.types import ValidationResult

if TYPE_CHECKING:
    from app.tabs.build_tab import BuildTab
    from app.tabs.validator_tab import ValidatorTab
    from app.tabs.dependencies_tab import DependenciesTab


class Mediator:
    def __init__(self):
        self._build_tab: Optional['BuildTab'] = None
        self._validator_tab: Optional['ValidatorTab'] = None
        self._dependencies_tab: Optional['DependenciesTab'] = None
        self._status_callback = None

    def set_status_callback(self, callback):
        self._status_callback = callback

    def register_build_tab(self, tab: 'BuildTab') -> None:
        self._build_tab = tab

    def register_validator_tab(self, tab: 'ValidatorTab') -> None:
        self._validator_tab = tab

    def register_dependencies_tab(self, tab: 'DependenciesTab') -> None:
        self._dependencies_tab = tab

    def update_status(self, message: str) -> None:
        if self._status_callback:
            self._status_callback(message)

    def set_desktop_content(self, content: str) -> None:
        if self._validator_tab:
            self._validator_tab.set_content(content)

    def get_desktop_content(self) -> str:
        if self._validator_tab:
            return self._validator_tab.get_content()
        return ""

    def validate_desktop_file(self) -> ValidationResult:
        if self._validator_tab:
            return self._validator_tab.validate()
        return ValidationResult(is_valid=False, errors=["No validator tab registered"])

    def get_dependencies(self) -> List[str]:
        if self._dependencies_tab:
            return self._dependencies_tab.get_dependencies()
        return []

    def set_dependencies(self, deps: List[str]) -> None:
        if self._dependencies_tab:
            self._dependencies_tab.set_dependencies(deps)
