# Plan de Refactoring SDD - AppImage Builder

## 1. Documentos de Especificación

### 1.1 Especificación de Arquitectura Core

**Propósito:** Definir la arquitectura del sistema y las interacciones entre componentes.

**Componentes:**
- `AppImageBuilderApp` - Controlador principal de la aplicación
- `Mediator` - Hub central de coordinación (implementado correctamente)
- `BuildTab` - UI para construir AppImages
- `ValidatorTab` - UI de validación de archivos .desktop
- `DependenciesTab` - UI de gestión de dependencias
- `LinuxDeployManager` - Gestión de la herramienta linuxdeploy
- `AppDirBuilder` - Lógica de construcción de AppDir
- `DesktopFileHandler` - Operaciones con archivos .desktop
- `Constants` - Valores de configuración compartidos

**Patrón de Comunicación:**
```
Tabs → Mediator → Tabs
         ↓
    Services (LinuxDeployManager, AppDirBuilder, etc.)
```

---

### 1.2 Especificación del Mediator

**Propósito:** Coordinador central para comunicación entre tabs.

**Interfaz:**
```python
class Mediator:
    def update_status(self, message: str) -> None
    def set_desktop_content(self, content: str) -> None
    def get_desktop_content(self) -> str
    def validate_desktop_file(self, content: str) -> ValidationResult
    def get_dependencies(self) -> List[str]
    def set_dependencies(self, deps: List[str]) -> None
    def register_build_tab(self, tab: BuildTab) -> None
    def register_validator_tab(self, tab: ValidatorTab) -> None
    def register_dependencies_tab(self, tab: DependenciesTab) -> None
```

**Restricciones:**
- Sin referencias directas entre tabs
- Toda comunicación a través del mediator
- Actualizaciones de status thread-safe

---

### 1.3 Especificación de BuildTab

**Propósito:** UI para construir AppImages.

**Responsabilidades:**
- Mostrar formulario de configuración de build
- Recoger inputs del usuario (ejecutable, icono, nombre, versión, etc.)
- Disparar proceso de build a través del mediator
- Mostrar progreso y logs del build

**NO es responsable de:**
- Gestión de linuxdeploy (delegado a LinuxDeployManager)
- Construcción de AppDir (delegado a AppDirBuilder)
- Generación de archivos .desktop (delegado a DesktopFileHandler)

---

### 1.4 Especificación de LinuxDeployManager

**Propósito:** Gestión del ciclo de vida de linuxdeploy.

**Interfaz:**
```python
class LinuxDeployManager:
    def is_available(self) -> bool
    def get_version(self) -> Optional[str]
    def install(self, progress_callback: Callable) -> bool
    def get_url(self, arch: str = None) -> str
    def ensure_available(self) -> bool
```

**Restricciones:**
- Auto-detectar arquitectura (arm64/amd64)
- Soportar instalación manual y automática
- Proporcionar feedback de progreso durante instalación

---

### 1.5 Especificación de AppDirBuilder

**Propósito:** Construir la estructura AppDir.

**Interfaz:**
```python
class AppDirBuilder:
    def __init__(self, base_dir: Path)
    def create(self, config: BuildConfig) -> Path
    def cleanup(self) -> None
    def add_executable(self, src: Path) -> None
    def add_icon(self, src: Path, name: str) -> None
    def create_desktop_file(self, config: BuildConfig) -> Path
    def create_apprun_script(self, executable_name: str) -> Path
```

**BuildConfig:**
```python
@dataclass
class BuildConfig:
    name: str
    version: str
    category: str
    comment: str
    executable_path: Path
    icon_path: Optional[Path]
    extra_deps: List[Path]
```

---

### 1.6 Especificación de DesktopFileHandler

**Propósito:** Generar y validar archivos .desktop.

**Interfaz:**
```python
class DesktopFileHandler:
    REQUIRED_FIELDS = ['Name', 'Exec', 'Type', 'Categories']
    VALID_CATEGORIES = [...]
    
    def generate(self, config: BuildConfig) -> str
    def validate(self, content: str) -> ValidationResult
    def get_sample(self) -> str
```

**ValidationResult:**
```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
```

---

### 1.7 Especificación de Constants

**Propósito:** Centralizar valores de configuración.

**Valores:**
```python
APP_NAME = "AppImage Builder"
APP_VERSION = "1.0.0"
DEFAULT_APP_VERSION = "1.0"
LINUXDEPLOY_URLS = {
    'arm64': 'https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-arm64.AppImage',
    'amd64': 'https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage'
}
VALID_CATEGORIES = [
    'AudioVideo', 'Audio', 'Video', 'Graphics', 'Office',
    'Development', 'Education', 'Game', 'Network', 'Settings',
    'System', 'Utility'
]
```

---

## 2. Plan de Implementación

### Fase 1: Fundación (Especificaciones → Constants & Utils)

**Paso 1.1:** Crear `app/utils/constants.py`
- Mover todos los valores hardcodeados
- Definir VALID_CATEGORIES, LINUXDEPLOY_URLS, etc.

