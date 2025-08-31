# SIRIJ BOT - Diseño Técnico Completo
## Chatbot para Digitalización del Formulario "Reunión de Inicio de Jornada" CFE

---

## 1. ANÁLISIS DEL FORMULARIO

### Estructura del Formulario "Reunión de Inicio de Jornada"

El formulario está dividido en las siguientes secciones:

#### **Datos Generales**
- Departamento (texto libre)
- Fecha (formato fecha)
- Categoría máxima representada en la reunión (texto libre)
- Nombre del supervisor (texto libre)
- Nombre del personal (lista de nombres)
- Hora de inicio (formato hora)
- Hora de término (formato hora)

#### **Sección: Inicio**
1. ¿Se realizó el saludo de inicio de jornada? (S/N)
2. ¿Se enumeró al personal participante? (S/N)
3. ¿Se preguntó el estado de salud de los participantes? (S/N)
4. ¿Se realizaron los ejercicios? (S/N)
4.1. ¿Se detectaron anomalías en el estado de salud? (S/N)
5. ¿Se tomó lista de asistencia? (S/N)

#### **Sección: Información**
5.1. ¿Se comentaron trabajos de mantenimiento relevantes? (S/N)
5.2. ¿Se comentaron trabajos de operación relevantes? (S/N)
5.3. ¿Se comentaron trabajos con potencial de alto riesgo? (S/N)
5.4. ¿Se comentaron incidentes o accidentes ocurridos? (S/N)
5.5. Otra información (texto libre - especificar temas)

#### **Sección: Actividades de Seguridad**
6.1. ¿Se realizó la revisión espejo? (S/N)
6.2. ¿Se realizó actividad de predicción de peligro (APP)? (S/N)
6.3. ¿Se dio lectura al un artículo del reglamento de seguridad e higiene? (S/N)
6.4. ¿Se realizó una exposición de sentir el peligro (justo)? (S/N)
6.5. ¿Actividades relevantes posteriores (inspecciones, campañas etc.)? (S/N)
6.6. Actividad (especificar actividades de seguridad realizadas) (texto libre)

#### **Sección: Meta/Propósito**
- Meta o propósito de la jornada (texto libre)

#### **Sección: Observaciones**
- Observaciones (texto libre)

---

## 2. DISEÑO DEL FLUJO DE CONVERSACIÓN

### Flujo Completo del Diálogo SIRIJ BOT

```
🤖 SIRIJ BOT: ¡Hola! Soy SIRIJ BOT, tu asistente para las Reuniones de Inicio de Jornada de CFE. 
¿Estás listo para comenzar con el registro de hoy?

👤 USUARIO: Sí

🤖 SIRIJ BOT: Perfecto. Comenzaremos con los datos generales.
¿Cuál es el nombre del Departamento?

👤 USUARIO: [Respuesta del departamento]

🤖 SIRIJ BOT: Gracias. ¿Cuál es la fecha de hoy? (formato: DD/MM/AAAA)

👤 USUARIO: [Fecha]

🤖 SIRIJ BOT: ¿Cuál es la categoría máxima representada en la reunión?

👤 USUARIO: [Categoría]

🤖 SIRIJ BOT: ¿Cuál es tu nombre como supervisor?

👤 USUARIO: [Nombre supervisor]

🤖 SIRIJ BOT: Ahora necesito los nombres del personal que participó en la reunión. 
Puedes escribir los nombres separados por comas, o escribir "fin" cuando termines de agregar nombres.

👤 USUARIO: [Lista de nombres o nombres individuales]

🤖 SIRIJ BOT: ¿A qué hora inició la reunión? (formato: HH:MM)

👤 USUARIO: [Hora inicio]

🤖 SIRIJ BOT: ¿A qué hora terminó la reunión? (formato: HH:MM)

👤 USUARIO: [Hora término]

🤖 SIRIJ BOT: Excelente. Ahora pasaremos a la sección de INICIO.
¿Se realizó el saludo de inicio de jornada? (Responde: Sí o No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se enumeró al personal participante? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se preguntó el estado de salud de los participantes? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se realizaron los ejercicios? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se detectaron anomalías en el estado de salud? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se tomó lista de asistencia? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: Ahora la sección de INFORMACIÓN.
¿Se comentaron trabajos de mantenimiento relevantes? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se comentaron trabajos de operación relevantes? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se comentaron trabajos con potencial de alto riesgo? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se comentaron incidentes o accidentes ocurridos? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Hay otra información relevante que quieras agregar? 
Si es así, especifica los temas tratados. Si no, escribe "No".

👤 USUARIO: [Información adicional o "No"]

🤖 SIRIJ BOT: Continuamos con ACTIVIDADES DE SEGURIDAD.
¿Se realizó la revisión espejo? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se realizó actividad de predicción de peligro (APP)? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se dio lectura a un artículo del reglamento de seguridad e higiene? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se realizó una exposición de sentir el peligro (justo)? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: ¿Se realizaron actividades relevantes posteriores (inspecciones, campañas, etc.)? (Sí/No)

👤 USUARIO: [Sí/No]

🤖 SIRIJ BOT: Especifica las actividades de seguridad que se realizaron:

👤 USUARIO: [Descripción de actividades]

🤖 SIRIJ BOT: ¿Cuál es la meta o propósito de la jornada?

👤 USUARIO: [Meta/propósito]

🤖 SIRIJ BOT: ¿Tienes alguna observación adicional? Si no, escribe "No".

👤 USUARIO: [Observaciones o "No"]

🤖 SIRIJ BOT: Perfecto. Para finalizar, necesito que subas una fotografía como evidencia de la reunión.
Por favor, envía la imagen.

👤 USUARIO: [Envía foto]

🤖 SIRIJ BOT: ¡Excelente! He registrado toda la información de la Reunión de Inicio de Jornada.

📋 **RESUMEN:**
- Departamento: [departamento]
- Fecha: [fecha]
- Supervisor: [nombre]
- Personal: [lista]
- Hora: [inicio] - [fin]
- Evidencia fotográfica: ✅ Guardada

¿Confirmas que toda la información es correcta? (Sí/No)

👤 USUARIO: Sí

🤖 SIRIJ BOT: ¡Perfecto! La reunión ha sido registrada exitosamente en el sistema.
ID de registro: [ID_GENERADO]

¡Gracias por usar SIRIJ BOT! 🚀
```

