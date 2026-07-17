from typing import List
from app.utils.constants import REQUIRED_DESKTOP_FIELDS, VALID_CATEGORIES, DEFAULT_COMMENT
from app.utils.types import BuildConfig, ValidationResult


class DesktopFileHandler:
    def generate(self, config: BuildConfig) -> str:
        return (
            f"[Desktop Entry]\n"
            f"Name={config.name}\n"
            f"Exec={config.name}\n"
            f"Icon={config.name}\n"
            f"Type=Application\n"
            f"Categories={config.category};\n"
            f"Comment={config.comment}\n"
            f"Version={config.version}\n"
        )

    def validate(self, content: str) -> ValidationResult:
        lines = content.split('\n')
        errors: List[str] = []
        warnings: List[str] = []
        present_fields: List[str] = []

        for line in lines:
            line = line.strip()
            if '=' not in line:
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            if key in REQUIRED_DESKTOP_FIELDS:
                present_fields.append(key)

            if key == 'Categories':
                category_value = value.rstrip(';')
                if category_value not in VALID_CATEGORIES:
                    warnings.append(
                        f"Category '{category_value}' is not a standard category. "
                        f"Consider using one of the standard categories."
                    )

        for field in REQUIRED_DESKTOP_FIELDS:
            if field not in present_fields:
                errors.append(f"Missing required field: {field}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def get_sample(self) -> str:
        return (
            "[Desktop Entry]\n"
            "Name=My Application\n"
            "Exec=myapp\n"
            "Icon=myapp\n"
            "Type=Application\n"
            "Categories=Utility;\n"
            "Comment=A sample application\n"
        )
