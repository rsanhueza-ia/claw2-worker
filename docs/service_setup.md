# Configuración de ClawVoice Worker como Servicio de Windows

Para que el worker funcione de forma permanente y se inicie automáticamente con tu PC, recomendamos usar **NSSM (Non-Sucking Service Manager)**.

## Requisitos previos
1. Tener [Python](https://www.python.org/) instalado y en el PATH.
2. Haber configurado el archivo `.env` en la carpeta raíz del worker.
3. Descargar **NSSM** desde [nssm.cc](https://nssm.cc/download).

## Pasos para la instalación

1. **Extraer NSSM**: Copia el ejecutable `nssm.exe` (de la carpeta `win64` o `win32` según tu sistema) a una ubicación accesible (ej. la carpeta del worker).
2. **Abrir Terminal como Administrador**: Haz clic derecho en el botón de Inicio y selecciona "Terminal (Administrador)" o "PowerShell (Administrador)".
3. **Ejecutar el instalador**:
   Navega hasta la carpeta donde tienes NSSM y ejecuta:
   ```powershell
   .\nssm.exe install ClawVoiceWorker
   ```
4. **Configurar en la ventana emergente**:
   - **Path**: Busca tu ejecutable de python (ej. `C:\Users\TuUsuario\AppData\Local\Programs\Python\Python311\python.exe`).
   - **Startup directory**: La carpeta donde está `worker.py` (ej. `C:\Archivos-otros-programas\claw2_worker`).
   - **Arguments**: `worker.py`
5. **Pestaña I/O (Opcional pero recomendado)**:
   - Configura un archivo de log para `stdout` y `stderr` (ej. `logs\service.log`) para poder ver errores si el worker falla.
6. **Instalar y Arrancar**:
   - Haz clic en "Install service".
   - Luego, en la terminal, ejecuta: `Start-Service ClawVoiceWorker` o ábrelo desde `services.msc`.

## Mantenimiento
- **Detener**: `nssm stop ClawVoiceWorker`
- **Editar configuración**: `nssm edit ClawVoiceWorker`
- **Eliminar**: `nssm remove ClawVoiceWorker`