---

## 3. ESQUEMA DE BASE DE DATOS

### Tabla Principal: `reuniones_inicio_jornada`

```sql
CREATE TABLE reuniones_inicio_jornada (
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
    usuario_registro VARCHAR(255)
);
```

### Índices Recomendados

```sql
CREATE INDEX idx_fecha ON reuniones_inicio_jornada(fecha);
CREATE INDEX idx_departamento ON reuniones_inicio_jornada(departamento);
CREATE INDEX idx_supervisor ON reuniones_inicio_jornada(nombre_supervisor);
CREATE INDEX idx_fecha_registro ON reuniones_inicio_jornada(fecha_registro);
```

---

## 4. LÓGICA DE FUNCIONES CLAVE

### 4.1 Función `iniciar_reunion()`

```python
def iniciar_reunion(user_id):
    """
    Inicia una nueva sesión de reunión para el usuario
    """
    # Verificar si el usuario tiene una reunión en progreso
    sesion_activa = verificar_sesion_activa(user_id)
    
    if sesion_activa:
        return {
            'mensaje': '¿Quieres continuar con la reunión en progreso o iniciar una nueva?',
            'opciones': ['Continuar', 'Nueva reunión'],
            'estado': 'sesion_existente'
        }
    
    # Crear nueva sesión
    nueva_sesion = crear_sesion_reunion(user_id)
    
    return {
        'mensaje': '¡Hola! Soy SIRIJ BOT, tu asistente para las Reuniones de Inicio de Jornada de CFE. ¿Estás listo para comenzar con el registro de hoy?',
        'sesion_id': nueva_sesion['id'],
        'estado': 'esperando_confirmacion',
        'siguiente_paso': 'datos_generales'
    }
```

### 4.2 Función `hacer_pregunta(pregunta, tipo_respuesta)`

