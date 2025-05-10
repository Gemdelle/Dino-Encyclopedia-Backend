# Dino Encyclopedia Backend

Backend para la aplicación Dino Encyclopedia, que proporciona autenticación de usuarios y clasificación de imágenes de dinosaurios.

## Estructura del Proyecto

```
dino-encyclopedia-backend/
├── app/
│   ├── __init__.py           # Inicialización de la aplicación
│   ├── api/                  # Rutas de la API
│   │   └── v1/
│   │       ├── api.py        # Configuración de rutas v1
│   │       └── endpoints/
│   │           ├── auth.py   # Endpoints de autenticación
│   │           └── predict.py # Endpoints de predicción
│   ├── core/                 # Configuración central
│   │   ├── config.py        # Configuración general
│   │   ├── firebase.py      # Configuración de Firebase
│   │   └── supabase.py      # Configuración de Supabase
│   ├── models/              # Modelos de datos
│   │   └── user.py         # Modelos de usuario
│   └── ml/                  # Código de Machine Learning
│       ├── data/           # Datos para ML
│       │   ├── dataset/    # Dataset de entrenamiento
│       │   ├── models/     # Modelos entrenados
│       │   └── temp/       # Archivos temporales
│       ├── predict.py      # Código de predicción
│       └── train.py        # Código de entrenamiento
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias
└── env.example            # Ejemplo de variables de entorno
```

## Configuración

1. Crea un archivo `.env` basado en `env.example` y configura:
   - Credenciales de Firebase
   - Credenciales de Supabase

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Endpoints de la API

### Autenticación y Usuarios

- `POST /api/v1/auth/register`: Registro de usuarios
- `POST /api/v1/auth/login`: Inicio de sesión
- `POST /api/v1/auth/reset-password`: Recuperación de contraseña
- `GET /api/v1/auth/profile/{user_id}`: Obtener perfil
- `PUT /api/v1/auth/profile/{user_id}`: Actualizar perfil
- `DELETE /api/v1/auth/profile/{user_id}`: Eliminar usuario

### Machine Learning

- `POST /api/v1/predict`: Predicción de dinosaurios
  - Recibe una imagen como `multipart/form-data`
  - Retorna la especie de dinosaurio predicha

## Desarrollo

Para ejecutar el servidor en modo desarrollo:

```bash
python main.py
```

## Base de Datos

### Tabla de Perfiles (Supabase)

```sql
create table public.profiles (
  id uuid not null default gen_random_uuid(),
  full_name text null,
  created_at timestamp with time zone null default now(),
  email text null,
  images_uploaded_count integer null default 0,
  has_entries boolean null default false,
  profile_picture text null default 'no_profile'::text,
  constraint profiles_pk primary key (id),
  constraint unique_email unique (email)
);
``` 
