# -*- coding: utf-8 -*-
"""
Modelos de base de datos para SIRIJ BOT
Define las tablas y operaciones de base de datos
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

# Ruta de la base de datos
DB_PATH = os.getenv('DATABASE_URL', 'sqlite:///sirij_bot.db').replace('sqlite:///', '')

def get_db_connection():
    """
    Obtiene una conexión a la base de datos
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
    return conn

def create_tables():
    """
    Crea las tablas necesarias en la base de datos
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tabla principal de reuniones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reuniones_inicio_jornada (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                
                -- Datos Generales
                departamento VARCHAR(255) NOT NULL,
                fecha DATE NOT NULL,
                categoria_maxima VARCHAR(255),
                nombre_supervisor VARCHAR(255) NOT NULL,
                nombres_personal TEXT, -- JSON array de nombres
                hora_inicio TIME NOT NULL,
                hora_termino TIME NOT NULL,
                
                -- Sección Inicio (S/N)
                saludo_inicio_jornada BOOLEAN,
                enumero_personal BOOLEAN,
                pregunto_estado_salud BOOLEAN,
                realizo_ejercicios BOOLEAN,
                detecto_anomalias_salud BOOLEAN,
                tomo_lista_asistencia BOOLEAN,
                
                -- Sección Información (S/N)
                comento_trabajos_mantenimiento BOOLEAN,
                comento_trabajos_operacion BOOLEAN,
                comento_trabajos_alto_riesgo BOOLEAN,
                comento_incidentes_accidentes BOOLEAN,
                otra_informacion TEXT,
                
                -- Sección Actividades de Seguridad (S/N)
                realizo_revision_espejo BOOLEAN,
                realizo_prediccion_peligro BOOLEAN,
                dio_lectura_reglamento BOOLEAN,
                realizo_exposicion_sentir_peligro BOOLEAN,
                actividades_posteriores BOOLEAN,
                descripcion_actividades_seguridad TEXT,
                
                -- Meta y Observaciones
                meta_proposito_jornada TEXT,
                observaciones TEXT,
                
                -- Evidencia y Metadatos
                ruta_evidencia_fotografica VARCHAR(500),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_telegram_id INTEGER
            )
        ''')
        
        # Tabla de sesiones temporales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sesiones_temporales (
                id VARCHAR(50) PRIMARY KEY,
                usuario_telegram_id INTEGER NOT NULL,
                estado VARCHAR(50) NOT NULL,
                pregunta_actual VARCHAR(100),
                datos_sesion TEXT, -- JSON con las respuestas
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear índices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_fecha ON reuniones_inicio_jornada(fecha)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_departamento ON reuniones_inicio_jornada(departamento)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_supervisor ON reuniones_inicio_jornada(nombre_supervisor)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_fecha_registro ON reuniones_inicio_jornada(fecha_registro)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuario_telegram ON reuniones_inicio_jornada(usuario_telegram_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sesion_usuario ON sesiones_temporales(usuario_telegram_id)')
        
        conn.commit()
        logger.info("Tablas de base de datos creadas/verificadas correctamente")

def guardar_reunion_completa(datos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Guarda una reunión completa en la base de datos
    
    Args:
        datos: Diccionario con todos los datos de la reunión
        
    Returns:
        Dict con 'exito', 'reunion_id' o 'error'
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Preparar datos para inserción
            datos_db = {
                'departamento': datos.get('departamento'),
                'fecha': datos.get('fecha'),
                'categoria_maxima': datos.get('categoria_maxima'),
                'nombre_supervisor': datos.get('nombre_supervisor'),
                'nombres_personal': json.dumps(datos.get('nombres_personal', [])),
                'hora_inicio': datos.get('hora_inicio'),
                'hora_termino': datos.get('hora_termino'),
                
                # Sección Inicio
                'saludo_inicio_jornada': datos.get('saludo_inicio_jornada'),
                'enumero_personal': datos.get('enumero_personal'),
                'pregunto_estado_salud': datos.get('pregunto_estado_salud'),
                'realizo_ejercicios': datos.get('realizo_ejercicios'),
                'detecto_anomalias_salud': datos.get('detecto_anomalias_salud'),
                'tomo_lista_asistencia': datos.get('tomo_lista_asistencia'),
                
                # Sección Información
                'comento_trabajos_mantenimiento': datos.get('comento_trabajos_mantenimiento'),
                'comento_trabajos_operacion': datos.get('comento_trabajos_operacion'),
                'comento_trabajos_alto_riesgo': datos.get('comento_trabajos_alto_riesgo'),
                'comento_incidentes_accidentes': datos.get('comento_incidentes_accidentes'),
                'otra_informacion': datos.get('otra_informacion', ''),
                
                # Sección Actividades de Seguridad
                'realizo_revision_espejo': datos.get('realizo_revision_espejo'),
                'realizo_prediccion_peligro': datos.get('realizo_prediccion_peligro'),
                'dio_lectura_reglamento': datos.get('dio_lectura_reglamento'),
                'realizo_exposicion_sentir_peligro': datos.get('realizo_exposicion_sentir_peligro'),
                'actividades_posteriores': datos.get('actividades_posteriores'),
                'descripcion_actividades_seguridad': datos.get('descripcion_actividades_seguridad'),
                
                # Meta y Observaciones
                'meta_proposito_jornada': datos.get('meta_proposito_jornada'),
                'observaciones': datos.get('observaciones', ''),
                
                # Evidencia
                'ruta_evidencia_fotografica': datos.get('ruta_evidencia_fotografica'),
                'usuario_telegram_id': datos.get('usuario_telegram_id')
            }
            
            # Validar campos requeridos
            campos_requeridos = [
                'departamento', 'fecha', 'nombre_supervisor', 'hora_inicio', 'hora_termino'
            ]
            
            for campo in campos_requeridos:
                if not datos_db.get(campo):
                    return {
                        'exito': False,
                        'error': f'Campo requerido faltante: {campo}'
                    }
            
            # Construir query de inserción
            columnas = list(datos_db.keys())
            placeholders = ', '.join(['?' for _ in columnas])
            columnas_str = ', '.join(columnas)
            
            query = f"INSERT INTO reuniones_inicio_jornada ({columnas_str}) VALUES ({placeholders})"
            
            cursor.execute(query, list(datos_db.values()))
            reunion_id = cursor.lastrowid
            
            conn.commit()
            
            logger.info(f"Reunión guardada exitosamente con ID: {reunion_id}")
            
            return {
                'exito': True,
                'reunion_id': reunion_id
            }
            
    except Exception as e:
        logger.error(f"Error guardando reunión: {e}")
        return {
            'exito': False,
            'error': str(e)
        }

def obtener_reunion_por_id(reunion_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene una reunión por su ID
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM reuniones_inicio_jornada WHERE id = ?",
                (reunion_id,)
            )
            
            row = cursor.fetchone()
            
            if row:
                reunion = dict(row)
                # Deserializar JSON
                if reunion['nombres_personal']:
                    reunion['nombres_personal'] = json.loads(reunion['nombres_personal'])
                return reunion
            
            return None
            
    except Exception as e:
        logger.error(f"Error obteniendo reunión {reunion_id}: {e}")
        return None

def obtener_reuniones_por_usuario(usuario_id: int, limite: int = 10) -> List[Dict[str, Any]]:
    """
    Obtiene las últimas reuniones de un usuario
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT id, departamento, fecha, nombre_supervisor, fecha_registro
                FROM reuniones_inicio_jornada 
                WHERE usuario_telegram_id = ?
                ORDER BY fecha_registro DESC
                LIMIT ?
                """,
                (usuario_id, limite)
            )
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
    except Exception as e:
        logger.error(f"Error obteniendo reuniones de usuario {usuario_id}: {e}")
        return []

def obtener_estadisticas_reuniones(fecha_inicio: str = None, fecha_fin: str = None) -> Dict[str, Any]:
    """
    Obtiene estadísticas de las reuniones
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Query base
            where_clause = ""
            params = []
            
            if fecha_inicio and fecha_fin:
                where_clause = "WHERE fecha BETWEEN ? AND ?"
                params = [fecha_inicio, fecha_fin]
            elif fecha_inicio:
                where_clause = "WHERE fecha >= ?"
                params = [fecha_inicio]
            elif fecha_fin:
                where_clause = "WHERE fecha <= ?"
                params = [fecha_fin]
            
            # Total de reuniones
            cursor.execute(f"SELECT COUNT(*) FROM reuniones_inicio_jornada {where_clause}", params)
            total_reuniones = cursor.fetchone()[0]
            
            # Reuniones por departamento
            cursor.execute(
                f"""
                SELECT departamento, COUNT(*) as cantidad
                FROM reuniones_inicio_jornada {where_clause}
                GROUP BY departamento
                ORDER BY cantidad DESC
                """,
                params
            )
            por_departamento = [dict(row) for row in cursor.fetchall()]
            
            # Reuniones por fecha
            cursor.execute(
                f"""
                SELECT fecha, COUNT(*) as cantidad
                FROM reuniones_inicio_jornada {where_clause}
                GROUP BY fecha
                ORDER BY fecha DESC
                LIMIT 30
                """,
                params
            )
            por_fecha = [dict(row) for row in cursor.fetchall()]
            
            return {
                'total_reuniones': total_reuniones,
                'por_departamento': por_departamento,
                'por_fecha': por_fecha
            }
            
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return {
            'total_reuniones': 0,
            'por_departamento': [],
            'por_fecha': []
        }

