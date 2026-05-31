# Script de backup de MinIO para Urukais Klick (PowerShell)

# Configuración
$BACKUP_DIR = "C:\backups\minio"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_FILE = "$BACKUP_DIR\urukais_audio_$TIMESTAMP.tar.gz"
$RETENTION_DAYS = 7

# Crear directorio de backup si no existe
if (-not (Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force
}

# Ejecutar backup
Write-Host "Iniciando backup de MinIO..."
docker run --rm `
    -v minio_data:/data `
    -v ${BACKUP_DIR}:/backup `
    alpine tar czf /backup/urukais_audio_${TIMESTAMP}.tar.gz -C /data .

if ($LASTEXITCODE -eq 0) {
    Write-Host "Backup completado exitosamente: $BACKUP_FILE"
    
    # Eliminar backups antiguos
    Get-ChildItem $BACKUP_DIR -Filter "urukais_audio_*.tar.gz" | Where-Object {
        $_.LastWriteTime -lt (Get-Date).AddDays(-$RETENTION_DAYS)
    } | Remove-Item
    Write-Host "Backups antiguos eliminados (más de $RETENTION_DAYS días)"
} else {
    Write-Host "Error al ejecutar backup"
    exit 1
}
