# Guía de Instalación y Distribución

Esta guía contiene los pasos necesarios para desplegar tu propio ecosistema de comunicación verbal personal.

---

## 1. Configuración de Supabase (Nube)
Necesitarás un proyecto en [Supabase](https://supabase.com/) (el plan gratuito es suficiente).

1. Crea una tabla llamada `oclaw2_messages` con las siguientes columnas:
   - `id`: uuid (Primary Key, por defecto gen_random_uuid())
   - `created_at`: timestamptz (por defecto now())
   - `conversation_id`: text
   - `user_id`: text
   - `role`: text (ej: "user", "assistant")
   - `content`: text
   - `status`: text (ej: "pending", "processing", "completed", "failed")
2. **IMPORTANTE**: En el panel de Supabase, ve a **Database -> Replication** y habilita Realtime para la tabla `oclaw2_messages`.

---

## 2. Instalación del Worker (PC)
El worker debe ejecutarse en la misma máquina donde tienes OpenClaw.

1. **Clonar/Descargar** los archivos del worker.
2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar entorno**: Renombra `.env.example` a `.env` y completa los datos:
   - `SUPABASE_URL`: La URL de tu proyecto.
   - `SUPABASE_SERVICE_ROLE_KEY`: Tu clave secreta (Service Role) para saltar políticas RLS.
   - `OPENCLAW_URL`: Habitualmente `http://127.0.0.1:18789`.
   - `MODEL`: Debe ser `openclaw`.
4. **Ejecutar**:
   ```bash
   python worker.py
   ```
   *(Opcional: Ver `docs/service_setup.md` para dejarlo como servicio de Windows).*

---

## 3. Instalación de la App (Android)
1. Descarga el APK desde la sección de *Releases* (o compila el código en Android Studio).
2. Al abrir la app, ingresa tu `SUPABASE_URL` y `SUPABASE_ANON_KEY`.
3. ¡Empieza a hablar!

---

## Consejos para Distribución y Fama ⭐

Si quieres publicar este proyecto libremente en GitHub y que otros lo usen/mejoren:

1. **Licencia**: Incluye un archivo `LICENSE` (ej: MIT) para que otros puedan usarlo y mejorarlo libremente.
2. **Personalización**: Anima a los usuarios a crear sus propios "Skins" para la app Android.
3. **OpenClaw Community**: Comparte tu repositorio en foros de OpenClaw y Discord.
4. **Pull Requests**: ¡Deja claro que aceptas mejoras! El manejo multiusuario o la memoria conversacional son excelentes puntos para que la comunidad colabore.
5. **Video Demo**: Un video corto mostrando la latencia casi nula entre la voz y la respuesta local suele volverse viral en comunidades de IA.

---

## Estructura del Proyecto
- `/app`: Código fuente de Android (Kotlin/Compose).
- `/worker`: Puente de comunicación en Python.
- `/docs`: Guías de arquitectura, servicios e instalación.
- `/scripts`: Herramientas de utilidad para el sistema.
