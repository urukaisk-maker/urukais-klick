# Script de inicialización de base de datos para Urukais Klick (PowerShell)

Write-Host "=== Inicialización de Base de Datos Urukais Klick ===" -ForegroundColor Cyan

# Copiar archivo de entorno si no existe
if (-not (Test-Path "backend\.env")) {
    Write-Host "Copiando .env.example a .env..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "Archivo .env creado" -ForegroundColor Green
} else {
    Write-Host "Archivo .env ya existe" -ForegroundColor Green
}

# Iniciar servicios de infraestructura
Write-Host "Iniciando servicios de infraestructura..." -ForegroundColor Yellow
docker-compose up -d postgres redis meilisearch minio

# Esperar a que PostgreSQL esté disponible
Write-Host "Esperando a que PostgreSQL esté disponible..." -ForegroundColor Yellow
$timeout = 60
$elapsed = 0
while ($elapsed -lt $timeout) {
    try {
        $result = docker-compose exec -T postgres pg_isready -U urukais 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "PostgreSQL está disponible" -ForegroundColor Green
            break
        }
    } catch {
        # Continuar esperando
    }
    Start-Sleep -Seconds 1
    $elapsed++
}

if ($elapsed -ge $timeout) {
    Write-Host "ERROR: Timeout esperando a PostgreSQL" -ForegroundColor Red
    exit 1
}

# Ejecutar migraciones
Write-Host "Ejecutando migraciones de Alembic..." -ForegroundColor Yellow
Push-Location backend
try {
    alembic upgrade head
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Migraciones ejecutadas exitosamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al ejecutar migraciones" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}

Write-Host "=== Inicialización completada ===" -ForegroundColor Cyan
