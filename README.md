# API de Automatización de Procesos

Esta API está construida con **FastAPI** y está diseñada para la automatización de procesos, transformación de datos (ETL) utilizando **Polars**, y gestión eficiente de conexiones a bases de datos mediante **SQLAlchemy**.

## 📋 Características

- **FastAPI**: Alto rendimiento y validación de datos.
- **Polars**: Transformación de datos rápida y eficiente (ver `BaseTransformer`).
- **DB Manager**: Gestión de conexiones a múltiples bases de datos con pool de conexiones y manejo de sesiones seguro.
- **Entornos**: Configuración separada para `development` y `production`.
- **Seguridad**: Middleware de CORS y TrustedHost configurables.

## 🚀 Requisitos

- Python 3.9+
- Pip

## 🛠️ Instalación

1.  **Clonar el repositorio:**

    ```bash
    git clone <url-del-repositorio>
    cd automation-api
    ```

2.  **Crear un entorno virtual:**

    ```bash
    python -m venv venv

    # En Windows
    venv\Scripts\activate

    # En Linux/Mac
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuración

El proyecto utiliza variables de entorno para su configuración. Crea un archivo `.env` en la raíz del proyecto.

**Variables obligatorias:**

```ini
# Entorno de la aplicación (DEV | QA | PROD)
APP_ENV="DEV"
```

> **Nota:** La aplicación validará que `APP_ENV` sea correcto al iniciar. Si falta, la aplicación se detendrá.

## ▶️ Ejecución

### Entorno de Desarrollo

En desarrollo, la documentación interactiva (Swagger UI) está habilitada y el servidor se reinicia ante cambios en el código.

```bash
# Asegúrate de que APP_ENV=development en tu .env
fastapi dev app/main.py
```

- **Documentación:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

### Requerimientos Técnicos y Despliegue (QA / Producción)

La aplicación está diseñada para ser desplegada mediante entrega de artefactos (contenedores Docker), asegurando consistencia entre ambientes.

- **Sistema Operativo:** Linux (mediante el runtime de Docker). A nivel de desarrollo y virtual env es multiplataforma.
- **Versión de Python:** El código fuente es compatible con Python 3.9+, pero el artefacto de despliegue (`Dockerfile`) utiliza **Python 3.14** para optimizar el rendimiento y la seguridad.
- **Almacenamiento y Datos:** La API no requiere almacenamiento local en disco. Todo el volumen de datos crece y se gestiona directamente en la base de datos relacional.
- **Red y DNS:** El registro DNS o IP se gestiona externamente, mientras que el control de acceso de la API está parametrizado por las variables de entorno `CORS_ORIGINS` y `ALLOWED_HOST`. Puede ser despliegue interno o externo según necesidad.

1.  **Configurar entorno:**
    Cambia en tu archivo `.env` el entorno correspondiente:

    ```ini
    APP_ENV="QA" # o "PROD"
    ```

2.  **Ejecutar mediante contenedores Docker (Opción Recomendada):**
    El proyecto cuenta con un `Dockerfile` y un `compose.yml` listos para levantar la aplicación productiva.
    
    ```bash
    docker compose up -d --build
    ```

3.  **Ejecutar con FastAPI CLI (Opción alternativa sin Docker):**

    ```bash
    fastapi run app/app.py --port 8000
    ```
    
    > **Nota:** La aplicación ocultará automáticamente los endpoints de documentación interactiva (`/docs`) por seguridad si `APP_ENV` es "QA" o "PROD".

## 📂 Estructura del Proyecto

```
automation-api/
├── app
│   ├── api
│   │   ├── v1
│   │   │   ├── __init__.py
│   │   │   └── api.py
│   │   └── __init__.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   ├── handlers.py
│   │   ├── logger.py
│   │   ├── security.py
│   │   └── settings.py
│   ├── modules
│   │   ├── ep
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   └── transform.py
│   │   ├── erc
│   │   │   ├── transformers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── bienes_transform.py
│   │   │   │   ├── inversion_transform.py
│   │   │   │   ├── paises_transform.py
│   │   │   │   ├── servicios_transform.py
│   │   │   │   └── turismo_transform.py
│   │   │   ├── router.py
│   │   │   └── service.py
│   │   ├── health
│   │   │   └── router.py
│   │   └── __init__.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── base_transformer.py
│   │   ├── loader_file.py
│   │   ├── schema.py
│   │   └── uploader.py
│   ├── __init__.py
│   └── app.py
├── .env.template
├── .gitignore
├── Dockerfile
├── README.md
├── compose.yml
└── requirements.txt
```

## 🔧 Utilidades

### BaseTransformer

El sistema incluye una clase `BaseTransformer` en `app/utils/base_transformer.py` para estandarizar la limpieza y transformación de DataFrames de Polars.

- **\_clean**: Normaliza nombres de columnas (snake_case).
- **\_map_columns**: Renombra columnas según un diccionario de mapeo.
- **\_validate_required_columns**: Asegura la integridad de los datos antes de procesar.
