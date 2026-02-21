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
# Entorno de la aplicación (development | production)
APP_ENV=development

# Configuración de Base de Datos (Ejemplos, depende de core/config.py)
DB_CONNECTION_STRING=mssql+pyodbc://user:pass@host/db
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

### Entorno de Producción (Despliegue)

Para producción, se recomienda usar múltiples workers y deshabilitar el modo debug. La aplicación ocultará automáticamente los endpoints de documentación (`/docs`) por seguridad si `APP_ENV=production`.

1.  **Configurar entorno:**
    Cambia en tu archivo `.env`:

    ```ini
    APP_ENV=production
    ```

2.  **Ejecutar con FastAPI CLI (Producción):**

    ```bash
    fastapi run app/main.py
    ```

## 📂 Estructura del Proyecto

```text
automation-api/
├── app/
│   ├── api/
│   │   └── v1/             # Rutas y endpoints de la API
│   ├── core/
│   │   ├── config.py       # Clases de configuración (Dev/Prod)
│   │   ├── db_manager.py   # Gestor de conexiones SQLAlchemy (Singleton pattern)
│   │   └── logger.py       # Configuración de logs
│   ├── utils/
│   │   └── base_transformer.py # Clase base abstracta para ETL con Polars
│   └── main.py             # Punto de entrada (Entry point)
├── .env                    # Variables de entorno (no commitear)
├── .gitignore
└── requirements.txt
```

## 🔧 Utilidades

### BaseTransformer

El sistema incluye una clase `BaseTransformer` en `app/utils/base_transformer.py` para estandarizar la limpieza y transformación de DataFrames de Polars.

- **\_clean**: Normaliza nombres de columnas (snake_case).
- **\_map_columns**: Renombra columnas según un diccionario de mapeo.
- **\_validate_required_columns**: Asegura la integridad de los datos antes de procesar.