```python
def hacer_pregunta(sesion_id, pregunta_id, respuesta_usuario):
    """
    Procesa la respuesta del usuario y determina la siguiente pregunta
    """
    # Obtener configuración de la pregunta
    config_pregunta = obtener_config_pregunta(pregunta_id)
    
    # Validar respuesta según el tipo
    validacion = validar_respuesta(
        respuesta_usuario, 
        config_pregunta['tipo']
    )
    
    if not validacion['valida']:
        return {
            'mensaje': f"Por favor, {validacion['mensaje_error']}",
            'repetir_pregunta': True,
            'pregunta_actual': pregunta_id
        }
    
    # Guardar respuesta en sesión temporal
    guardar_respuesta_temporal(sesion_id, pregunta_id, validacion['valor_procesado'])
    
    # Determinar siguiente pregunta
    siguiente_pregunta = obtener_siguiente_pregunta(pregunta_id)
    
    if siguiente_pregunta:
        return {
            'mensaje': siguiente_pregunta['texto'],
            'pregunta_id': siguiente_pregunta['id'],
            'tipo_respuesta': siguiente_pregunta['tipo'],
            'estado': 'esperando_respuesta'
        }
    else:
        # Todas las preguntas completadas
        return {
            'mensaje': 'Perfecto. Para finalizar, necesito que subas una fotografía como evidencia de la reunión. Por favor, envía la imagen.',
            'estado': 'esperando_foto'
        }

def validar_respuesta(respuesta, tipo):
    """
    Valida la respuesta según el tipo esperado
    """
    if tipo == 'boolean':
        respuesta_lower = respuesta.lower().strip()
        if respuesta_lower in ['sí', 'si', 's', 'yes', 'y']:
            return {'valida': True, 'valor_procesado': True}
        elif respuesta_lower in ['no', 'n']:
            return {'valida': True, 'valor_procesado': False}
        else:
            return {
                'valida': False, 
                'mensaje_error': 'responde con "Sí" o "No"'
            }
    
    elif tipo == 'fecha':
        try:
            fecha_obj = datetime.strptime(respuesta, '%d/%m/%Y')
            return {'valida': True, 'valor_procesado': fecha_obj.date()}
        except ValueError:
            return {
                'valida': False,
                'mensaje_error': 'ingresa la fecha en formato DD/MM/AAAA'
            }
    
    elif tipo == 'hora':
        try:
            hora_obj = datetime.strptime(respuesta, '%H:%M')
            return {'valida': True, 'valor_procesado': hora_obj.time()}
        except ValueError:
            return {
                'valida': False,
                'mensaje_error': 'ingresa la hora en formato HH:MM'
            }
    
    elif tipo == 'texto':
        if len(respuesta.strip()) > 0:
            return {'valida': True, 'valor_procesado': respuesta.strip()}
        else:
            return {
                'valida': False,
                'mensaje_error': 'no puede estar vacío'
            }
    
    elif tipo == 'lista_nombres':
        nombres = [nombre.strip() for nombre in respuesta.split(',')]
        nombres_validos = [n for n in nombres if len(n) > 0]
        if nombres_validos:
            return {'valida': True, 'valor_procesado': nombres_validos}
        else:
            return {
                'valida': False,
                'mensaje_error': 'ingresa al menos un nombre válido'
            }
```

### 4.3 Función `guardar_en_db(datos)`

