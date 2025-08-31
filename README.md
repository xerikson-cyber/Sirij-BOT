# SIRIJ BOT 🤖

**Bot de Telegram para digitalizar Reuniones de Inicio de Jornada - CFE**

## 📋 Descripción

SIRIJ BOT es un chatbot de Telegram diseñado para digitalizar el proceso de llenado del formulario "Reunión de Inicio de Jornada" de la Comisión Federal de Electricidad (CFE). El bot guía a los supervisores de campo a través de todas las preguntas del formulario, almacena las respuestas en una base de datos y gestiona la evidencia fotográfica de las reuniones.

## ✨ Características Principales

- **Flujo de conversación guiado**: El bot hace las preguntas en el mismo orden que aparecen en el formulario oficial
- **Captura de datos diversos**: Maneja texto libre, fechas, horas, respuestas Sí/No y listas de nombres
- **Almacenamiento estructurado**: Todas las respuestas se guardan en una base de datos SQL
- **Gestión de evidencia fotográfica**: Permite subir y almacenar múltiples fotografías como evidencia
- **Validación de datos**: Verifica formatos y coherencia de las respuestas
- **Sesiones temporales**: Maneja sesiones de usuario con timeout automático
- **Exportación de datos**: Permite exportar reuniones a formato CSV

## 🏗️ Arquitectura del Proyecto

```
SIRIJ BOT/
├── app.py                 # Aplicación principal
├── config.py              # Configuración centralizada
├── requirements.txt       # Dependencias de Python
├── .env.example          # Plantilla de variables de entorno
├── README.md             # Documentación del proyecto
├── SIRIJ_BOT_Design.md   # Documento de diseño técnico
├── bot/                  # Módulo del chatbot
│   ├── __init__.py
│   ├── handlers.py       # Manejadores de comandos y mensajes
│   ├── conversation.py   # Lógica de conversación
│   └── validators.py     # Validadores de respuestas
├── database/             # Módulo de base de datos
│   ├── __init__.py
│   └── models.py         # Modelos y operaciones de BD
└── services/             # Servicios de negocio
    ├── __init__.py
    ├── session_service.py    # Gestión de sesiones
    ├── photo_service.py      # Gestión de fotografías
    └── meeting_service.py    # Gestión de reuniones
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- Bot de Telegram (token obtenido de @BotFather)
- SQLite (incluido) o PostgreSQL (opcional)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd "SIRIJ BOT"
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```
   
   Editar `.env` con tus configuraciones:
   ```env
   TELEGRAM_BOT_TOKEN=tu_token_de_telegram_aqui
   DATABASE_URL=sqlite:///sirij_bot.db
   PHOTO_STORAGE_PATH=./photos
   PHOTO_MAX_SIZE_MB=10
   SESSION_TIMEOUT_MINUTES=60
   DEBUG=False
   LOG_LEVEL=INFO
   ```

5. **Ejecutar el bot**
   ```bash
   python app.py
   ```

## 🎯 Uso del Bot

### Comandos Disponibles

- `/start` - Iniciar nueva reunión
- `/help` - Mostrar ayuda
- `/cancel` - Cancelar reunión actual
- `/status` - Ver estado actual

### Flujo de Uso

1. **Iniciar conversación**: Envía `/start` al bot
2. **Responder preguntas**: El bot te guiará a través de todas las preguntas del formulario
3. **Subir fotografías**: Cuando se solicite, envía las fotos de evidencia
4. **Confirmar datos**: Revisa y confirma la información antes de guardar
5. **Completar**: El bot guardará la reunión y proporcionará un resumen

### Tipos de Respuesta

- **Texto libre**: Para departamento, nombres, observaciones
- **Fechas**: Formato YYYY-MM-DD (ej: 2024-01-15)
- **Horas**: Formato HH:MM (ej: 08:30)
- **Sí/No**: Para preguntas de verificación
- **Fotografías**: Imágenes JPG, PNG o WEBP (máximo 10MB)

## 📊 Base de Datos

### Tabla Principal: `reuniones_inicio_jornada`

Almacena toda la información de las reuniones:

