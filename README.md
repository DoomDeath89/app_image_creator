# AppImage Builder

GUI en Tkinter para crear AppImages usando linuxdeploy. Incluye un validador simple de archivos .desktop y un boton para instalar linuxdeploy si no esta disponible.

## Download

- Release arm64 (PyInstaller onefile): https://github.com/DoomDeath89/app_image_creator/releases/tag/1.0.0
- Checksum SHA256: https://github.com/DoomDeath89/app_image_creator/releases/tag/1.0.0

## Capturas

Agrega capturas en `docs/screenshots/` y enlazalas aqui cuando esten listas.

## Requisitos

- Python 3
- Tkinter (normalmente viene con la instalacion de Python en Linux)
- linuxdeploy (se puede instalar desde la GUI o con el script)

## Ejecutar desde codigo fuente

Si deseas usar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
python3 main.py
```

O ejecutar directamente:

```bash
python3 main.py
```

## Ejecutable (arm64)

Descarga el binario desde la release y dale permisos:

```bash
chmod +x AppImageBuilder
./AppImageBuilder
```

## Instalar linuxdeploy

Opcion 1: desde la GUI

- Si no esta instalado, el boton "Install linuxdeploy" permite descargar e instalar con confirmacion.

Opcion 2: con el script

```bash
./install_appimage_tools.sh
```

## Publicacion en directorios

- Considera publicar en AppImageHub/AppImage Catalog cuando tengas un AppImage publico.

## Notas

- El AppDir se crea como `<AppName>.AppDir` y se sobrescribe si ya existe.
- La version por defecto es 1.0 si no se especifica.

## Licencia

MIT. Ver LICENSE.
