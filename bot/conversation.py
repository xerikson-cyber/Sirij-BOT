# -*- coding: utf-8 -*-
"""
Lógica de conversación para SIRIJ BOT
Maneja el flujo de preguntas y respuestas del formulario
"""

import logging
from datetime import datetime
from typing import Dict, Any

from .validators import ResponseValidator
from services.session_service import SessionService
from database.models import guardar_reunion_completa

logger = logging.getLogger(__name__)

class ConversationManager:
    """
    Maneja el flujo de conversación del bot
    """
    
    def __init__(self):
        self.validator = ResponseValidator()
        self.session_service = SessionService()
        
        # Definir el flujo de preguntas
        self.preguntas = {
            'departamento': {
                'texto': 'Perfecto. Comenzaremos con los datos generales.\n¿Cuál es el nombre del Departamento?',
                'tipo': 'texto',
                'siguiente': 'fecha'
            },
            'fecha': {
                'texto': 'Gracias. ¿Cuál es la fecha de hoy? (formato: DD/MM/AAAA)',
                'tipo': 'fecha',
                'siguiente': 'categoria_maxima'
            },
            'categoria_maxima': {
                'texto': '¿Cuál es la categoría máxima representada en la reunión?',
                'tipo': 'texto',
                'siguiente': 'nombre_supervisor'
            },
            'nombre_supervisor': {
                'texto': '¿Cuál es tu nombre como supervisor?',
                'tipo': 'texto',
                'siguiente': 'nombres_personal'
            },
            'nombres_personal': {
                'texto': 'Ahora necesito los nombres del personal que participó en la reunión.\nPuedes escribir los nombres separados por comas.',
                'tipo': 'lista_nombres',
                'siguiente': 'hora_inicio'
            },
            'hora_inicio': {
                'texto': '¿A qué hora inició la reunión? (formato: HH:MM)',
                'tipo': 'hora',
                'siguiente': 'hora_termino'
            },
            'hora_termino': {
                'texto': '¿A qué hora terminó la reunión? (formato: HH:MM)',
                'tipo': 'hora',
                'siguiente': 'saludo_inicio_jornada'
            },
            
            # Sección INICIO
            'saludo_inicio_jornada': {
                'texto': 'Excelente. Ahora pasaremos a la sección de INICIO.\n¿Se realizó el saludo de inicio de jornada? (Responde: Sí o No)',
                'tipo': 'boolean',
                'siguiente': 'enumero_personal'
            },
            'enumero_personal': {
                'texto': '¿Se enumeró al personal participante? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'pregunto_estado_salud'
            },
            'pregunto_estado_salud': {
                'texto': '¿Se preguntó el estado de salud de los participantes? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'realizo_ejercicios'
            },
            'realizo_ejercicios': {
                'texto': '¿Se realizaron los ejercicios? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'detecto_anomalias_salud'
            },
            'detecto_anomalias_salud': {
                'texto': '¿Se detectaron anomalías en el estado de salud? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'tomo_lista_asistencia'
            },
            'tomo_lista_asistencia': {
                'texto': '¿Se tomó lista de asistencia? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'comento_trabajos_mantenimiento'
            },
            
            # Sección INFORMACIÓN
            'comento_trabajos_mantenimiento': {
                'texto': 'Ahora la sección de INFORMACIÓN.\n¿Se comentaron trabajos de mantenimiento relevantes? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'comento_trabajos_operacion'
            },
            'comento_trabajos_operacion': {
                'texto': '¿Se comentaron trabajos de operación relevantes? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'comento_trabajos_alto_riesgo'
            },
            'comento_trabajos_alto_riesgo': {
                'texto': '¿Se comentaron trabajos con potencial de alto riesgo? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'comento_incidentes_accidentes'
            },
            'comento_incidentes_accidentes': {
                'texto': '¿Se comentaron incidentes o accidentes ocurridos? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'otra_informacion'
            },
            'otra_informacion': {
                'texto': '¿Hay otra información relevante que quieras agregar?\nSi es así, especifica los temas tratados. Si no, escribe "No".',
                'tipo': 'texto_opcional',
                'siguiente': 'realizo_revision_espejo'
            },
            
            # Sección ACTIVIDADES DE SEGURIDAD
            'realizo_revision_espejo': {
                'texto': 'Continuamos con ACTIVIDADES DE SEGURIDAD.\n¿Se realizó la revisión espejo? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'realizo_prediccion_peligro'
            },
            'realizo_prediccion_peligro': {
                'texto': '¿Se realizó actividad de predicción de peligro (APP)? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'dio_lectura_reglamento'
            },
            'dio_lectura_reglamento': {
                'texto': '¿Se dio lectura a un artículo del reglamento de seguridad e higiene? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'realizo_exposicion_sentir_peligro'
            },
            'realizo_exposicion_sentir_peligro': {
                'texto': '¿Se realizó una exposición de sentir el peligro (justo)? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'actividades_posteriores'
            },
            'actividades_posteriores': {
                'texto': '¿Se realizaron actividades relevantes posteriores (inspecciones, campañas, etc.)? (Sí/No)',
                'tipo': 'boolean',
                'siguiente': 'descripcion_actividades_seguridad'
            },
            'descripcion_actividades_seguridad': {
                'texto': 'Especifica las actividades de seguridad que se realizaron:',
                'tipo': 'texto',
                'siguiente': 'meta_proposito_jornada'
            },
            
            # Sección META/PROPÓSITO
            'meta_proposito_jornada': {
                'texto': '¿Cuál es la meta o propósito de la jornada?',
                'tipo': 'texto',
                'siguiente': 'observaciones'
            },
            
            # Sección OBSERVACIONES
            'observaciones': {
                'texto': '¿Tienes alguna observación adicional? Si no, escribe "No".',
                'tipo': 'texto_opcional',
                'siguiente': 'solicitar_foto'
            },
            
            'solicitar_foto': {
                'texto': 'Perfecto. Para finalizar, necesito que subas una fotografía como evidencia de la reunión.\nPor favor, envía la imagen.',
                'tipo': 'foto',
                'siguiente': None
            }
        }
    
    def iniciar_reunion(self, user_id: int) -> Dict[str, Any]:
        """
        Inicia una nueva reunión para el usuario
        """
        try:
            # Verificar si hay sesión activa
            sesion_activa = self.session_service.obtener_sesion_activa(user_id)
            
            if sesion_activa:
                return {
                    'mensaje': '⚠️ Ya tienes una reunión en progreso.\n\n'
                              '¿Quieres continuar con la reunión actual o cancelarla para iniciar una nueva?\n\n'
                              'Responde "Continuar" o "Nueva"',
                    'estado': 'sesion_existente'
                }
            
            # Crear nueva sesión
            sesion = self.session_service.crear_nueva_sesion(user_id)
            
            return {
                'mensaje': '¡Hola! Soy SIRIJ BOT, tu asistente para las Reuniones de Inicio de Jornada de CFE. '
                          '¿Estás listo para comenzar con el registro de hoy?\n\n'
                          'Responde "Sí" para continuar.',
                'sesion_id': sesion['sesion_id'],
                'estado': 'esperando_confirmacion'
            }
            
        except Exception as e:
            logger.error(f"Error iniciando reunión para usuario {user_id}: {e}")
            return {
                'mensaje': '❌ Error al iniciar la reunión. Por favor, intenta de nuevo.',
                'estado': 'error'
            }
    
    def procesar_mensaje(self, user_id: int, mensaje: str) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario y determina la respuesta
        """
        try:
            # Obtener sesión activa
            sesion = self.session_service.obtener_sesion_activa(user_id)
            
            if not sesion:
                return {
                    'mensaje': 'ℹ️ No tienes una reunión activa. Usa /start para comenzar.',
                    'estado': 'sin_sesion'
                }
            
            estado_actual = sesion.get('estado', 'esperando_confirmacion')
            
            # Manejar diferentes estados
            if estado_actual == 'esperando_confirmacion':
                return self._manejar_confirmacion_inicial(user_id, mensaje, sesion)
            
            elif estado_actual == 'sesion_existente':
                return self._manejar_sesion_existente(user_id, mensaje, sesion)
            
            elif estado_actual == 'esperando_respuesta':
                return self._manejar_respuesta_pregunta(user_id, mensaje, sesion)
            
            elif estado_actual == 'esperando_foto':
                return {
                    'mensaje': '📷 Estoy esperando que envíes una fotografía como evidencia. '
                              'Por favor, envía la imagen (no texto).',
                    'estado': 'esperando_foto'
                }
            
            else:
                return {
                    'mensaje': '❌ Estado de conversación no reconocido. Usa /cancel para reiniciar.',
                    'estado': 'error'
                }
                
        except Exception as e:
            logger.error(f"Error procesando mensaje de usuario {user_id}: {e}")
            return {
                'mensaje': '❌ Error procesando tu mensaje. Usa /cancel para reiniciar.',
                'estado': 'error'
            }
    
    def _manejar_confirmacion_inicial(self, user_id: int, mensaje: str, sesion: Dict) -> Dict[str, Any]:
        """
        Maneja la confirmación inicial para comenzar la reunión
        """
        respuesta_lower = mensaje.lower().strip()
        
        if respuesta_lower in ['sí', 'si', 's', 'yes', 'y']:
            # Comenzar con la primera pregunta
            primera_pregunta = 'departamento'
            config_pregunta = self.preguntas[primera_pregunta]
            
            # Actualizar sesión
            self.session_service.actualizar_estado_sesion(
                sesion['sesion_id'], 
                'esperando_respuesta',
                {'pregunta_actual': primera_pregunta}
            )
            
            return {
                'mensaje': config_pregunta['texto'],
                'estado': 'esperando_respuesta',
                'pregunta_actual': primera_pregunta
            }
        
        elif respuesta_lower in ['no', 'n']:
            # Cancelar sesión
            self.session_service.cancelar_sesion(user_id)
            return {
                'mensaje': '👋 Entendido. Cuando estés listo para registrar una reunión, usa /start.',
                'estado': 'cancelado'
            }
        
        else:
            return {
                'mensaje': 'Por favor, responde "Sí" para comenzar o "No" para cancelar.',
                'estado': 'esperando_confirmacion'
            }
    
    def _manejar_sesion_existente(self, user_id: int, mensaje: str, sesion: Dict) -> Dict[str, Any]:
        """
        Maneja la decisión sobre sesión existente
        """
        respuesta_lower = mensaje.lower().strip()
        
        if respuesta_lower in ['continuar', 'continúa', 'continua']:
            # Continuar con la sesión existente
            pregunta_actual = sesion.get('pregunta_actual', 'departamento')
            config_pregunta = self.preguntas.get(pregunta_actual)
            
            if config_pregunta:
                self.session_service.actualizar_estado_sesion(
                    sesion['sesion_id'], 
                    'esperando_respuesta'
                )
                
                return {
                    'mensaje': f"Continuando con la reunión...\n\n{config_pregunta['texto']}",
                    'estado': 'esperando_respuesta',
                    'pregunta_actual': pregunta_actual
                }
        
        elif respuesta_lower in ['nueva', 'nuevo', 'cancelar']:
            # Cancelar sesión actual y crear nueva
            self.session_service.cancelar_sesion(user_id)
            return self.iniciar_reunion(user_id)
        
        return {
            'mensaje': 'Por favor, responde "Continuar" para seguir con la reunión actual o "Nueva" para cancelar y empezar de nuevo.',
            'estado': 'sesion_existente'
        }
    
    def _manejar_respuesta_pregunta(self, user_id: int, mensaje: str, sesion: Dict) -> Dict[str, Any]:
        """
        Maneja la respuesta a una pregunta específica
        """
        pregunta_actual = sesion.get('pregunta_actual')
        config_pregunta = self.preguntas.get(pregunta_actual)
        
        if not config_pregunta:
            return {
                'mensaje': '❌ Error en el flujo de conversación. Usa /cancel para reiniciar.',
                'estado': 'error'
            }
        
        # Validar respuesta
        validacion = self.validator.validar_respuesta(mensaje, config_pregunta['tipo'])
        
        if not validacion['valida']:
            return {
                'mensaje': f"Por favor, {validacion['mensaje_error']}",
                'estado': 'esperando_respuesta',
                'pregunta_actual': pregunta_actual
            }
        
        # Guardar respuesta
        self.session_service.guardar_respuesta(
            sesion['sesion_id'], 
            pregunta_actual, 
            validacion['valor_procesado']
        )
        
        # Determinar siguiente pregunta
        siguiente_pregunta = config_pregunta['siguiente']
        
        if siguiente_pregunta and siguiente_pregunta != 'solicitar_foto':
            # Continuar con siguiente pregunta
            config_siguiente = self.preguntas[siguiente_pregunta]
            
            self.session_service.actualizar_estado_sesion(
                sesion['sesion_id'],
                'esperando_respuesta',
                {'pregunta_actual': siguiente_pregunta}
            )
            
            return {
                'mensaje': config_siguiente['texto'],
                'estado': 'esperando_respuesta',
                'pregunta_actual': siguiente_pregunta
            }
        
        elif siguiente_pregunta == 'solicitar_foto':
            # Solicitar fotografía
            self.session_service.actualizar_estado_sesion(
                sesion['sesion_id'],
                'esperando_foto'
            )
            
            return {
                'mensaje': self.preguntas['solicitar_foto']['texto'],
                'estado': 'esperando_foto'
            }
        
        else:
            # No debería llegar aquí, pero por seguridad
            return {
                'mensaje': '❌ Error en el flujo de conversación. Usa /cancel para reiniciar.',
                'estado': 'error'
            }
    
    def procesar_foto_recibida(self, user_id: int, ruta_foto: str) -> Dict[str, Any]:
        """
        Procesa la fotografía recibida y finaliza la reunión
        """
        try:
            sesion = self.session_service.obtener_sesion_activa(user_id)
            
            if not sesion or sesion.get('estado') != 'esperando_foto':
                return {
                    'mensaje': '❌ Error: no se esperaba una fotografía en este momento.',
                    'estado': 'error'
                }
            
            # Actualizar sesión con la ruta de la foto
            self.session_service.guardar_respuesta(
                sesion['sesion_id'],
                'ruta_evidencia_fotografica',
                ruta_foto
            )
            
            # Generar resumen para confirmación
            resumen = self._generar_resumen_confirmacion(sesion['sesion_id'])
            
            # Actualizar estado para esperar confirmación final
            self.session_service.actualizar_estado_sesion(
                sesion['sesion_id'],
                'esperando_confirmacion_final'
            )
            
            return {
                'mensaje': f"¡Excelente! He registrado toda la información de la Reunión de Inicio de Jornada.\n\n"
                          f"{resumen}\n\n"
                          f"¿Confirmas que toda la información es correcta? (Sí/No)",
                'estado': 'esperando_confirmacion_final'
            }
            
        except Exception as e:
            logger.error(f"Error procesando foto de usuario {user_id}: {e}")
            return {
                'mensaje': '❌ Error procesando la fotografía. Intenta de nuevo.',
                'estado': 'error'
            }
    
    def _generar_resumen_confirmacion(self, sesion_id: str) -> str:
        """
        Genera un resumen de la información para confirmación
        """
        datos = self.session_service.obtener_datos_sesion_completa(sesion_id)
        
        resumen = "📋 **RESUMEN:**\n"
        resumen += f"• Departamento: {datos.get('departamento', 'N/A')}\n"
        resumen += f"• Fecha: {datos.get('fecha', 'N/A')}\n"
        resumen += f"• Supervisor: {datos.get('nombre_supervisor', 'N/A')}\n"
        
        if datos.get('nombres_personal'):
            nombres = ', '.join(datos['nombres_personal'])
            resumen += f"• Personal: {nombres}\n"
        
        resumen += f"• Horario: {datos.get('hora_inicio', 'N/A')} - {datos.get('hora_termino', 'N/A')}\n"
        resumen += f"• Evidencia fotográfica: ✅ Guardada"
        
        return resumen
    
    def generar_resumen_final(self, user_id: int) -> str:
        """
        Genera el resumen final después de guardar en base de datos
        """
        try:
            sesion = self.session_service.obtener_sesion_activa(user_id)
            
            if not sesion:
                return "❌ Error generando resumen final."
            
            # Obtener todos los datos y guardar en base de datos
            datos_completos = self.session_service.obtener_datos_sesion_completa(sesion['sesion_id'])
            
            # Guardar en base de datos
            resultado = guardar_reunion_completa(datos_completos)
            
            i# REEMPLAZA LA PARTE FINAL DE LA FUNCIÓN CON ESTO

        if resultado['exito']:
            # Limpiar sesión
            self.session_service.finalizar_sesion(sesion['sesion_id'])

            return (f"""✅ **¡Reunión registrada exitosamente!**

🆔 **ID de registro:** {resultado['reunion_id']}
📅 **Fecha de registro:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

¡Gracias por usar SIRIJ BOT! 🚀

Usa /start cuando necesites registrar otra reunión.""")
        else:
            return f"❌ **Error al guardar la reunión:**\n{resultado['error']}\n\n" \
                   f"Por favor, contacta al administrador."

    except Exception as e:
        logger.error(f"Error generando resumen final para usuario {user_id}: {e}")
        return "❌ Error generando resumen final. Contacta al administrador."
                
                # actualizacion de error
return (f"""✅ **¡Reunión registrada exitosamente!**
            else:
                return f"❌ **Error al guardar la reunión:**\n{resultado['error']}\n\n"
                      f"Por favor, contacta al administrador."
                      
        except Exception as e:
            logger.error(f"Error generando resumen final para usuario {user_id}: {e}")
            return "❌ Error generando resumen final. Contacta al administrador."