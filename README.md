# AppImage Builder

GUI en Tkinter para crear AppImages usando linuxdeploy. Incluye un validador simple de archivos .desktop y un boton para instalar linuxdeploy si no esta disponible.

## Requisitos

- Python 3
- Tkinter (normalmente viene con la instalacion de Python en Linux)
- linuxdeploy (se puede instalar desde la GUI o con el script)

## Ejecutar

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

## Instalar linuxdeploy

Opcion 1: desde la GUI

- Si no esta instalado, el boton "Install linuxdeploy" permite descargar e instalar con confirmacion.

Opcion 2: con el script

```bash
./install_appimage_tools.sh
```

## Notas

- El AppDir se crea como `<AppName>.AppDir` y se sobrescribe si ya existe.
- La version por defecto es 1.0 si no se especifica.
