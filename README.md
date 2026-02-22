# ClawVoice Worker 🤖🎙️

> **Desarrollado por: Ricardo Sanhueza**
> *Ingeniero Civil en Informática (Chile)*

> El puente entre tu voz y tu OpenClaw local.

**ClawVoice Worker** es el componente backend del ecosistema ClawVoice. Su función es conectar la aplicación Android con tu instancia local de **OpenClaw** a través de **Supabase**, permitiendo una comunicación verbal fluida, privada y en tiempo real.

---

## 📂 Contenido del Repositorio

Para facilitar la comprensión y el despliegue del proyecto, hemos organizado la documentación en secciones claras:

1.  **[¿Cómo funciona? (Arquitectura)](./docs/ABOUT.md)**: Explicación del flujo de datos entre el móvil, Supabase, el Worker y OpenClaw.
2.  **[Guía de Instalación](./docs/INSTALLATION.md)**: Pasos para configurar Supabase, el entorno Python y la App Android.
3.  **[Ejecutar como Servicio](./docs/service_setup.md)**: Instrucciones para dejar el worker funcionando permanentemente en segundo plano en Windows.

---

## 🚀 Inicio Rápido

### Opción A: Con Python (Recomendado para Windows)

1. Instala dependencias: `pip install -r requirements.txt`
2. Copia `.env.example` a `.env` y configura tus claves
3. Ejecuta: `python worker.py`

### Opción B: Con Docker (Linux/Mac)

1. Copia `.env.example` a `.env` y configura tus claves
2. Ejecuta: `docker-compose up -d`

> **Nota**: En Windows, Docker Desktop no tiene acceso directo a localhost. Ejecuta el worker con Python directamente.

---

## 🤝 Contribuciones y Comunidad

Este es un proyecto **libre y abierto**. Si quieres mejorar el sistema, añadir soporte multiusuario o integrar nuevos modelos, ¡tus Pull Requests son bienvenidos!

*Diseñado para ser la herramienta definitiva de comunicación verbal personal con IA local.*

---

## 📜 Licencia
Este proyecto se distribuye bajo la licencia **MIT**. Siéntete libre de usarlo, modificarlo y compartirlo para "hacerte famoso" y mejorar la comunidad de IA libre.