**Paso 1.2:** Crear `app/utils/types.py`
- Definir dataclasses BuildConfig, ValidationResult
- Definir aliases de tipo para callbacks

**Paso 1.3:** Agregar `.gitignore`
- Excluir __pycache__, *.pyc, venv/, .env

---

### Fase 2: Services (Especificaciones → Implementación)

**Paso 2.1:** Crear `app/services/desktop_file_handler.py`
- Implementar clase DesktopFileHandler
- Mover lógica de validación desde ValidatorTab
- Mover generación de archivos .desktop desde BuildTab

**Paso 2.2:** Crear `app/services/linux_deploy_manager.py`
- Implementar clase LinuxDeployManager
- Extraer lógica de linuxdeploy desde BuildTab
- Agregar detección de arquitectura

**Paso 2.3:** Crear `app/services/app_dir_builder.py`
- Implementar clase AppDirBuilder
- Extraer construcción de AppDir desde BuildTab
- Usar shutil en lugar de subprocess para operaciones de archivos

---

### Fase 3: Mediator (Especificaciones → Implementación)

**Paso 3.1:** Refactorizar `app/core/mediator.py`
- Crear clase Mediator correctamente
- Definir todos los métodos requeridos
- Eliminar referencias directas a tabs de la interfaz

**Paso 3.2:** Actualizar `app/core/main.py`
- Eliminar código de bypass del mediator
- Usar la nueva clase Mediator
- Limpiar inicialización

---

### Fase 4: Tabs (Especificaciones → Implementación)

**Paso 4.1:** Refactorizar `app/tabs/build_tab.py`
- Eliminar toda la lógica de negocio (movida a services)
- Usar mediator para toda comunicación entre tabs
- Simplificar a responsabilidad pura de UI

**Paso 4.2:** Refactorizar `app/tabs/validator_tab.py`
- Usar DesktopFileHandler para validación
- Usar mediator para acceso a contenido desktop
- Unificar nomenclatura de parámetros (mediator)

**Paso 4.3:** Refactorizar `app/tabs/dependencies_tab.py`
- Usar mediator para gestión de dependencias
- Unificar nomenclatura de parámetros (mediator)

---

### Fase 5: Entry Point & Packaging

**Paso 5.1:** Crear `pyproject.toml`
- Definir metadata del paquete
- Agregar entry points
- Especificar dependencias (ninguna externa)

**Paso 5.2:** Actualizar `run_app.py`
- Eliminar manipulación de sys.path
- Usar imports de paquete correctos

**Paso 5.3:** Actualizar `README.md`
- Corregir instrucciones de ejecución
- Agregar guía de setup para desarrollo

---

### Fase 6: Tests (Especificaciones → Implementación)

**Paso 6.1:** Crear `tests/conftest.py`
- Agregar fixtures de pytest
- Mockear tkinter para testing headless

**Paso 6.2:** Crear `tests/test_services.py`
- Testear DesktopFileHandler
- Testear LinuxDeployManager
- Testear AppDirBuilder

**Paso 6.3:** Refactorizar tests existentes
- Usar fixtures de conftest.py
- Agregar tests de integración
- Mejorar coverage para build_appimage()

**Paso 6.4:** Agregar `tests/__init__.py`
- Habilitar discovery correcto de tests

---

### Fase 7: CI/CD

**Paso 7.1:** Actualizar `.github/workflows/pylint.yml`
- Actualizar matriz de versiones de Python
- Agregar paso de ejecución de tests
- Agregar pytest con xvfb para tests de tkinter

---

## 3. Estructura de Archivos Post-Refactor

```
app_image_creator/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── main.py              (AppImageBuilderApp)
│   │   └── mediator.py          (Mediator)
│   ├── tabs/
│   │   ├── __init__.py
│   │   ├── build_tab.py         (solo UI)
│   │   ├── dependencies_tab.py  (solo UI)
│   │   └── validator_tab.py     (solo UI)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── app_dir_builder.py
│   │   ├── desktop_file_handler.py
│   │   └── linux_deploy_manager.py
│   └── utils/
│       ├── __init__.py
│       ├── constants.py
│       └── types.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_mediator.py
│   ├── test_services.py
│   ├── test_build_tab.py
│   ├── test_dependencies_tab.py
│   └── test_validator_tab.py
├── .github/workflows/
│   └── pylint.yml
├── pyproject.toml
├── .gitignore
├── LICENSE
├── README.md
├── run_app.py
├── run_appimager.sh
└── install_appimage_tools.sh
```

---

## 4. Checklist de Verificación

- [ ] Todas las especificaciones implementadas
- [ ] Sin referencias directas entre tabs
- [ ] Toda comunicación a través del mediator
- [ ] Services independientes y testables
- [ ] Tests pasan sin display (tkinter mockeado)
- [ ] Code coverage > 80%
- [ ] CI ejecuta tests exitosamente
- [ ] README actualizado
- [ ] Sin hacks de sys.path
- [ ] Estructura de paquete correcta
