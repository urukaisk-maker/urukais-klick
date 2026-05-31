# Guía de Despliegue - Urukais Klick

## Requisitos Previos

- Docker Desktop instalado
- Node.js 18+ (para frontend web)
- Flutter SDK 3.0+ (para frontend móvil)
- Git

## 1. Configuración del Entorno

### 1.1 Clonar el Repositorio
```bash
git clone <repositorio>
cd Domingo-noche
```

### 1.2 Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp backend/.env.example backend/.env
cp frontend-web/.env.example frontend-web/.env
```

Editar `backend/.env` con tus configuraciones:
```env
DATABASE_URL=postgresql://urukais:urukais123@localhost:5432/urukais_klick
REDIS_URL=redis://localhost:6379
MEILISEARCH_URL=http://localhost:7700
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=urukais
MINIO_SECRET_KEY=urukais123
MINIO_BUCKET=urukais-audio
SECRET_KEY=<tu-secret-key-seguro>
YOUTUBE_API_KEY=AIzaSyDm7cm8O9VeNUWfJvooXxUdEEcugzonVjU
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

## 2. Despliegue con Docker

### 2.1 Iniciar Servicios de Infraestructura
```bash
docker-compose up -d postgres redis meilisearch minio
```

### 2.2 Ejecutar Migraciones de Base de Datos
```bash
cd backend
alembic upgrade head
```

### 2.3 Iniciar Backend
```bash
# Opción 1: Con Docker
docker-compose up -d backend

# Opción 2: Localmente
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en `http://localhost:8000`

## 3. Despliegue Frontend Web

### 3.1 Instalar Dependencias
```bash
cd frontend-web
npm install
```

### 3.2 Iniciar Desarrollo
```bash
npm run dev
```

El frontend web estará disponible en `http://localhost:3000`

### 3.3 Build para Producción
```bash
npm run build
npm start
```

## 4. Despliegue Frontend Móvil

### 4.1 Instalar Dependencias
```bash
cd frontend-mobile
flutter pub get
```

### 4.2 Mover Archivos Temporales (si es necesario)
Si los archivos están en `temp-mobile-screens/` y `temp-mobile-widgets/`:
```powershell
# Crear directorios
New-Item -ItemType Directory -Path "lib/screens" -Force
New-Item -ItemType Directory -Path "lib/widgets" -Force

# Mover archivos
Copy-Item "../temp-mobile-screens/*.dart" "lib/screens/"
Copy-Item "../temp-mobile-widgets/*.dart" "lib/widgets/"
Copy-Item "../temp-mobile-main/main.dart" "lib/main.dart"
```

### 4.3 Ejecutar en Emulador
```bash
flutter run
```

### 4.4 Build para Producción
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release
```

## 5. Configuración de MinIO

### 5.1 Acceder a Consola MinIO
- URL: `http://localhost:9001`
- Usuario: `urukais`
- Contraseña: `urukais123`

### 5.2 Crear Bucket
1. Iniciar sesión en la consola
2. Crear bucket llamado `urukais-audio`
3. Configurar política de acceso público para lectura

## 6. Configuración de Meilisearch

### 6.1 Acceder a Meilisearch
- URL: `http://localhost:7700`

### 6.2 Configurar Índices
Los índices se crean automáticamente al iniciar el backend.

## 7. Verificación del Despliegue

### 7.1 Verificar Backend
```bash
curl http://localhost:8000/
```

Respuesta esperada:
```json
{
  "message": "Bienvenido a Urukais Klick API",
  "version": "1.0.0",
  "status": "operativo"
}
```

### 7.2 Verificar Documentación API
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 7.3 Verificar Frontend Web
- Abrir `http://localhost:3000` en el navegador

## 8. Comandos Útiles

### 8.1 Detener Todos los Servicios
```bash
docker-compose down
```

### 8.2 Ver Logs de Servicios
```bash
docker-compose logs -f backend
docker-compose logs -f postgres
```

### 8.3 Reiniciar Servicios
```bash
docker-compose restart backend
```

### 8.4 Limpiar Volúmenes Docker
```bash
docker-compose down -v
```

## 9. Solución de Problemas

### 9.1 Error de Conexión a Base de Datos
- Verificar que PostgreSQL esté corriendo: `docker-compose ps postgres`
- Verificar credenciales en `.env`

### 9.2 Error de Conexión a MinIO
- Verificar que MinIO esté corriendo: `docker-compose ps minio`
- Verificar que el bucket exista

### 9.3 Error de Migraciones
- Eliminar base de datos y volver a crear:
```bash
docker-compose exec postgres psql -U urukais -d urukais_klick -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
alembic upgrade head
```

### 9.4 Error de Build Flutter
- Limpiar caché: `flutter clean`
- Obtener dependencias: `flutter pub get`
- Verificar versión de Flutter: `flutter --version`

## 10. Despliegue en Producción

### 10.1 Variables de Entorno Producción
Crear `.env.production` con valores reales:
```env
DATABASE_URL=postgresql://usuario:password@host-produccion:5432/urukais_klick
REDIS_URL=redis://host-produccion:6379
SECRET_KEY=<secret-key-muy-seguro>
# ... otras variables
```

### 10.2 Configurar Dominio y SSL
- Configurar dominio en servidor
- Instalar certificado SSL (Let's Encrypt recomendado)
- Configurar Nginx como reverse proxy

### 10.3 Configurar Backup
- Configurar backup automático de PostgreSQL
- Configurar backup de MinIO
- Configurar backup de Redis

### 10.4 Monitoreo
- Configurar logging centralizado
- Configurar métricas (Prometheus + Grafana)
- Configurar alertas

## 11. Arquitectura del Sistema

```
┌─────────────────┐
│  Frontend Web   │ (Next.js - Port 3000)
│  Frontend Móvil │ (Flutter)
└────────┬────────┘
         │ HTTP/REST
┌────────▼────────┐
│  Backend API    │ (FastAPI - Port 8000)
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼────┐ ┌──▼──────┐ ┌─▼──────┐
│PostgreSQL│ Redis │Meilisearch│ MinIO │
└───────┘ └───────┘ └──────────┘ └───────┘
```

## 12. Soporte

Para problemas o preguntas:
- Revisar logs: `docker-compose logs`
- Verificar documentación API: `http://localhost:8000/docs`
- Revisar issues del repositorio
