#!/bin/bash

# Script de backup de MinIO para Urukais Klick

# Configuración
BACKUP_DIR="/backups/minio"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/urukais_audio_$TIMESTAMP.tar.gz"
RETENTION_DAYS=7

# Crear directorio de backup si no existe
mkdir -p $BACKUP_DIR

# Ejecutar backup
echo "Iniciando backup de MinIO..."
docker run --rm \
    -v minio_data:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/urukais_audio_$TIMESTAMP.tar.gz -C /data .

if [ $? -eq 0 ]; then
    echo "Backup completado exitosamente: $BACKUP_FILE"
    
    # Eliminar backups antiguos
    find $BACKUP_DIR -name "urukais_audio_*.tar.gz" -mtime +$RETENTION_DAYS -delete
    echo "Backups antiguos eliminados (más de $RETENTION_DAYS días)"
else
    echo "Error al ejecutar backup"
    exit 1
fi
