from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Callable


@dataclass
class BuildConfig:
    name: str
    version: str
    category: str
    comment: str
    executable_path: Path
    icon_path: Optional[Path] = None
    extra_deps: List[Path] = field(default_factory=list)


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def summary(self) -> str:
        if self.errors:
            return "Validation FAILED: " + "; ".join(self.errors)
        if self.warnings:
            return "Validation PASSED with warnings: " + "; ".join(self.warnings)
        return "Validation PASSED"

    @property
    def color(self) -> str:
        if self.errors:
            return "red"
        if self.warnings:
            return "orange"
        return "green"
