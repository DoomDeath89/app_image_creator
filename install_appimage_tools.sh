#!/bin/bash

set -e

echo "Instalando AppImageTool y LinuxDeploy para ARM64..."

# Crear carpeta temporal
TMP_DIR=$(mktemp -d)
cd $TMP_DIR

# Descargar AppImageTool ARM64 (ruta verificada)
echo "Descargando AppImageTool ARM64..."
wget -c "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-aarch64.AppImage" -O appimagetool.AppImage
chmod +x appimagetool.AppImage
sudo mv appimagetool.AppImage /usr/local/bin/appimagetool
echo "AppImageTool instalado en /usr/local/bin/appimagetool"

# Descargar LinuxDeploy ARM64 (ruta específica verificada)
echo "Descargando LinuxDeploy ARM64..."
wget -c "https://github.com/linuxdeploy/linuxdeploy/releases/download/1-alpha-20250213-2/linuxdeploy-aarch64.AppImage" -O linuxdeploy.AppImage
chmod +x linuxdeploy.AppImage
sudo mv linuxdeploy.AppImage /usr/local/bin/linuxdeploy
echo "LinuxDeploy instalado en /usr/local/bin/linuxdeploy"

# Limpiar
cd ~
rm -rf $TMP_DIR

echo "Instalación completada. Verifica con:"
echo "appimagetool --version"
echo "linuxdeploy --version"
