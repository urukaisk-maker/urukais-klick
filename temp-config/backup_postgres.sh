#!/bin/bash

# Script de backup de PostgreSQL para Urukais Klick

# Configuración
BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/urukais_klick_$TIMESTAMP.sql"
RETENTION_DAYS=7

# Crear directorio de backup si no existe
mkdir -p $BACKUP_DIR

# Ejecutar backup
echo "Iniciando backup de PostgreSQL..."
docker-compose exec -T postgres pg_dump -U urukais urukais_klick > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "Backup completado exitosamente: $BACKUP_FILE"
    
    # Comprimir backup
    gzip $BACKUP_FILE
    echo "Backup comprimido: ${BACKUP_FILE}.gz"
    
    # Eliminar backups antiguos
    find $BACKUP_DIR -name "urukais_klick_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    echo "Backups antiguos eliminados (más de $RETENTION_DAYS días)"
else
    echo "Error al ejecutar backup"
    exit 1
fi
