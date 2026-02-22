# =============================================
# ClawVoice Worker - Dockerfile
# =============================================
# Imagen liviana con Python 3.11
# =============================================

FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar primero las dependencias para cachear
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear directorio para logs
RUN mkdir -p logs

# Puerto por defecto
EXPOSE 8000

# Comando por defecto
CMD ["python", "worker.py"]