```python
def guardar_en_db(sesion_id):
    """
    Consolida todos los datos de la sesión y los guarda en la base de datos
    """
    try:
        # Obtener todos los datos de la sesión temporal
        datos_sesion = obtener_datos_sesion_completa(sesion_id)
        
        # Validar que todos los campos requeridos estén presentes
        validacion = validar_datos_completos(datos_sesion)
        if not validacion['completo']:
            return {
                'exito': False,
                'error': f"Faltan datos: {validacion['campos_faltantes']}"
            }
        
        # Preparar datos para inserción
        datos_db = {
            'departamento': datos_sesion['departamento'],
            'fecha': datos_sesion['fecha'],
            'categoria_maxima': datos_sesion['categoria_maxima'],
            'nombre_supervisor': datos_sesion['nombre_supervisor'],
            'nombres_personal': json.dumps(datos_sesion['nombres_personal']),
            'hora_inicio': datos_sesion['hora_inicio'],
            'hora_termino': datos_sesion['hora_termino'],
            
            # Sección Inicio
            'saludo_inicio_jornada': datos_sesion['saludo_inicio_jornada'],
            'enumero_personal': datos_sesion['enumero_personal'],
            'pregunto_estado_salud': datos_sesion['pregunto_estado_salud'],
            'realizo_ejercicios': datos_sesion['realizo_ejercicios'],
            'detecto_anomalias_salud': datos_sesion['detecto_anomalias_salud'],
            'tomo_lista_asistencia': datos_sesion['tomo_lista_asistencia'],
            
            # Sección Información
            'comento_trabajos_mantenimiento': datos_sesion['comento_trabajos_mantenimiento'],
            'comento_trabajos_operacion': datos_sesion['comento_trabajos_operacion'],
            'comento_trabajos_alto_riesgo': datos_sesion['comento_trabajos_alto_riesgo'],
            'comento_incidentes_accidentes': datos_sesion['comento_incidentes_accidentes'],
            'otra_informacion': datos_sesion.get('otra_informacion', ''),
            
            # Sección Actividades de Seguridad
            'realizo_revision_espejo': datos_sesion['realizo_revision_espejo'],
            'realizo_prediccion_peligro': datos_sesion['realizo_prediccion_peligro'],
            'dio_lectura_reglamento': datos_sesion['dio_lectura_reglamento'],
            'realizo_exposicion_sentir_peligro': datos_sesion['realizo_exposicion_sentir_peligro'],
            'actividades_posteriores': datos_sesion['actividades_posteriores'],
            'descripcion_actividades_seguridad': datos_sesion['descripcion_actividades_seguridad'],
            
            # Meta y Observaciones
            'meta_proposito_jornada': datos_sesion['meta_proposito_jornada'],
            'observaciones': datos_sesion.get('observaciones', ''),
            
            # Evidencia
            'ruta_evidencia_fotografica': datos_sesion['ruta_evidencia_fotografica'],
            'usuario_registro': datos_sesion['user_id']
        }
        
        # Insertar en base de datos
        with sqlite3.connect('sirij_bot.db') as conn:
            cursor = conn.cursor()
            
            placeholders = ', '.join(['?' for _ in datos_db])
            columns = ', '.join(datos_db.keys())
            
            query = f"INSERT INTO reuniones_inicio_jornada ({columns}) VALUES ({placeholders})"
            
            cursor.execute(query, list(datos_db.values()))
            reunion_id = cursor.lastrowid
            
            conn.commit()
        
        # Limpiar sesión temporal
        limpiar_sesion_temporal(sesion_id)
        
        return {
            'exito': True,
            'reunion_id': reunion_id,
            'mensaje': f'Reunión registrada exitosamente. ID: {reunion_id}'
        }
        
    except Exception as e:
        return {
            'exito': False,
            'error': f'Error al guardar en base de datos: {str(e)}'
        }
```

### 4.4 Función `manejar_subida_foto(archivo)`

```python
import os
import uuid
from datetime import datetime
from PIL import Image

def manejar_subida_foto(sesion_id, archivo_foto):
    """
    Procesa y guarda la fotografía de evidencia
    """
    try:
        # Generar nombre único para el archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        extension = obtener_extension_archivo(archivo_foto)
        
        nombre_archivo = f"reunion_{sesion_id}_{timestamp}_{unique_id}.{extension}"
        
        # Crear directorio si no existe
        directorio_evidencias = 'evidencias_fotograficas'
        os.makedirs(directorio_evidencias, exist_ok=True)
        
        ruta_completa = os.path.join(directorio_evidencias, nombre_archivo)
        
        # Validar que es una imagen válida
        validacion = validar_imagen(archivo_foto)
        if not validacion['valida']:
            return {
                'exito': False,
                'error': validacion['mensaje_error']
            }
        
        # Redimensionar imagen si es muy grande (opcional)
        imagen_procesada = redimensionar_imagen(archivo_foto, max_width=1920, max_height=1080)
        
        # Guardar archivo
        with open(ruta_completa, 'wb') as f:
            f.write(imagen_procesada)
        
        # Actualizar sesión con la ruta de la foto
        actualizar_sesion_foto(sesion_id, ruta_completa)
        
        return {
            'exito': True,
            'ruta_archivo': ruta_completa,
            'mensaje': 'Fotografía guardada exitosamente'
        }
        
    except Exception as e:
        return {
            'exito': False,
            'error': f'Error al procesar la fotografía: {str(e)}'
        }

def validar_imagen(archivo):
    """
    Valida que el archivo sea una imagen válida
    """
    try:
        # Verificar tamaño del archivo (máximo 10MB)
        if len(archivo) > 10 * 1024 * 1024:
            return {
                'valida': False,
                'mensaje_error': 'La imagen es demasiado grande. Máximo 10MB.'
            }
        
        # Verificar que sea una imagen válida
        imagen = Image.open(io.BytesIO(archivo))
        
        # Verificar formato
        if imagen.format not in ['JPEG', 'PNG', 'JPG']:
            return {
                'valida': False,
                'mensaje_error': 'Formato no soportado. Usa JPEG o PNG.'
            }
        
        return {'valida': True}
        
    except Exception:
        return {
            'valida': False,
            'mensaje_error': 'El archivo no es una imagen válida.'
        }

def redimensionar_imagen(archivo, max_width=1920, max_height=1080):
    """
    Redimensiona la imagen si excede las dimensiones máximas
    """
    imagen = Image.open(io.BytesIO(archivo))
    
    # Calcular nuevas dimensiones manteniendo proporción
    width, height = imagen.size
    
    if width > max_width or height > max_height:
        ratio = min(max_width/width, max_height/height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        imagen = imagen.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Convertir de vuelta a bytes
    output = io.BytesIO()
    imagen.save(output, format='JPEG', quality=85)
    return output.getvalue()
```

