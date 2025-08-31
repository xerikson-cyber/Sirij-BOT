# -*- coding: utf-8 -*-
"""
Manejadores de mensajes y comandos para SIRIJ BOT
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from .conversation import ConversationManager
from services.session_service import SessionService
from services.photo_service import PhotoService

logger = logging.getLogger(__name__)

# Instancias de servicios
conversation_manager = ConversationManager()
session_service = SessionService()
photo_service = PhotoService()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja el comando /start
    """
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    logger.info(f"Usuario {username} ({user_id}) inició el bot")
    
    # Inicializar conversación
    response = conversation_manager.iniciar_reunion(user_id)
    
    await update.message.reply_text(response['mensaje'])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja el comando /help
    """
    help_text = """
🤖 **SIRIJ BOT - Ayuda**

**Comandos disponibles:**
/start - Iniciar nueva reunión de inicio de jornada
/help - Mostrar esta ayuda
/cancel - Cancelar reunión actual

**¿Cómo usar el bot?**
1. Usa /start para comenzar
2. Responde las preguntas paso a paso
3. Sube una foto como evidencia
4. Confirma la información

**Tipos de respuesta:**
• Texto libre: Escribe tu respuesta
• Sí/No: Responde "Sí" o "No"
• Fecha: Formato DD/MM/AAAA
• Hora: Formato HH:MM
• Nombres: Separa con comas

¿Necesitas ayuda? Contacta al administrador.
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja el comando /cancel
    """
    user_id = update.effective_user.id
    
    # Cancelar sesión activa
    result = session_service.cancelar_sesion(user_id)
    
    if result['exito']:
        mensaje = "✅ Reunión cancelada. Puedes iniciar una nueva con /start"
    else:
        mensaje = "ℹ️ No tienes ninguna reunión activa."
    
    await update.message.reply_text(mensaje)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja mensajes de texto del usuario
    """
    user_id = update.effective_user.id
    mensaje_usuario = update.message.text
    
    logger.info(f"Usuario {user_id} envió: {mensaje_usuario}")
    
    try:
        # Procesar mensaje a través del manejador de conversación
        response = conversation_manager.procesar_mensaje(user_id, mensaje_usuario)
        
        # Enviar respuesta
        await update.message.reply_text(response['mensaje'])
        
        # Si la conversación terminó, mostrar resumen
        if response.get('estado') == 'completado':
            resumen = conversation_manager.generar_resumen(user_id)
            await update.message.reply_text(resumen, parse_mode='Markdown')
            
    except Exception as e:
        logger.error(f"Error procesando mensaje de usuario {user_id}: {e}")
        await update.message.reply_text(
            "❌ Ocurrió un error procesando tu mensaje. Por favor, intenta de nuevo o usa /cancel para reiniciar."
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja fotografías enviadas por el usuario
    """
    user_id = update.effective_user.id
    
    logger.info(f"Usuario {user_id} envió una fotografía")
    
    try:
        # Verificar si el usuario está en el estado correcto para enviar foto
        sesion = session_service.obtener_sesion_activa(user_id)
        
        if not sesion or sesion.get('estado') != 'esperando_foto':
            await update.message.reply_text(
                "ℹ️ No estoy esperando una fotografía en este momento. "
                "Completa primero todas las preguntas de la reunión."
            )
            return
        
        # Obtener el archivo de foto más grande disponible
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        
        # Descargar y procesar la foto
        photo_bytes = await photo_file.download_as_bytearray()
        
        # Guardar foto usando el servicio
        result = photo_service.guardar_foto_evidencia(
            sesion['sesion_id'], 
            photo_bytes, 
            photo.file_id
        )
        
        if result['exito']:
            # Continuar con la conversación
            response = conversation_manager.procesar_foto_recibida(user_id, result['ruta_archivo'])
            await update.message.reply_text(response['mensaje'])
            
            # Si se completó la reunión, mostrar resumen final
            if response.get('estado') == 'completado':
                resumen = conversation_manager.generar_resumen_final(user_id)
                await update.message.reply_text(resumen, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                f"❌ Error al procesar la fotografía: {result['error']}"
            )
            
    except Exception as e:
        logger.error(f"Error procesando foto de usuario {user_id}: {e}")
        await update.message.reply_text(
            "❌ Ocurrió un error procesando la fotografía. Por favor, intenta enviarla de nuevo."
        )