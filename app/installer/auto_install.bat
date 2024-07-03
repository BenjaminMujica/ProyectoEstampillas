@echo off
echo Presione cualquier tecla para instalar las dependencias del programa...
pause >nul
cd dependencies
python install_dependencies.py
pause