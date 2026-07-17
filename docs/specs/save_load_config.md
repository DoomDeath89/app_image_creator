# Spec: Save/Load Build Configuration

## User Story
Como usuario quiero guardar mi configuración de build para no reingresar los datos cada vez.

## Criterios de Aceptación

### CA1: Botón Save Config
- Botón "Save Config" visible en el tab de Build
- Ubicación: junto al botón "Generate AppImage"

### CA2: Diálogo de guardado
- Al hacer click en "Save Config", se abre diálogo para elegir ubicación del archivo .json
- Formato de archivo: JSON
- Extensión por defecto: .json

### CA3: Contenido del archivo
El archivo JSON debe contener:
```json
{
  "name": "string",
  "version": "string",
  "category": "string",
  "comment": "string",
  "executable_path": "string",
  "icon_path": "string"
}
```

### CA4: Botón Load Config
- Botón "Load Config" visible en el tab de Build
- Ubicación: junto al botón "Save Config"

### CA5: Importación de configuración
- Al hacer click en "Load Config", se abre diálogo para seleccionar un archivo .json
- Los campos del formulario se rellenan automáticamente con los valores del archivo
- Si un campo no existe en el JSON, se deja vacío o con valor por defecto

### CA6: Tests
- `test_save_config_creates_valid_json`: Verificar que el JSON generado contiene todos los campos requeridos
- `test_load_config_populates_fields`: Verificar que los campos se rellenan correctamente

## Archivos a modificar
- `app/tabs/build_tab.py` - Agregar botones Save/Load y lógica
- `tests/test_build_tab.py` - Agregar tests

## No incluido
- Validación de campos al guardar
- Historial de configuraciones
- Configuración por defecto
