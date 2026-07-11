@echo off
rem Запуск сборки через PyInstaller со спецификацией и очисткой старых билдов
cd /d "%~dp0"
pyinstaller mouse_states_release.spec --clean
echo.
echo ----------------------------
echo Сборка завершена. Нажмите любую клавишу...
pause >nul