#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIRIJ BOT - Chatbot para Reuniones de Inicio de Jornada CFE
Archivo principal de la aplicación
"""

import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Cargar variables de entorno
load_dotenv()

# Importar módulos del bot
from bot.handlers import (
    start_command,
    help_command,
    handle_message,
    handle_photo,
    cancel_command
)
from database.models import create_tables

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO'))
)
logger = logging.getLogger(__name__)

def main():
    """Función principal para iniciar el bot"""
    
    # Obtener token del bot
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN no encontrado en variables de entorno")
        return
    
    # Crear tablas de base de datos
    try:
        create_tables()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar base de datos: {e}")
        return
    
    # Crear aplicación del bot
    application = Application.builder().token(token).build()
    
    # Registrar manejadores de comandos
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    # Registrar manejadores de mensajes
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Iniciar el bot
    logger.info("Iniciando SIRIJ BOT...")
    application.run_polling(allowed_updates=['message'])

if __name__ == '__main__':
    main()