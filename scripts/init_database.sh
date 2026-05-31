#!/bin/bash

# Script de inicialización de base de datos para Urukais Klick

echo "=== Inicialización de Base de Datos Urukais Klick ==="

# Copiar archivo de entorno si no existe
if [ ! -f backend/.env ]; then
    echo "Copiando .env.example a .env..."
    cp backend/.env.example backend/.env
    echo "Archivo .env creado"
else
    echo "Archivo .env ya existe"
fi

# Iniciar servicios de infraestructura
echo "Iniciando servicios de infraestructura..."
docker-compose up -d postgres redis meilisearch minio

# Esperar a que PostgreSQL esté disponible
echo "Esperando a que PostgreSQL esté disponible..."
timeout=60
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if docker-compose exec -T postgres pg_isready -U urukais > /dev/null 2>&1; then
        echo "PostgreSQL está disponible"
        break
    fi
    sleep 1
    elapsed=$((elapsed + 1))
done

if [ $elapsed -ge $timeout ]; then
    echo "ERROR: Timeout esperando a PostgreSQL"
    exit 1
fi

# Ejecutar migraciones
echo "Ejecutando migraciones de Alembic..."
cd backend
alembic upgrade head
cd ..

if [ $? -eq 0 ]; then
    echo "✅ Migraciones ejecutadas exitosamente"
else
    echo "❌ Error al ejecutar migraciones"
    exit 1
fi

echo "=== Inicialización completada ==="
