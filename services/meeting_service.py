# -*- coding: utf-8 -*-
"""
Servicio de gestión de reuniones para SIRIJ BOT
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from database.models import (
    save_complete_meeting,
    get_meeting_by_id,
    get_meetings_by_user,
    get_meeting_statistics,
    export_meetings_to_csv
)

logger = logging.getLogger(__name__)

class MeetingService:
    """Servicio para manejar la lógica de negocio de las reuniones"""
    
    def __init__(self):
        pass
    
    def save_meeting_from_session(self, session_data: Dict[str, Any]) -> Optional[str]:
        """
        Guarda una reunión completa basada en los datos de la sesión
        
        Args:
            session_data: Datos de la sesión con todas las respuestas
            
        Returns:
            str: ID de la reunión guardada o None si hubo error
        """
        try:
            answers = session_data.get('answers', {})
            photos = session_data.get('photos', [])
            user_id = session_data.get('user_id')
            
            # Preparar datos generales
            general_data = {
                'departamento': answers.get('departamento', ''),
                'fecha': answers.get('fecha', ''),
                'categoria_maxima': answers.get('categoria_maxima', ''),
                'nombres_personal': answers.get('nombres_personal', ''),
                'hora_inicio': answers.get('hora_inicio', ''),
                'hora_termino': answers.get('hora_termino', '')
            }
            
            # Preparar secciones S/N
            inicio_data = {
                'saludo_inicio_jornada': answers.get('saludo_inicio_jornada', False),
                'enumero_personal_participante': answers.get('enumero_personal_participante', False),
                'pregunto_estado_salud_participantes': answers.get('pregunto_estado_salud_participantes', False),
                'detectaron_anomalias_salud': answers.get('detectaron_anomalias_salud', False),
                'tomo_lista_asistencia': answers.get('tomo_lista_asistencia', False)
            }
            
            informacion_data = {
                'comentaron_trabajos_mantenimiento': answers.get('comentaron_trabajos_mantenimiento', False),
                'comentaron_trabajos_operacion': answers.get('comentaron_trabajos_operacion', False),
                'comentaron_trabajos_potencial_riesgo': answers.get('comentaron_trabajos_potencial_riesgo', False),
                'comentaron_incidentes_accidentes': answers.get('comentaron_incidentes_accidentes', False)
            }
            
            seguridad_data = {
                'realizo_revision_equipo': answers.get('realizo_revision_equipo', False),
                'comento_uso_epp': answers.get('comento_uso_epp', False),
                'dio_lectura_articulo_reglamento': answers.get('dio_lectura_articulo_reglamento', False),
                'relato_experiencia_peligro': answers.get('relato_experiencia_peligro', False),
                'actividades_relevantes_posteriores': answers.get('actividades_relevantes_posteriores', False),
                'especifico_actividades_seguridad': answers.get('especifico_actividades_seguridad', False)
            }
            
            # Preparar meta y observaciones
            meta_data = {
                'otra_informacion': answers.get('otra_informacion', ''),
                'meta_proposito_jornada': answers.get('meta_proposito_jornada', ''),
                'observaciones': answers.get('observaciones', '')
            }
            
            # Preparar evidencia
            evidencia_data = {
                'fotos_paths': [photo.get('path', '') for photo in photos],
                'total_fotos': len(photos),
                'usuario_telegram': user_id,
                'fecha_creacion': datetime.now().isoformat(),
                'completado_por_bot': True
            }
            
            # Guardar en la base de datos
            meeting_id = save_complete_meeting(
                general_data=general_data,
                inicio_data=inicio_data,
                informacion_data=informacion_data,
                seguridad_data=seguridad_data,
                meta_data=meta_data,
                evidencia_data=evidencia_data
            )
            
            if meeting_id:
                logger.info(f"Reunión guardada exitosamente con ID: {meeting_id}")
                return meeting_id
            else:
                logger.error("Error guardando reunión en la base de datos")
                return None
                
        except Exception as e:
            logger.error(f"Error guardando reunión desde sesión: {e}")
            return None
    
    def get_meeting_summary(self, meeting_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un resumen de una reunión
        
        Args:
            meeting_id: ID de la reunión
            
        Returns:
            Dict con el resumen de la reunión
        """
        try:
            meeting = get_meeting_by_id(meeting_id)
            if not meeting:
                return None
            
            # Contar respuestas positivas por sección
            inicio_positivas = sum([
                meeting.get('saludo_inicio_jornada', False),
                meeting.get('enumero_personal_participante', False),
                meeting.get('pregunto_estado_salud_participantes', False),
                meeting.get('detectaron_anomalias_salud', False),
                meeting.get('tomo_lista_asistencia', False)
            ])
            
            informacion_positivas = sum([
                meeting.get('comentaron_trabajos_mantenimiento', False),
                meeting.get('comentaron_trabajos_operacion', False),
                meeting.get('comentaron_trabajos_potencial_riesgo', False),
                meeting.get('comentaron_incidentes_accidentes', False)
            ])
            
            seguridad_positivas = sum([
                meeting.get('realizo_revision_equipo', False),
                meeting.get('comento_uso_epp', False),
                meeting.get('dio_lectura_articulo_reglamento', False),
                meeting.get('relato_experiencia_peligro', False),
                meeting.get('actividades_relevantes_posteriores', False),
                meeting.get('especifico_actividades_seguridad', False)
            ])
            
            return {
                'id': meeting_id,
                'departamento': meeting.get('departamento', ''),
                'fecha': meeting.get('fecha', ''),
                'hora_inicio': meeting.get('hora_inicio', ''),
                'hora_termino': meeting.get('hora_termino', ''),
                'total_fotos': meeting.get('total_fotos', 0),
                'secciones': {
                    'inicio': f"{inicio_positivas}/5",
                    'informacion': f"{informacion_positivas}/4",
                    'seguridad': f"{seguridad_positivas}/6"
                },
                'completitud': {
                    'inicio': round((inicio_positivas / 5) * 100, 1),
                    'informacion': round((informacion_positivas / 4) * 100, 1),
                    'seguridad': round((seguridad_positivas / 6) * 100, 1)
                },
                'fecha_creacion': meeting.get('fecha_creacion', ''),
                'usuario': meeting.get('usuario_telegram', '')
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo resumen de reunión {meeting_id}: {e}")
            return None
    
    def get_user_meetings(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene las reuniones de un usuario
        
        Args:
            user_id: ID del usuario
            limit: Límite de reuniones a obtener
            
        Returns:
            Lista de reuniones del usuario
        """
        try:
            meetings = get_meetings_by_user(user_id, limit)
            summaries = []
            
            for meeting in meetings:
                summary = self.get_meeting_summary(meeting['id'])
                if summary:
                    summaries.append(summary)
            
            return summaries
            
        except Exception as e:
            logger.error(f"Error obteniendo reuniones del usuario {user_id}: {e}")
            return []
    
    def validate_meeting_data(self, answers: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Valida los datos de una reunión antes de guardarla
        
        Args:
            answers: Respuestas de la sesión
            
        Returns:
            Dict con errores encontrados por categoría
        """
        errors = {
            'required': [],
            'format': [],
            'logic': []
        }
        
        # Validar campos requeridos
        required_fields = [
            'departamento', 'fecha', 'categoria_maxima', 
            'nombres_personal', 'hora_inicio', 'hora_termino'
        ]
        
        for field in required_fields:
            if not answers.get(field):
                errors['required'].append(f"Campo requerido: {field}")
        
        # Validar formato de fecha
        fecha = answers.get('fecha')
        if fecha:
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                errors['format'].append("Formato de fecha inválido (debe ser YYYY-MM-DD)")
        
        # Validar formato de horas
        hora_inicio = answers.get('hora_inicio')
        hora_termino = answers.get('hora_termino')
        
        if hora_inicio:
            try:
                datetime.strptime(hora_inicio, '%H:%M')
            except ValueError:
                errors['format'].append("Formato de hora de inicio inválido (debe ser HH:MM)")
        
        if hora_termino:
            try:
                datetime.strptime(hora_termino, '%H:%M')
            except ValueError:
                errors['format'].append("Formato de hora de término inválido (debe ser HH:MM)")
        
        # Validar lógica de horas
        if hora_inicio and hora_termino:
            try:
                inicio = datetime.strptime(hora_inicio, '%H:%M')
                termino = datetime.strptime(hora_termino, '%H:%M')
                if termino <= inicio:
                    errors['logic'].append("La hora de término debe ser posterior a la hora de inicio")
            except ValueError:
                pass  # Ya se reportó el error de formato
        
        return errors
    
    def get_statistics(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene estadísticas generales de las reuniones
        
        Returns:
            Dict con estadísticas o None si hay error
        """
        try:
            return get_meeting_statistics()
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return None
    
    def export_meetings(self, output_path: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> bool:
        """
        Exporta reuniones a CSV
        
        Args:
            output_path: Ruta del archivo de salida
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)
            
        Returns:
            bool: True si se exportó exitosamente
        """
        try:
            return export_meetings_to_csv(output_path, start_date, end_date)
        except Exception as e:
            logger.error(f"Error exportando reuniones: {e}")
            return False
    
    def generate_meeting_report(self, meeting_id: str) -> Optional[str]:
        """
        Genera un reporte textual de una reunión
        
        Args:
            meeting_id: ID de la reunión
            
        Returns:
            str: Reporte en formato texto
        """
        try:
            meeting = get_meeting_by_id(meeting_id)
            if not meeting:
                return None
            
            report = f"""📋 REPORTE DE REUNIÓN DE INICIO DE JORNADA

🏢 DATOS GENERALES:
• Departamento: {meeting.get('departamento', 'N/A')}
• Fecha: {meeting.get('fecha', 'N/A')}
• Categoría máxima: {meeting.get('categoria_maxima', 'N/A')}
• Hora inicio: {meeting.get('hora_inicio', 'N/A')}
• Hora término: {meeting.get('hora_termino', 'N/A')}
• Personal: {meeting.get('nombres_personal', 'N/A')}

🚀 SECCIÓN INICIO:
• Saludo inicio de jornada: {'✅ Sí' if meeting.get('saludo_inicio_jornada') else '❌ No'}
• Enumeró personal participante: {'✅ Sí' if meeting.get('enumero_personal_participante') else '❌ No'}
• Preguntó estado de salud: {'✅ Sí' if meeting.get('pregunto_estado_salud_participantes') else '❌ No'}
• Detectaron anomalías de salud: {'✅ Sí' if meeting.get('detectaron_anomalias_salud') else '❌ No'}
• Tomó lista de asistencia: {'✅ Sí' if meeting.get('tomo_lista_asistencia') else '❌ No'}

📢 SECCIÓN INFORMACIÓN:
• Comentaron trabajos de mantenimiento: {'✅ Sí' if meeting.get('comentaron_trabajos_mantenimiento') else '❌ No'}
• Comentaron trabajos de operación: {'✅ Sí' if meeting.get('comentaron_trabajos_operacion') else '❌ No'}
• Comentaron trabajos con potencial de riesgo: {'✅ Sí' if meeting.get('comentaron_trabajos_potencial_riesgo') else '❌ No'}
• Comentaron incidentes o accidentes: {'✅ Sí' if meeting.get('comentaron_incidentes_accidentes') else '❌ No'}

🛡️ SECCIÓN ACTIVIDADES DE SEGURIDAD:
• Realizó revisión de equipo: {'✅ Sí' if meeting.get('realizo_revision_equipo') else '❌ No'}
• Comentó uso de EPP: {'✅ Sí' if meeting.get('comento_uso_epp') else '❌ No'}
• Dio lectura a artículo del reglamento: {'✅ Sí' if meeting.get('dio_lectura_articulo_reglamento') else '❌ No'}
• Relató experiencia de peligro: {'✅ Sí' if meeting.get('relato_experiencia_peligro') else '❌ No'}
• Actividades relevantes posteriores: {'✅ Sí' if meeting.get('actividades_relevantes_posteriores') else '❌ No'}
• Especificó actividades de seguridad: {'✅ Sí' if meeting.get('especifico_actividades_seguridad') else '❌ No'}

📝 INFORMACIÓN ADICIONAL:
• Otra información: {meeting.get('otra_informacion', 'N/A')}
• Meta/Propósito de la jornada: {meeting.get('meta_proposito_jornada', 'N/A')}
• Observaciones: {meeting.get('observaciones', 'N/A')}

📸 EVIDENCIA:
• Total de fotos: {meeting.get('total_fotos', 0)}
• Fecha de creación: {meeting.get('fecha_creacion', 'N/A')}
• Usuario: {meeting.get('usuario_telegram', 'N/A')}
"""
            
            return report
            
        except Exception as e:
            logger.error(f"Error generando reporte de reunión {meeting_id}: {e}")
            return None