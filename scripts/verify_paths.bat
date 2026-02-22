@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo   ClawVoice Worker - Auxiliar de Servicio
echo ==========================================

:: Verificar si el script se ejecuta como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Por favor, ejecuta este script como ADMINISTRADOR.
    pause
    exit /b
)

:: Verificar existencia de python
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] No se encontro Python en el PATH.
    pause
    exit /b
)

:: Obtener ruta de python
for /f "tokens=*" %%i in ('where python') do set PYTHON_EXE=%%i

:: Verificar worker.py
if not exist "..\worker.py" (
    echo [ERROR] No se encontro worker.py en la carpeta superior.
    echo Asegurate de ejecutar este script desde la carpeta 'scripts'.
    pause
    exit /b
)

set WORKER_PATH=%~dp0..\worker.py
for %%A in ("%WORKER_PATH%") do set WORKER_FULL_PATH=%%~fA
set WORKDIR=%~dp0..
for %%A in ("%WORKDIR%") do set WORKDIR_FULL=%%~fA

echo.
echo === Informacion para configurar en NSSM ===
echo Path: %PYTHON_EXE%
echo Startup directory: %WORKDIR_FULL%
echo Arguments: %WORKER_FULL_PATH%
echo ==========================================
echo.
echo Ahora puedes ejecutar: nssm install ClawVoiceWorker
echo Y usar los datos de arriba.
echo.
pause
