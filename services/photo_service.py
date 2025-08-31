# -*- coding: utf-8 -*-
"""
Servicio de gestión de fotografías para SIRIJ BOT
"""

import os
import logging
from datetime import datetime
from typing import Optional, Tuple
from PIL import Image
import hashlib

logger = logging.getLogger(__name__)

class PhotoService:
    """Servicio para manejar la subida y procesamiento de fotografías"""
    
    def __init__(self, storage_path: str, max_size_mb: int = 10):
        self.storage_path = storage_path
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.allowed_formats = {'JPEG', 'PNG', 'WEBP'}
        
        # Crear directorio de almacenamiento si no existe
        os.makedirs(storage_path, exist_ok=True)
    
    def save_photo(self, file_path: str, user_id: str, reunion_id: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
        """
        Guarda una fotografía en el sistema de archivos
        
        Args:
            file_path: Ruta temporal del archivo descargado
            user_id: ID del usuario que subió la foto
            reunion_id: ID de la reunión (opcional)
            
        Returns:
            Tuple[bool, str, Optional[str]]: (éxito, mensaje, ruta_guardada)
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(file_path):
                return False, "El archivo no existe", None
            
            # Verificar tamaño del archivo
            file_size = os.path.getsize(file_path)
            if file_size > self.max_size_bytes:
                return False, f"El archivo es muy grande. Máximo {self.max_size_bytes // (1024*1024)}MB", None
            
            # Verificar y procesar la imagen
            try:
                with Image.open(file_path) as img:
                    # Verificar formato
                    if img.format not in self.allowed_formats:
                        return False, f"Formato no permitido. Use: {', '.join(self.allowed_formats)}", None
                    
                    # Generar nombre único para el archivo
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_hash = self._generate_file_hash(file_path)
                    extension = img.format.lower()
                    if extension == 'jpeg':
                        extension = 'jpg'
                    
                    filename = f"{user_id}_{timestamp}_{file_hash[:8]}.{extension}"
                    
                    # Crear subdirectorio por fecha si no existe
                    date_folder = datetime.now().strftime("%Y-%m")
                    save_dir = os.path.join(self.storage_path, date_folder)
                    os.makedirs(save_dir, exist_ok=True)
                    
                    save_path = os.path.join(save_dir, filename)
                    
                    # Optimizar y guardar la imagen
                    optimized_img = self._optimize_image(img)
                    optimized_img.save(save_path, format=img.format, optimize=True, quality=85)
                    
                    logger.info(f"Foto guardada exitosamente: {save_path}")
                    return True, "Foto guardada exitosamente", save_path
                    
            except Exception as e:
                logger.error(f"Error procesando imagen: {e}")
                return False, "Error procesando la imagen. Verifique que sea un archivo válido", None
                
        except Exception as e:
            logger.error(f"Error guardando foto: {e}")
            return False, f"Error guardando la foto: {str(e)}", None
    
    def _generate_file_hash(self, file_path: str) -> str:
        """
        Genera un hash único para el archivo
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            str: Hash MD5 del archivo
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _optimize_image(self, img: Image.Image) -> Image.Image:
        """
        Optimiza la imagen para reducir el tamaño
        
        Args:
            img: Imagen PIL
            
        Returns:
            Image.Image: Imagen optimizada
        """
        # Redimensionar si es muy grande
        max_dimension = 1920
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convertir a RGB si es necesario (para JPEG)
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        return img
    
    def delete_photo(self, photo_path: str) -> bool:
        """
        Elimina una fotografía del sistema de archivos
        
        Args:
            photo_path: Ruta de la foto a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            if os.path.exists(photo_path):
                os.remove(photo_path)
                logger.info(f"Foto eliminada: {photo_path}")
                return True
            else:
                logger.warning(f"Foto no encontrada para eliminar: {photo_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error eliminando foto {photo_path}: {e}")
            return False
    
    def get_photo_info(self, photo_path: str) -> Optional[dict]:
        """
        Obtiene información de una fotografía
        
        Args:
            photo_path: Ruta de la foto
            
        Returns:
            dict: Información de la foto o None si no existe
        """
        try:
            if not os.path.exists(photo_path):
                return None
            
            file_size = os.path.getsize(photo_path)
            file_stat = os.stat(photo_path)
            
            with Image.open(photo_path) as img:
                return {
                    'path': photo_path,
                    'size_bytes': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2),
                    'dimensions': img.size,
                    'format': img.format,
                    'mode': img.mode,
                    'created_at': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    'modified_at': datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error obteniendo información de foto {photo_path}: {e}")
            return None
    
    def validate_photo_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Valida un archivo de foto antes de procesarlo
        
        Args:
            file_path: Ruta del archivo a validar
            
        Returns:
            Tuple[bool, str]: (es_válido, mensaje)
        """
        try:
            # Verificar existencia
            if not os.path.exists(file_path):
                return False, "El archivo no existe"
            
            # Verificar tamaño
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return False, "El archivo está vacío"
            
            if file_size > self.max_size_bytes:
                max_mb = self.max_size_bytes // (1024 * 1024)
                return False, f"El archivo es muy grande. Máximo {max_mb}MB"
            
            # Verificar que es una imagen válida
            try:
                with Image.open(file_path) as img:
                    if img.format not in self.allowed_formats:
                        return False, f"Formato no permitido. Use: {', '.join(self.allowed_formats)}"
                    
                    # Verificar dimensiones mínimas
                    if min(img.size) < 100:
                        return False, "La imagen es muy pequeña. Mínimo 100px en cada dimensión"
                    
                    return True, "Archivo válido"
                    
            except Exception:
                return False, "El archivo no es una imagen válida"
                
        except Exception as e:
            return False, f"Error validando archivo: {str(e)}"
    
    def cleanup_old_photos(self, days_old: int = 30) -> int:
        """
        Limpia fotos antiguas del sistema
        
        Args:
            days_old: Días de antigüedad para considerar una foto como antigua
            
        Returns:
            int: Número de fotos eliminadas
        """
        deleted_count = 0
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        
        try:
            for root, dirs, files in os.walk(self.storage_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.getmtime(file_path) < cutoff_time:
                            os.remove(file_path)
                            deleted_count += 1
                            logger.info(f"Foto antigua eliminada: {file_path}")
                    except Exception as e:
                        logger.error(f"Error eliminando foto antigua {file_path}: {e}")
            
            logger.info(f"Limpieza completada. {deleted_count} fotos eliminadas")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error en limpieza de fotos: {e}")
            return deleted_count