def limpiar_sesiones_expiradas(horas_expiracion: int = 24):
    """
    Limpia sesiones temporales expiradas
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                """
                DELETE FROM sesiones_temporales 
                WHERE datetime(fecha_actualizacion) < datetime('now', '-{} hours')
                """.format(horas_expiracion)
            )
            
            eliminadas = cursor.rowcount
            conn.commit()
            
            if eliminadas > 0:
                logger.info(f"Eliminadas {eliminadas} sesiones expiradas")
                
    except Exception as e:
        logger.error(f"Error limpiando sesiones expiradas: {e}")

def exportar_reuniones_csv(archivo_salida: str, fecha_inicio: str = None, fecha_fin: str = None) -> bool:
    """
    Exporta reuniones a archivo CSV
    """
    try:
        import csv
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Query con filtros de fecha
            where_clause = ""
            params = []
            
            if fecha_inicio and fecha_fin:
                where_clause = "WHERE fecha BETWEEN ? AND ?"
                params = [fecha_inicio, fecha_fin]
            
            cursor.execute(f"SELECT * FROM reuniones_inicio_jornada {where_clause} ORDER BY fecha_registro", params)
            
            rows = cursor.fetchall()
            
            if not rows:
                return False
            
            # Escribir CSV
            with open(archivo_salida, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir encabezados
                writer.writerow([description[0] for description in cursor.description])
                
                # Escribir datos
                for row in rows:
                    writer.writerow(row)
            
            logger.info(f"Exportadas {len(rows)} reuniones a {archivo_salida}")
            return True
            
    except Exception as e:
        logger.error(f"Error exportando a CSV: {e}")
        return False