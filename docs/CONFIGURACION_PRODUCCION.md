# Configuración de Producción - Urukais Klick

## 1. Variables de Entorno Producción

### Backend (.env.production)
Crear archivo `backend/.env.production`:
```env
# Configuración de base de datos - PRODUCCIÓN
DATABASE_URL=postgresql://usuario:password_seguro@host-produccion:5432/urukais_klick

# Redis - PRODUCCIÓN
REDIS_URL=redis://host-produccion:6379

# Meilisearch - PRODUCCIÓN
MEILISEARCH_URL=http://host-produccion:7700
MEILISEARCH_API_KEY=tu-api-key-meilisearch

# MinIO (S3-compatible) - PRODUCCIÓN
MINIO_ENDPOINT=host-produccion:9000
MINIO_ACCESS_KEY=tu-access-key-seguro
MINIO_SECRET_KEY=tu-secret-key-muy-seguro
MINIO_BUCKET=urukais-audio

# Seguridad - PRODUCCIÓN
SECRET_KEY=GENERAR_UN_SECRET_KEY_SEGuro_AQUI

# YouTube API
YOUTUBE_API_KEY=AIzaSyDm7cm8O9VeNUWfJvooXxUdEEcugzonVjU

# CORS - PRODUCCIÓN
ALLOWED_ORIGINS=["https://tu-dominio.com", "https://app.tu-dominio.com"]

# Configuración adicional
DEBUG=False
ENVIRONMENT=production
```

### Frontend Web (.env.production)
Crear archivo `frontend-web/.env.production`:
```env
NEXT_PUBLIC_API_URL=https://api.tu-dominio.com
NEXT_PUBLIC_APP_URL=https://tu-dominio.com
```

## 2. Sistema de Backup

### Script de Backup PostgreSQL (backup_postgres.sh)
```bash
#!/bin/bash
BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/urukais_klick_$TIMESTAMP.sql"
RETENTION_DAYS=7

mkdir -p $BACKUP_DIR
docker-compose exec -T postgres pg_dump -U urukais urukais_klick > $BACKUP_FILE

if [ $? -eq 0 ]; then
    gzip $BACKUP_FILE
    find $BACKUP_DIR -name "urukais_klick_*.sql.gz" -mtime +$RETENTION_DAYS -delete
fi
```

### Script de Backup PostgreSQL (backup_postgres.ps1)
```powershell
$BACKUP_DIR = "C:\backups\postgres"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_FILE = "$BACKUP_DIR\urukais_klick_$TIMESTAMP.sql"
$RETENTION_DAYS = 7

if (-not (Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force
}

docker-compose exec -T postgres pg_dump -U urukais urukais_klick | Out-File -FilePath $BACKUP_FILE -Encoding utf8

if ($LASTEXITCODE -eq 0) {
    Compress-Archive -Path $BACKUP_FILE -DestinationPath "$BACKUP_FILE.gz" -Force
    Remove-Item $BACKUP_FILE
    Get-ChildItem $BACKUP_DIR -Filter "urukais_klick_*.sql.gz" | Where-Object {
        $_.LastWriteTime -lt (Get-Date).AddDays(-$RETENTION_DAYS)
    } | Remove-Item
}
```

### Script de Backup MinIO (backup_minio.sh)
```bash
#!/bin/bash
BACKUP_DIR="/backups/minio"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p $BACKUP_DIR
docker run --rm -v minio_data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/urukais_audio_$TIMESTAMP.tar.gz -C /data .
find $BACKUP_DIR -name "urukais_audio_*.tar.gz" -mtime +7 -delete
```

### Configuración Cron Jobs (setup_cron.sh)
```bash
#!/bin/bash
(crontab -l 2>/dev/null; echo "0 2 * * * /path/to/scripts/backup_postgres.sh") | crontab -
(crontab -l 2>/dev/null; echo "0 3 * * 0 /path/to/scripts/backup_minio.sh") | crontab -
```

## 3. Monitoreo y Logs

### Configuración de Logging (backend/app/core/logging.py)
```python
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10485760, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
```

### Configuración Prometheus (docker-compose.yml)
Agregar al docker-compose.yml:
```yaml
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./infrastructure/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - urukais-network
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    networks:
      - urukais-network
```

## 4. Tests

### Test de Autenticación (backend/app/tests/test_auth.py)
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "test123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
```

### Ejecutar Tests
```bash
cd backend
pytest
```

## 5. CI/CD Pipeline

### GitHub Actions (.github/workflows/ci.yml)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install pytest pytest-asyncio
    - name: Run tests
      run: |
        cd backend
        pytest

  test-frontend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: |
        cd frontend-web
        npm install
    - name: Run tests
      run: |
        cd frontend-web
        npm test

  deploy:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
```

## 6. Optimización Docker

### Dockerfile Multi-stage Backend
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app ./app
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile Multi-stage Frontend Web
```dockerfile
# Build stage
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY package*.json ./
RUN npm ci --only=production
CMD ["npm", "start"]
```

## 7. Configuración CDN

### Cloudflare R2 (Alternativa a MinIO)
```python
# backend/app/services/storage.py
import boto3

class R2StorageService:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url='https://<account-id>.r2.cloudflarestorage.com',
            aws_access_key_id='<access-key>',
            aws_secret_access_key='<secret-key>',
            region_name='auto'
        )
    
    def upload_file(self, file_path, object_name):
        self.client.upload_file(
            'urukais-audio',
            object_name,
            file_path
        )
```

## 8. SSL/HTTPS con Nginx

### Configuración Nginx (nginx.conf)
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com;

    ssl_certificate /etc/ssl/certs/fullchain.pem;
    ssl_certificate_key /etc/ssl/private/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Generar Certificado SSL (Let's Encrypt)
```bash
sudo certbot --nginx -d tu-dominio.com
```

## 9. Resumen de Tareas

Para completar la configuración de producción:

1. ✅ Variables de entorno configuradas (documentadas)
2. ✅ Scripts de backup creados (documentados)
3. ✅ Monitoreo configurado (documentado)
4. ✅ Tests creados (documentados)
5. ✅ CI/CD pipeline configurado (documentado)
6. ✅ Optimización Docker (documentada)
7. ✅ CDN configurado (documentado)
8. ✅ SSL/HTTPS configurado (documentado)

**Para aplicar estos cambios:**
- Copiar los archivos de configuración a sus ubicaciones correspondientes
- Ejecutar los scripts de setup
- Configurar los servicios externos (Cloudflare R2, Let's Encrypt)
- Desplegar en servidor de producción
