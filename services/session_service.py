# -*- coding: utf-8 -*-
"""
Servicio de gestión de sesiones temporales para SIRIJ BOT
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from database.models import (
    get_db_connection, 
    save_session, 
    get_session, 
    update_session, 
    delete_session,
    clean_expired_sessions
)

logger = logging.getLogger(__name__)

class SessionService:
    """Servicio para manejar sesiones temporales de usuarios"""
    
    def __init__(self, session_timeout_minutes: int = 60):
        self.session_timeout = session_timeout_minutes
    
    def create_session(self, user_id: str, chat_id: str) -> bool:
        """
        Crea una nueva sesión para el usuario
        
        Args:
            user_id: ID del usuario
            chat_id: ID del chat
            
        Returns:
            bool: True si se creó exitosamente
        """
        try:
            session_data = {
                'current_question': 0,
                'answers': {},
                'photos': [],
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
            
            return save_session(
                user_id=user_id,
                chat_id=chat_id,
                session_data=json.dumps(session_data, ensure_ascii=False)
            )
            
        except Exception as e:
            logger.error(f"Error creando sesión para usuario {user_id}: {e}")
            return False
    
    def get_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene la sesión activa del usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Dict con los datos de la sesión o None si no existe
        """
        try:
            session = get_session(user_id)
            if not session:
                return None
            
            # Verificar si la sesión ha expirado
            created_at = datetime.fromisoformat(session['created_at'])
            if datetime.now() - created_at > timedelta(minutes=self.session_timeout):
                self.delete_session(user_id)
                return None
            
            # Parsear los datos de la sesión
            session_data = json.loads(session['session_data'])
            session_data.update({
                'user_id': session['user_id'],
                'chat_id': session['chat_id'],
                'created_at': session['created_at']
            })
            
            return session_data
            
        except Exception as e:
            logger.error(f"Error obteniendo sesión para usuario {user_id}: {e}")
            return None
    
    def update_session(self, user_id: str, session_data: Dict[str, Any]) -> bool:
        """
        Actualiza los datos de la sesión
        
        Args:
            user_id: ID del usuario
            session_data: Nuevos datos de la sesión
            
        Returns:
            bool: True si se actualizó exitosamente
        """
        try:
            # Remover campos que no deben guardarse en session_data
            clean_data = session_data.copy()
            clean_data.pop('user_id', None)
            clean_data.pop('chat_id', None)
            clean_data.pop('created_at', None)
            
            return update_session(
                user_id=user_id,
                session_data=json.dumps(clean_data, ensure_ascii=False)
            )
            
        except Exception as e:
            logger.error(f"Error actualizando sesión para usuario {user_id}: {e}")
            return False
    
    def delete_session(self, user_id: str) -> bool:
        """
        Elimina la sesión del usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            return delete_session(user_id)
            
        except Exception as e:
            logger.error(f"Error eliminando sesión para usuario {user_id}: {e}")
            return False
    
    def add_answer(self, user_id: str, question_key: str, answer: Any) -> bool:
        """
        Agrega una respuesta a la sesión
        
        Args:
            user_id: ID del usuario
            question_key: Clave de la pregunta
            answer: Respuesta del usuario
            
        Returns:
            bool: True si se agregó exitosamente
        """
        session = self.get_session(user_id)
        if not session:
            return False
        
        session['answers'][question_key] = answer
        return self.update_session(user_id, session)
    
    def add_photo(self, user_id: str, photo_path: str) -> bool:
        """
        Agrega una foto a la sesión
        
        Args:
            user_id: ID del usuario
            photo_path: Ruta de la foto guardada
            
        Returns:
            bool: True si se agregó exitosamente
        """
        session = self.get_session(user_id)
        if not session:
            return False
        
        if 'photos' not in session:
            session['photos'] = []
        
        session['photos'].append({
            'path': photo_path,
            'uploaded_at': datetime.now().isoformat()
        })
        
        return self.update_session(user_id, session)
    
    def advance_question(self, user_id: str) -> bool:
        """
        Avanza a la siguiente pregunta
        
        Args:
            user_id: ID del usuario
            
        Returns:
            bool: True si se avanzó exitosamente
        """
        session = self.get_session(user_id)
        if not session:
            return False
        
        session['current_question'] += 1
        return self.update_session(user_id, session)
    
    def set_status(self, user_id: str, status: str) -> bool:
        """
        Establece el estado de la sesión
        
        Args:
            user_id: ID del usuario
            status: Nuevo estado (active, waiting_photo, completed, cancelled)
            
        Returns:
            bool: True si se estableció exitosamente
        """
        session = self.get_session(user_id)
        if not session:
            return False
        
        session['status'] = status
        return self.update_session(user_id, session)
    
    def clean_expired_sessions(self) -> int:
        """
        Limpia las sesiones expiradas
        
        Returns:
            int: Número de sesiones eliminadas
        """
        try:
            return clean_expired_sessions(self.session_timeout)
        except Exception as e:
            logger.error(f"Error limpiando sesiones expiradas: {e}")
            return 0
    
    def get_session_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un resumen de la sesión para confirmación
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Dict con el resumen de la sesión
        """
        session = self.get_session(user_id)
        if not session:
            return None
        
        answers = session.get('answers', {})
        photos = session.get('photos', [])
        
        return {
            'total_questions': len(answers),
            'total_photos': len(photos),
            'status': session.get('status', 'unknown'),
            'created_at': session.get('created_at'),
            'answers': answers,
            'photos': [photo['path'] for photo in photos]
        }