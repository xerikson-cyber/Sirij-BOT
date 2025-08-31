# -*- coding: utf-8 -*-
"""
Configuración centralizada para SIRIJ BOT
"""

import os
from typing import Dict, Any

class Config:
    """Clase de configuración centralizada"""
    
    # Configuración de Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Configuración de Base de Datos
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///sirij_bot.db')
    
    # Configuración de Almacenamiento de Fotos
    PHOTO_STORAGE_PATH = os.getenv('PHOTO_STORAGE_PATH', './photos')
    PHOTO_MAX_SIZE_MB = int(os.getenv('PHOTO_MAX_SIZE_MB', '10'))
    
    # Configuración de Sesiones
    SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '60'))
    
    # Configuración de Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'sirij_bot.log')
    
    # Configuración de Debug
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Configuración de la aplicación
    APP_NAME = "SIRIJ BOT"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Bot para digitalizar Reuniones de Inicio de Jornada - CFE"
    
    # Mensajes del bot
    MESSAGES = {
        'welcome': (
            "¡Hola! 👋 Soy SIRIJ BOT, tu asistente para las Reuniones de Inicio de Jornada de CFE.\n\n"
            "Te ayudaré a completar el formulario de manera digital y sencilla. "
            "¿Estás listo para comenzar con el registro de hoy?"
        ),
        'help': (
            "🤖 *SIRIJ BOT - Ayuda*\n\n"
            "*Comandos disponibles:*\n"
            "• /start - Iniciar nueva reunión\n"
            "• /help - Mostrar esta ayuda\n"
            "• /cancel - Cancelar reunión actual\n"
            "• /status - Ver estado actual\n\n"
            "*¿Cómo funciona?*\n"
            "1. Usa /start para comenzar\n"
            "2. Responde las preguntas una por una\n"
            "3. Sube las fotos de evidencia\n"
            "4. Confirma y guarda tu reunión\n\n"
            "*Tipos de respuesta:*\n"
            "• Texto libre para nombres y descripciones\n"
            "• Fechas en formato YYYY-MM-DD\n"
            "• Horas en formato HH:MM\n"
            "• Sí/No para preguntas de verificación\n\n"
            "¿Necesitas ayuda? Contacta al administrador."
        ),
        'cancel_confirm': (
            "⚠️ ¿Estás seguro de que quieres cancelar la reunión actual?\n\n"
            "Se perderán todos los datos ingresados hasta ahora.\n\n"
            "Responde 'sí' para confirmar o 'no' para continuar."
        ),
        'cancelled': (
            "❌ Reunión cancelada.\n\n"
            "Todos los datos han sido eliminados. "
            "Puedes iniciar una nueva reunión cuando gustes con /start."
        ),
        'session_expired': (
            "⏰ Tu sesión ha expirado por inactividad.\n\n"
            "Por favor, inicia una nueva reunión con /start."
        ),
        'error_general': (
            "❌ Ha ocurrido un error inesperado.\n\n"
            "Por favor, intenta nuevamente o contacta al administrador si el problema persiste."
        ),
        'photo_uploaded': (
            "📸 ¡Foto recibida correctamente!\n\n"
            "Puedes subir más fotos o escribir 'continuar' para finalizar."
        ),
        'meeting_saved': (
            "✅ ¡Reunión guardada exitosamente!\n\n"
            "Gracias por usar SIRIJ BOT. Tu reunión ha sido registrada correctamente."
        ),
        'invalid_response': (
            "❌ Respuesta no válida.\n\n"
            "Por favor, revisa el formato solicitado e intenta nuevamente."
        )
    }
    
    # Configuración de validación
    VALIDATION_RULES = {
        'departamento': {
            'min_length': 2,
            'max_length': 100,
            'required': True
        },
        'categoria_maxima': {
            'min_length': 1,
            'max_length': 50,
            'required': True
        },
        'nombres_personal': {
            'min_length': 2,
            'max_length': 500,
            'required': True
        },
        'observaciones': {
            'max_length': 1000,
            'required': False
        },
        'otra_informacion': {
            'max_length': 500,
            'required': False
        },
        'meta_proposito_jornada': {
            'max_length': 500,
            'required': False
        }
    }
    
    # Configuración de preguntas
    QUESTION_CONFIG = {
        'max_retries': 3,
        'retry_delay_seconds': 1,
        'confirmation_required': True,
        'photo_required': True,
        'min_photos': 1,
        'max_photos': 10
    }
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """
        Valida la configuración y retorna errores si los hay
        
        Returns:
            Dict con errores de configuración
        """
        errors = []
        warnings = []
        
        # Validar token de Telegram
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN no está configurado")
        elif not cls.TELEGRAM_BOT_TOKEN.startswith('bot'):
            warnings.append("TELEGRAM_BOT_TOKEN no tiene el formato esperado")
        
        # Validar configuración de fotos
        if not os.path.exists(cls.PHOTO_STORAGE_PATH):
            try:
                os.makedirs(cls.PHOTO_STORAGE_PATH, exist_ok=True)
                warnings.append(f"Directorio de fotos creado: {cls.PHOTO_STORAGE_PATH}")
            except Exception as e:
                errors.append(f"No se puede crear directorio de fotos: {e}")
        
        # Validar configuración de base de datos
        if cls.DATABASE_URL.startswith('sqlite:'):
            db_path = cls.DATABASE_URL.replace('sqlite:///', '')
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                try:
                    os.makedirs(db_dir, exist_ok=True)
                except Exception as e:
                    errors.append(f"No se puede crear directorio de base de datos: {e}")
        
        # Validar configuración numérica
        if cls.PHOTO_MAX_SIZE_MB <= 0:
            errors.append("PHOTO_MAX_SIZE_MB debe ser mayor a 0")
        
        if cls.SESSION_TIMEOUT_MINUTES <= 0:
            errors.append("SESSION_TIMEOUT_MINUTES debe ser mayor a 0")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @classmethod
    def get_database_config(cls) -> Dict[str, str]:
        """
        Obtiene la configuración de base de datos parseada
        
        Returns:
            Dict con configuración de base de datos
        """
        if cls.DATABASE_URL.startswith('sqlite:'):
            return {
                'type': 'sqlite',
                'path': cls.DATABASE_URL.replace('sqlite:///', '')
            }
        elif cls.DATABASE_URL.startswith('postgresql:'):
            return {
                'type': 'postgresql',
                'url': cls.DATABASE_URL
            }
        else:
            return {
                'type': 'unknown',
                'url': cls.DATABASE_URL
            }
    
    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """
        Obtiene la configuración de logging
        
        Returns:
            Dict con configuración de logging
        """
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
                'detailed': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'level': cls.LOG_LEVEL,
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard'
                },
                'file': {
                    'level': cls.LOG_LEVEL,
                    'class': 'logging.FileHandler',
                    'filename': cls.LOG_FILE,
                    'formatter': 'detailed',
                    'encoding': 'utf-8'
                }
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': cls.LOG_LEVEL,
                    'propagate': False
                }
            }
        }
    
    @classmethod
    def print_config_summary(cls):
        """
        Imprime un resumen de la configuración actual
        """
        print(f"\n🤖 {cls.APP_NAME} v{cls.APP_VERSION}")
        print(f"📝 {cls.APP_DESCRIPTION}")
        print("\n⚙️  CONFIGURACIÓN:")
        print(f"• Debug: {'✅ Activado' if cls.DEBUG else '❌ Desactivado'}")
        print(f"• Log Level: {cls.LOG_LEVEL}")
        print(f"• Base de datos: {cls.get_database_config()['type']}")
        print(f"• Almacenamiento fotos: {cls.PHOTO_STORAGE_PATH}")
        print(f"• Tamaño máximo foto: {cls.PHOTO_MAX_SIZE_MB}MB")
        print(f"• Timeout sesión: {cls.SESSION_TIMEOUT_MINUTES} minutos")
        
        validation = cls.validate_config()
        if validation['errors']:
            print("\n❌ ERRORES DE CONFIGURACIÓN:")
            for error in validation['errors']:
                print(f"  • {error}")
        
        if validation['warnings']:
            print("\n⚠️  ADVERTENCIAS:")
            for warning in validation['warnings']:
                print(f"  • {warning}")
        
        if validation['valid']:
            print("\n✅ Configuración válida")
        else:
            print("\n❌ Configuración inválida - revisa los errores")
        
        print("\n" + "="*50)