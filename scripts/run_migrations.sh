#!/bin/bash

# Script para ejecutar migraciones de Alembic

cd backend

# Esperar a que la base de datos esté disponible
echo "Esperando a que PostgreSQL esté disponible..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL está disponible"

# Ejecutar migraciones
echo "Ejecutando migraciones..."
alembic upgrade head

echo "Migraciones completadas"
