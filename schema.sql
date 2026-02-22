-- =============================================
-- ClawVoice Worker - Schema de Base de Datos
-- =============================================
-- Este script crea la tabla necesaria para el funcionamiento
-- del ecosistema ClawVoice en Supabase.
--
-- Ejecutar en: SQL Editor de Supabase
-- =============================================

-- 1. Crear la tabla de mensajes
CREATE TABLE IF NOT EXISTS public.oclaw2_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    conversation_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (
        status IN (
            'pending',
            'processing',
            'completed',
            'failed'
        )
    )
);

-- 2. Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON public.oclaw2_messages (conversation_id);

CREATE INDEX IF NOT EXISTS idx_messages_status ON public.oclaw2_messages (status);

CREATE INDEX IF NOT EXISTS idx_messages_role ON public.oclaw2_messages (role);

CREATE INDEX IF NOT EXISTS idx_messages_created ON public.oclaw2_messages (created_at DESC);

-- 3. Habilitar Realtime para la tabla
ALTER PUBLICATION supabase_realtime ADD TABLE public.oclaw2_messages;

-- 4. (Opcional) Configurar RLS - Descomenta si quieres habilitar
-- ALTER TABLE public.oclaw2_messages ENABLE ROW LEVEL SECURITY;

-- 5. (Opcional) Políticas RLS - Descomenta si usas RLS
-- Policy para que cualquier usuario pueda insertar mensajes
-- CREATE POLICY "Allow insert for all" ON public.oclaw2_messages
--     FOR INSERT TO anon, authenticated
--     WITH CHECK (true);

-- Policy para que cualquier usuario pueda leer mensajes
-- CREATE POLICY "Allow read for all" ON public.oclaw2_messages
--     FOR SELECT TO anon, authenticated
--     USING (true);

-- Policy para que cualquier usuario pueda actualizar (el worker necesita esto)
-- CREATE POLICY "Allow update for all" ON public.oclaw2_messages
--     FOR UPDATE TO anon, authenticated
--     USING (true)
--     WITH CHECK (true);

-- =============================================
-- NOTA IMPORTANTE:
-- =============================================
-- Después de ejecutar este script, ve al panel de Supabase:
-- Database -> Replication -> Enable Realtime para 'oclaw2_messages'
-- =============================================