- **Datos generales**: departamento, fecha, categoría, personal, horarios
- **Sección Inicio**: 5 preguntas de verificación (Sí/No)
- **Sección Información**: 4 preguntas sobre trabajos y operaciones
- **Sección Seguridad**: 6 preguntas sobre actividades de seguridad
- **Meta/Observaciones**: información adicional y observaciones
- **Evidencia**: rutas de fotos y metadatos

### Tabla de Sesiones: `sesiones_temporales`

Maneja las sesiones activas de los usuarios:

- Estado de la conversación
- Respuestas temporales
- Fotografías subidas
- Timeout automático

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | *(requerido)* |
| `DATABASE_URL` | URL de conexión a la base de datos | `sqlite:///sirij_bot.db` |
| `PHOTO_STORAGE_PATH` | Directorio para almacenar fotos | `./photos` |
| `PHOTO_MAX_SIZE_MB` | Tamaño máximo de foto en MB | `10` |
| `SESSION_TIMEOUT_MINUTES` | Timeout de sesión en minutos | `60` |
| `DEBUG` | Modo debug (true/false) | `False` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |
| `LOG_FILE` | Archivo de logs | `sirij_bot.log` |

### Base de Datos PostgreSQL

Para usar PostgreSQL en lugar de SQLite:

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/sirij_bot
```

### Configuración de Logging

El sistema de logging está configurado para escribir tanto en consola como en archivo. Los niveles disponibles son: DEBUG, INFO, WARNING, ERROR, CRITICAL.

## 📈 Funcionalidades Adicionales

### Exportación de Datos

El sistema permite exportar reuniones a formato CSV para análisis:

```python
from services.meeting_service import MeetingService

meeting_service = MeetingService()
meeting_service.export_meetings('reuniones_2024.csv', '2024-01-01', '2024-12-31')
```

### Estadísticas

Obtener estadísticas generales de las reuniones:

```python
stats = meeting_service.get_statistics()
print(f"Total reuniones: {stats['total_meetings']}")
```

### Limpieza Automática

El sistema incluye funciones para limpiar:

- Sesiones expiradas
- Fotografías antiguas
- Logs antiguos

## 🛠️ Desarrollo y Personalización

### Agregar Nuevas Preguntas

1. Modificar la lista `QUESTIONS` en `bot/conversation.py`
2. Actualizar el esquema de base de datos en `database/models.py`
3. Ajustar los validadores en `bot/validators.py`

### Personalizar Mensajes

Todos los mensajes del bot están centralizados en `config.py` en la sección `MESSAGES`.

### Agregar Nuevos Comandos

1. Definir el handler en `bot/handlers.py`
2. Registrar el comando en `app.py`

## 🔒 Seguridad

- **Variables de entorno**: Nunca hardcodear tokens o credenciales
- **Validación de entrada**: Todas las entradas de usuario son validadas
- **Sanitización de archivos**: Las imágenes son procesadas y optimizadas
- **Timeouts de sesión**: Las sesiones expiran automáticamente
- **Logging seguro**: No se registran datos sensibles

## 📝 Logging y Monitoreo

El bot registra:

- Inicio y fin de reuniones
- Errores y excepciones
- Subida de fotografías
- Operaciones de base de datos
- Estadísticas de uso

## 🐛 Solución de Problemas

### Problemas Comunes

1. **Bot no responde**
   - Verificar token de Telegram
   - Revisar conexión a internet
   - Comprobar logs de error

2. **Error de base de datos**
   - Verificar permisos de escritura
   - Comprobar espacio en disco
   - Revisar URL de conexión

3. **Fotos no se guardan**
   - Verificar permisos del directorio
   - Comprobar espacio disponible
   - Revisar tamaño máximo configurado

### Logs de Debug

Para activar logs detallados:

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios con tests
4. Enviar pull request

## 📄 Licencia

Este proyecto está desarrollado para uso interno de CFE. Todos los derechos reservados.

## 📞 Soporte

Para soporte técnico o preguntas sobre el bot, contactar al equipo de desarrollo.

---

**SIRIJ BOT v1.0.0** - Desarrollado para CFE  
*Digitalizando las Reuniones de Inicio de Jornada* 🚀