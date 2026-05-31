# Urukais Klick

Aplicación musical gratuita de descubrimiento social y conexión artística.

## Descripción

Urukais Klick es una plataforma completamente gratuita, sin pagos, sin suscripciones y sin publicidad. Su misión es facilitar el descubrimiento musical auténtico y la conexión humana entre oyentes y artistas emergentes.

## Estructura del Proyecto

```
urukais-klick/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/        # Endpoints
│   │   ├── core/       # Configuración y base de datos
│   │   ├── models/     # Modelos SQLAlchemy
│   │   ├── schemas/    # Esquemas Pydantic
│   │   └── services/   # Lógica de negocio
│   ├── tests/
│   └── requirements.txt
├── frontend-web/        # Aplicación web Next.js
│   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── styles/
│   └── package.json
├── frontend-mobile/     # Aplicación móvil Flutter
│   ├── lib/
│   │   ├── screens/
│   │   ├── services/
│   │   └── models/
│   └── pubspec.yaml
├── infrastructure/      # Configuración de servicios
│   ├── postgres/
│   ├── redis/
│   ├── meilisearch/
│   └── minio/
├── docs/               # Documentación
└── scripts/            # Scripts de utilidad
```

## Tecnologías

### Backend
- **FastAPI**: Framework web moderno y rápido
- **PostgreSQL**: Base de datos relacional
- **Redis**: Caché y sesiones
- **Meilisearch**: Motor de búsqueda
- **MinIO**: Almacenamiento S3-compatible

### Frontend Web
- **Next.js 14**: Framework React con SSR
- **TypeScript**: Tipado estático
- **TailwindCSS**: Estilos utility-first
- **Axios**: Cliente HTTP

### Frontend Móvil
- **Flutter**: Framework multiplataforma
- **Dart**: Lenguaje de programación

## Instalación

### Requisitos previos
- Docker y Docker Compose
- Python 3.11+ (para desarrollo local)
- Node.js 18+ (para desarrollo local)
- Flutter SDK (para desarrollo móvil)

### Iniciar con Docker

```bash
# Clonar el repositorio
<<<<<<< HEAD
git clone https://github.com/urukaisk-maker/urukais-klick.git
=======
git clone https://github.com/manuelcasimiro/urukais-klick.git
>>>>>>> 02bc4905106ef54a444d5f4eb3260795019742f4
cd urukais-klick

# Iniciar todos los servicios
docker-compose up -d

# Verificar estado
docker-compose ps
```

### Desarrollo local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

#### Frontend Web
```bash
cd frontend-web
npm install
npm run dev
```

#### Frontend Móvil
```bash
cd frontend-mobile
flutter pub get
flutter run
```

## API Endpoints

### Usuarios
- `POST /api/v1/users/` - Crear usuario
- `GET /api/v1/users/` - Listar usuarios
- `GET /api/v1/users/{id}` - Obtener usuario

### Pistas
- `POST /api/v1/tracks/` - Crear pista
- `GET /api/v1/tracks/` - Listar pistas
- `GET /api/v1/tracks/{id}` - Obtener pista
- `POST /api/v1/tracks/{id}/klick` - Enviar Klick de apoyo

## Documentación

La documentación de la API está disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contribución

Este proyecto es de código abierto y bienvenimos contribuciones. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Este proyecto es software libre y está disponible bajo licencia MIT.

## Contacto

- **Desarrollador**: Manuel Casimiro Carrasco
- **Fecha**: 31 de mayo de 2026
- **Email**: urukaisk@gmail.com

## Filosofía

Urukais Klick se mantiene como un bien común digital, financiado con recursos propios, colaboraciones voluntarias y donaciones opcionales. Nunca se cobrará a usuarios ni artistas por utilizar la plataforma.
