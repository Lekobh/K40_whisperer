@echo off
rem ---------------------------------------------------------------------
rem This file executes the build command for the windows executable file
rem using PyInstaller.
rem ---------------------------------------------------------------------

echo Cleaning up previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo Building executable with PyInstaller...
pyinstaller --noconfirm --onedir --windowed --icon "scorchworks.ico" --hidden-import lxml.etree --hidden-import lxml._elementpath k40_whisperer.py

echo Build completed! Check the 'dist' folder.
pause
