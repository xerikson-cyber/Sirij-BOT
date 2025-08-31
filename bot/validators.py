# -*- coding: utf-8 -*-
"""
Validadores de respuestas para SIRIJ BOT
Valida diferentes tipos de entrada del usuario
"""

import re
from datetime import datetime
from typing import Dict, Any, List

class ResponseValidator:
    """
    Clase para validar diferentes tipos de respuestas del usuario
    """
    
    def validar_respuesta(self, respuesta: str, tipo: str) -> Dict[str, Any]:
        """
        Valida una respuesta según el tipo especificado
        
        Args:
            respuesta: La respuesta del usuario
            tipo: El tipo de validación a aplicar
            
        Returns:
            Dict con 'valida', 'valor_procesado' y 'mensaje_error'
        """
        respuesta = respuesta.strip()
        
        if tipo == 'boolean':
            return self._validar_boolean(respuesta)
        elif tipo == 'fecha':
            return self._validar_fecha(respuesta)
        elif tipo == 'hora':
            return self._validar_hora(respuesta)
        elif tipo == 'texto':
            return self._validar_texto(respuesta)
        elif tipo == 'texto_opcional':
            return self._validar_texto_opcional(respuesta)
        elif tipo == 'lista_nombres':
            return self._validar_lista_nombres(respuesta)
        else:
            return {
                'valida': False,
                'mensaje_error': 'tipo de validación no reconocido'
            }
    
    def _validar_boolean(self, respuesta: str) -> Dict[str, Any]:
        """
        Valida respuestas Sí/No
        """
        respuesta_lower = respuesta.lower()
        
        # Respuestas afirmativas
        if respuesta_lower in ['sí', 'si', 's', 'yes', 'y', '1', 'true', 'verdadero']:
            return {
                'valida': True,
                'valor_procesado': True
            }
        
        # Respuestas negativas
        elif respuesta_lower in ['no', 'n', '0', 'false', 'falso']:
            return {
                'valida': True,
                'valor_procesado': False
            }
        
        else:
            return {
                'valida': False,
                'mensaje_error': 'responde con "Sí" o "No"'
            }
    
    def _validar_fecha(self, respuesta: str) -> Dict[str, Any]:
        """
        Valida formato de fecha DD/MM/AAAA
        """
        # Patrones de fecha aceptados
        patrones = [
            r'^(\d{1,2})/(\d{1,2})/(\d{4})$',  # DD/MM/AAAA o D/M/AAAA
            r'^(\d{1,2})-(\d{1,2})-(\d{4})$',  # DD-MM-AAAA o D-M-AAAA
            r'^(\d{1,2})\.(\d{1,2})\.(\d{4})$'  # DD.MM.AAAA o D.M.AAAA
        ]
        
        for patron in patrones:
            match = re.match(patron, respuesta)
            if match:
                dia, mes, año = match.groups()
                
                try:
                    # Validar que sea una fecha válida
                    fecha_obj = datetime(int(año), int(mes), int(dia))
                    
                    # Verificar que no sea una fecha futura muy lejana
                    año_actual = datetime.now().year
                    if int(año) > año_actual + 1:
                        return {
                            'valida': False,
                            'mensaje_error': f'el año no puede ser mayor a {año_actual + 1}'
                        }
                    
                    # Verificar que no sea muy antigua (más de 10 años)
                    if int(año) < año_actual - 10:
                        return {
                            'valida': False,
                            'mensaje_error': f'el año no puede ser menor a {año_actual - 10}'
                        }
                    
                    return {
                        'valida': True,
                        'valor_procesado': fecha_obj.date()
                    }
                    
                except ValueError:
                    continue
        
        return {
            'valida': False,
            'mensaje_error': 'ingresa la fecha en formato DD/MM/AAAA (ejemplo: 15/03/2024)'
        }
    
    def _validar_hora(self, respuesta: str) -> Dict[str, Any]:
        """
        Valida formato de hora HH:MM
        """
        # Patrones de hora aceptados
        patrones = [
            r'^(\d{1,2}):(\d{2})$',  # HH:MM o H:MM
            r'^(\d{1,2})\.(\d{2})$',  # HH.MM o H.MM
            r'^(\d{1,2})h(\d{2})$',   # HHhMM o HhMM
            r'^(\d{1,2}):(\d{2}):(\d{2})$'  # HH:MM:SS (ignorar segundos)
        ]
        
        for i, patron in enumerate(patrones):
            match = re.match(patron, respuesta)
            if match:
                if i == 3:  # Formato con segundos
                    hora, minuto, segundo = match.groups()
                else:
                    hora, minuto = match.groups()
                
                try:
                    hora_int = int(hora)
                    minuto_int = int(minuto)
                    
                    # Validar rangos
                    if not (0 <= hora_int <= 23):
                        return {
                            'valida': False,
                            'mensaje_error': 'la hora debe estar entre 00 y 23'
                        }
                    
                    if not (0 <= minuto_int <= 59):
                        return {
                            'valida': False,
                            'mensaje_error': 'los minutos deben estar entre 00 y 59'
                        }
                    
                    # Crear objeto time
                    hora_obj = datetime.strptime(f"{hora_int:02d}:{minuto_int:02d}", '%H:%M').time()
                    
                    return {
                        'valida': True,
                        'valor_procesado': hora_obj
                    }
                    
                except ValueError:
                    continue
        
        return {
            'valida': False,
            'mensaje_error': 'ingresa la hora en formato HH:MM (ejemplo: 08:30)'
        }
    
    def _validar_texto(self, respuesta: str) -> Dict[str, Any]:
        """
        Valida texto obligatorio
        """
        if len(respuesta) == 0:
            return {
                'valida': False,
                'mensaje_error': 'este campo no puede estar vacío'
            }
        
        if len(respuesta) < 2:
            return {
                'valida': False,
                'mensaje_error': 'ingresa al menos 2 caracteres'
            }
        
        if len(respuesta) > 500:
            return {
                'valida': False,
                'mensaje_error': 'el texto no puede exceder 500 caracteres'
            }
        
        # Limpiar texto
        texto_limpio = self._limpiar_texto(respuesta)
        
        return {
            'valida': True,
            'valor_procesado': texto_limpio
        }
    
    def _validar_texto_opcional(self, respuesta: str) -> Dict[str, Any]:
        """
        Valida texto opcional (puede estar vacío o ser "No")
        """
        if respuesta.lower() in ['no', 'n', 'ninguno', 'ninguna', 'nada', '']:
            return {
                'valida': True,
                'valor_procesado': ''
            }
        
        if len(respuesta) > 500:
            return {
                'valida': False,
                'mensaje_error': 'el texto no puede exceder 500 caracteres'
            }
        
        # Limpiar texto
        texto_limpio = self._limpiar_texto(respuesta)
        
        return {
            'valida': True,
            'valor_procesado': texto_limpio
        }
    
    def _validar_lista_nombres(self, respuesta: str) -> Dict[str, Any]:
        """
        Valida lista de nombres separados por comas
        """
        if len(respuesta) == 0:
            return {
                'valida': False,
                'mensaje_error': 'debes ingresar al menos un nombre'
            }
        
        # Separar por comas, punto y coma, o saltos de línea
        separadores = [',', ';', '\n']
        nombres = [respuesta]  # Empezar con la respuesta completa
        
        for sep in separadores:
            nombres_temp = []
            for nombre in nombres:
                nombres_temp.extend([n.strip() for n in nombre.split(sep)])
            nombres = nombres_temp
        
        # Filtrar nombres vacíos y validar
        nombres_validos = []
        for nombre in nombres:
            nombre = nombre.strip()
            if len(nombre) > 0:
                # Validar que el nombre tenga al menos 2 caracteres
                if len(nombre) < 2:
                    return {
                        'valida': False,
                        'mensaje_error': f'el nombre "{nombre}" es demasiado corto (mínimo 2 caracteres)'
                    }
                
                # Validar que no sea demasiado largo
                if len(nombre) > 100:
                    return {
                        'valida': False,
                        'mensaje_error': f'el nombre "{nombre[:20]}..." es demasiado largo (máximo 100 caracteres)'
                    }
                
                # Validar caracteres básicos (letras, espacios, acentos, guiones)
                if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-\.]+$', nombre):
                    return {
                        'valida': False,
                        'mensaje_error': f'el nombre "{nombre}" contiene caracteres no válidos'
                    }
                
                nombres_validos.append(self._limpiar_texto(nombre))
        
        if len(nombres_validos) == 0:
            return {
                'valida': False,
                'mensaje_error': 'debes ingresar al menos un nombre válido'
            }
        
        if len(nombres_validos) > 50:
            return {
                'valida': False,
                'mensaje_error': 'no puedes ingresar más de 50 nombres'
            }
        
        return {
            'valida': True,
            'valor_procesado': nombres_validos
        }
    
    def _limpiar_texto(self, texto: str) -> str:
        """
        Limpia y normaliza texto
        """
        # Eliminar espacios extra
        texto = ' '.join(texto.split())
        
        # Capitalizar primera letra de cada palabra para nombres
        if self._es_probable_nombre(texto):
            texto = texto.title()
        
        return texto
    
    def _es_probable_nombre(self, texto: str) -> bool:
        """
        Determina si un texto es probablemente un nombre
        """
        # Si tiene menos de 50 caracteres y no tiene números, probablemente es un nombre
        return len(texto) < 50 and not any(char.isdigit() for char in texto)
    
    def validar_horario_coherente(self, hora_inicio: str, hora_fin: str) -> Dict[str, Any]:
        """
        Valida que el horario de fin sea posterior al de inicio
        """
        validacion_inicio = self._validar_hora(hora_inicio)
        validacion_fin = self._validar_hora(hora_fin)
        
        if not validacion_inicio['valida']:
            return {
                'valida': False,
                'mensaje_error': f'Hora de inicio inválida: {validacion_inicio["mensaje_error"]}'
            }
        
        if not validacion_fin['valida']:
            return {
                'valida': False,
                'mensaje_error': f'Hora de fin inválida: {validacion_fin["mensaje_error"]}'
            }
        
        inicio = validacion_inicio['valor_procesado']
        fin = validacion_fin['valor_procesado']
        
        # Convertir a minutos para comparar
        minutos_inicio = inicio.hour * 60 + inicio.minute
        minutos_fin = fin.hour * 60 + fin.minute
        
        if minutos_fin <= minutos_inicio:
            return {
                'valida': False,
                'mensaje_error': 'la hora de término debe ser posterior a la hora de inicio'
            }
        
        # Verificar que la duración sea razonable (máximo 12 horas)
        duracion_minutos = minutos_fin - minutos_inicio
        if duracion_minutos > 12 * 60:
            return {
                'valida': False,
                'mensaje_error': 'la duración de la reunión no puede exceder 12 horas'
            }
        
        # Verificar duración mínima (al menos 5 minutos)
        if duracion_minutos < 5:
            return {
                'valida': False,
                'mensaje_error': 'la reunión debe durar al menos 5 minutos'
            }
        
        return {
            'valida': True,
            'hora_inicio': inicio,
            'hora_fin': fin,
            'duracion_minutos': duracion_minutos
        }