---

## 5. STACK TECNOLÓGICO RECOMENDADO

### 5.1 Tecnologías Principales

**Backend:**
- **Python 3.9+** - Lenguaje principal
- **Flask** - Framework web ligero
- **SQLite** - Base de datos (para desarrollo, PostgreSQL para producción)
- **python-telegram-bot** - Para integración con Telegram
- **Pillow (PIL)** - Procesamiento de imágenes

**Librerías Adicionales:**
```
Flask==2.3.3
python-telegram-bot==20.6
Pillow==10.0.1
sqlite3 (incluido en Python)
requests==2.31.0
python-dotenv==1.0.0
```

### 5.2 Estructura de Archivos del Proyecto

```
sirij-bot/
├── app.py                 # Aplicación principal
├── config.py              # Configuraciones
├── requirements.txt       # Dependencias
├── .env                   # Variables de entorno
├── README.md             # Documentación
│
├── bot/
│   ├── __init__.py
│   ├── handlers.py        # Manejadores de mensajes
│   ├── conversation.py    # Lógica de conversación
│   ├── validators.py      # Validadores de respuestas
│   └── utils.py          # Utilidades generales
│
├── database/
│   ├── __init__.py
│   ├── models.py         # Modelos de datos
│   ├── connection.py     # Conexión a BD
│   └── migrations.py     # Scripts de migración
│
├── services/
│   ├── __init__.py
│   ├── photo_service.py  # Manejo de fotografías
│   ├── session_service.py # Manejo de sesiones
│   └── report_service.py  # Generación de reportes
│
├── static/
│   └── evidencias_fotograficas/ # Carpeta para fotos
│
└── tests/
    ├── __init__.py
    ├── test_conversation.py
    ├── test_validators.py
    └── test_database.py
```

### 5.3 Configuración Inicial

**requirements.txt:**
```
Flask==2.3.3
python-telegram-bot==20.6
Pillow==10.0.1
requests==2.31.0
python-dotenv==1.0.0
sqlalchemy==2.0.23
```

**.env:**
```
TELEGRAM_BOT_TOKEN=tu_token_aqui
DATABASE_URL=sqlite:///sirij_bot.db
PHOTO_STORAGE_PATH=./static/evidencias_fotograficas/
MAX_PHOTO_SIZE_MB=10
DEBUG=True
```

### 5.4 Comandos de Instalación

```bash
# Crear entorno virtual
python -m venv sirij-bot-env

# Activar entorno virtual
# En Windows:
sirij-bot-env\Scripts\activate
# En macOS/Linux:
source sirij-bot-env/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
python -c "from database.models import create_tables; create_tables()"

# Ejecutar bot
python app.py
```

---

## 6. CONSIDERACIONES ADICIONALES

### 6.1 Manejo de Errores
- Implementar reintentos automáticos para respuestas inválidas
- Guardar progreso de sesión para recuperación en caso de interrupción
- Logs detallados para debugging

### 6.2 Seguridad
- Validación estricta de tipos de archivo para fotos
- Sanitización de inputs de texto
- Límites de tamaño para archivos y texto

### 6.3 Escalabilidad
- Usar Redis para sesiones en producción
- Implementar cola de trabajos para procesamiento de imágenes
- Considerar PostgreSQL para producción

### 6.4 Funcionalidades Futuras
- Exportación a PDF de reportes
- Dashboard web para visualizar estadísticas
- Notificaciones automáticas
- Integración con sistemas CFE existentes

---

**Documento creado para el desarrollo de SIRIJ BOT**  
**Fecha:** $(date)  
**Versión:** 1.0