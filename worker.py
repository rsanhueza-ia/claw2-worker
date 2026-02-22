import os
import asyncio
import traceback
import requests
import re
import unicodedata
from dotenv import load_dotenv
from supabase import create_client
from realtime import AsyncRealtimeClient as RealtimeClient

# =====================================================
# Load Environment
# =====================================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
OPENCLAW_URL = os.getenv("OPENCLAW_URL")  # Example: http://127.0.0.1:18789
OPENCLAW_TOKEN = os.getenv("OPENCLAW_GATEWAY_TOKEN")
MODEL = os.getenv("MODEL", "openclaw")

if not all([SUPABASE_URL, SUPABASE_KEY, OPENCLAW_URL]):
    print(f"DEBUG: SUPABASE_URL={SUPABASE_URL}")
    print(f"DEBUG: SUPABASE_KEY={'Set' if SUPABASE_KEY else 'Not Set'}")
    print(f"DEBUG: OPENCLAW_URL={OPENCLAW_URL}")
    raise ValueError("❌ Missing required environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Mono usuario → solo 1 procesamiento simultáneo
semaphore = asyncio.Semaphore(1)

# =====================================================
# TTS CLEANING FUNCTION
# =====================================================

def clean_for_tts(text: str) -> str:
    """
    Limpia texto para que sea seguro y natural en TTS.
    """

    # Normalizar unicode
    text = unicodedata.normalize("NFKC", text)

    # Eliminar markdown común
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"#+\s*", "", text)

    # Eliminar emojis y símbolos raros (mantener puntuación básica)
    text = re.sub(r"[^\w\s.,;:¿?¡!áéíóúÁÉÍÓÚñÑ()-]", "", text)

    # Convertir listas en frases
    text = re.sub(r"\n\s*-\s*", ". ", text)
    text = re.sub(r"\n\s*\d+\.\s*", ". ", text)

    # Eliminar saltos de línea
    text = text.replace("\n", " ")

    # Eliminar espacios múltiples
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =====================================================
# OpenClaw Call
# =====================================================

def get_openclaw_response(user_text: str) -> str:
    try:
        url = f"{OPENCLAW_URL}/v1/responses"

        headers = {
            "Content-Type": "application/json"
        }

        if OPENCLAW_TOKEN:
            headers["Authorization"] = f"Bearer {OPENCLAW_TOKEN}"

        payload = {
            "model": MODEL,
            "input": (
                "Eres un asistente de voz. "
                "Responde en texto plano optimizado para lectura por sintetizador de voz. "
                "No uses emojis. "
                "No uses símbolos decorativos. "
                "No uses markdown. "
                "No uses asteriscos. "
                "No uses listas. "
                "No incluyas saltos de línea. "
                "Responde en un único párrafo claro, natural y conversacional.\n\n"
                f"Usuario: {user_text}"
            )
        }

        print(f"🤖 Enviando a OpenClaw: {user_text}")
        print("⏳ Generando respuesta (esto puede tardar un momento)...")

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=90
        )

        if response.status_code != 200:
            return f"Error OpenClaw {response.status_code}: {response.text}"

        data = response.json()

        output_text = ""
        if "output" in data:
            for item in data["output"]:
                if item.get("type") == "message":
                    for content in item.get("content", []):
                        if content.get("type") == "output_text":
                            output_text = content.get("text", "")

        return output_text or "(Sin respuesta)"

    except Exception as e:
        return f"Error conexión OpenClaw: {str(e)}"


# =====================================================
# Processing Logic
# =====================================================

def process_record_sync(record):
    try:
        print(f"\n📨 Procesando mensaje: {record['id']}")

        # UPDATE ATÓMICO
        result = supabase.table("oclaw2_messages") \
            .update({"status": "processing"}) \
            .eq("id", record["id"]) \
            .eq("status", "pending") \
            .execute()

        if not result.data:
            # Verificamos si es por falta de permisos o porque realmente ya no es 'pending'
            check = supabase.table("oclaw2_messages").select("status").eq("id", record["id"]).execute()
            if check.data and check.data[0].get("status") != "pending":
                print(f"⚠️ Mensaje {record['id']} saltado: ya está en estado '{check.data[0]['status']}'.")
            else:
                print(f"❌ ERROR DE PERMISOS en mensaje {record['id']}.")
                print("👉 Tu SUPABASE_SERVICE_ROLE_KEY es una 'anon key' y no tiene permiso para actualizar.")
                print("👉 Por favor, usa la 'service_role' key de tu panel de Supabase.")
            return

        # Llamar modelo
        user_message = record.get("content", "")
        print(f"👤 Usuario: {user_message}")

        response_text = get_openclaw_response(user_message)

        if response_text.startswith("Error"):
            supabase.table("oclaw2_messages") \
                .update({"status": "failed"}) \
                .eq("id", record["id"]) \
                .execute()
            print(f"❌ Error en OpenClaw: {response_text}")
            return

        # Limpieza para TTS
        response_text = clean_for_tts(response_text)
        print(f"🤖 Asistente: {response_text}")

        # Insert assistant message
        supabase.table("oclaw2_messages").insert({
            "conversation_id": record.get("conversation_id"),
            "user_id": record.get("user_id"),
            "role": "assistant",
            "content": response_text,
            "status": "completed"
        }).execute()

        print("✅ Respuesta insertada correctamente")

    except Exception as e:
        print(f"❌ Error en procesamiento: {e}")
        traceback.print_exc()

        supabase.table("oclaw2_messages") \
            .update({"status": "failed"}) \
            .eq("id", record["id"]) \
            .execute()


# =====================================================
# Async Wrapper
# =====================================================

async def handle_insert_async(record):
    async with semaphore:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, process_record_sync, record)


def handle_insert(payload):
    try:
        record = payload.get("data", {}).get("record", {})

        if not record:
            return

        if record.get("role") == "user" and record.get("status") == "pending":
            print(f"👀 Nuevo mensaje detectado: {record.get('id')}")
            asyncio.create_task(handle_insert_async(record))

    except Exception as e:
        print(f"❌ Error en handle_insert: {e}")
        traceback.print_exc()


# =====================================================
# Main
# =====================================================

async def main():
    print("🚀 ClawVoice Worker v1.1 iniciado")

    realtime = RealtimeClient(
        f"{SUPABASE_URL}/realtime/v1",
        SUPABASE_KEY
    )

    channel = realtime.channel("clawvoice-worker")

    channel.on_postgres_changes(
        event="INSERT",
        schema="public",
        table="oclaw2_messages",
        callback=handle_insert
    )

    await realtime.connect()
    await channel.subscribe()

    print("👂 Escuchando eventos en tiempo real...")

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Worker detenido por usuario")
    except Exception as e:
        print(f"💀 Error fatal: {e}")
        traceback.print_exc()
