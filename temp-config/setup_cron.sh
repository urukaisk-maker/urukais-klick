#!/bin/bash

# Script para configurar cron jobs de backup automático

# Configurar backup diario de PostgreSQL a las 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * /path/to/Domingo-noche/scripts/backup_postgres.sh") | crontab -

# Configurar backup semanal de MinIO los domingos a las 3 AM
(crontab -l 2>/dev/null; echo "0 3 * * 0 /path/to/Domingo-noche/scripts/backup_minio.sh") | crontab -

echo "Cron jobs configurados:"
crontab -l
