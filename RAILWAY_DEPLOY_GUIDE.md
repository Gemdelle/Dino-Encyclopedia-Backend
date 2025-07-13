# Guía de Deploy en Railway

## Paso 1: Configuración inicial en Railway

1. **Crear cuenta en Railway**: Ve a [https://railway.app](https://railway.app) y crea una cuenta nueva
2. **Crear nuevo proyecto**: Haz clic en "New Project" → "Deploy from GitHub repo"
3. **Conectar repositorio**: Selecciona tu repositorio del proyecto
4. **Configurar el build**: Railway detectará automáticamente el `Dockerfile` y `railway.json`

## Paso 2: Configurar variables de entorno

En el dashboard de Railway, ve a la sección "Variables" y agrega las siguientes variables:

### Variables obligatorias:
```
PORT=8000
ENVIRONMENT=production
RAILWAY_DOMAIN=https://tu-app-name.railway.app
```

### Firebase (obligatorio para auth):
```
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-client-email@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-client-email%40your-project.iam.gserviceaccount.com
FIREBASE_WEB_API_KEY=your-web-api-key
```

### Supabase (obligatorio para base de datos):
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

### Email (opcional):
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_SENDER=your-email@gmail.com
```

## Paso 3: Configurar Firebase

1. **Crear proyecto Firebase**: Ve a [https://console.firebase.google.com](https://console.firebase.google.com)
2. **Habilitar Authentication**: Ve a Authentication → Sign-in method → Habilitar Email/Password
3. **Generar Service Account**: Ve a Project Settings → Service accounts → Generate new private key
4. **Obtener Web API Key**: Ve a Project Settings → General → Web API Key

## Paso 4: Configurar Supabase

1. **Crear proyecto Supabase**: Ve a [https://supabase.com](https://supabase.com)
2. **Crear tabla profiles**: Ejecuta el siguiente SQL:

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

3. **Obtener credenciales**: Ve a Project Settings → API → URL y anon key

## Paso 5: Deploy

1. **Actualizar RAILWAY_DOMAIN**: Una vez que Railway genere tu dominio, actualiza la variable `RAILWAY_DOMAIN`
2. **Hacer commit**: Haz push de los cambios (railway.json ya está incluido)
3. **Deploy automático**: Railway detectará los cambios y hará el deploy automáticamente

## Paso 6: Verificar el deploy

1. **Acceder a tu API**: `https://tu-app-name.railway.app`
2. **Probar endpoints**: 
   - Health check: `GET /`
   - Docs: `GET /docs`
   - Auth: `POST /api/v1/auth/register`
   - Predict: `POST /api/v1/predict`

## Troubleshooting

### Error de CORS:
- Asegúrate de que `RAILWAY_DOMAIN` está correctamente configurado
- Verifica que el dominio en Railway coincida con el configurado

### Error de Firebase:
- Verifica que todas las variables de Firebase estén correctamente configuradas
- Asegúrate de que el `FIREBASE_PRIVATE_KEY` tenga los saltos de línea `\n` correctos

### Error de Supabase:
- Verifica que la tabla `profiles` exista
- Asegúrate de que las credenciales de Supabase sean correctas

## Archivos configurados:
- ✅ `railway.json` - Configuración de Railway
- ✅ `Dockerfile` - Ya existía
- ✅ `requirements.txt` - Ya existía
- ✅ `runtime.txt` - Ya existía
- ✅ `app/core/config.py` - Actualizado con soporte para Railway
- ✅ `railway-env-variables.txt` - Lista de variables de entorno 