# Script de backup de PostgreSQL para Urukais Klick (PowerShell)

# Configuración
$BACKUP_DIR = "C:\backups\postgres"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_FILE = "$BACKUP_DIR\urukais_klick_$TIMESTAMP.sql"
$RETENTION_DAYS = 7

# Crear directorio de backup si no existe
if (-not (Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force
}

# Ejecutar backup
Write-Host "Iniciando backup de PostgreSQL..."
docker-compose exec -T postgres pg_dump -U urukais urukais_klick | Out-File -FilePath $BACKUP_FILE -Encoding utf8

if ($LASTEXITCODE -eq 0) {
    Write-Host "Backup completado exitosamente: $BACKUP_FILE"
    
    # Comprimir backup
    Compress-Archive -Path $BACKUP_FILE -DestinationPath "$BACKUP_FILE.gz" -Force
    Remove-Item $BACKUP_FILE
    Write-Host "Backup comprimido: ${BACKUP_FILE}.gz"
    
    # Eliminar backups antiguos
    Get-ChildItem $BACKUP_DIR -Filter "urukais_klick_*.sql.gz" | Where-Object {
        $_.LastWriteTime -lt (Get-Date).AddDays(-$RETENTION_DAYS)
    } | Remove-Item
    Write-Host "Backups antiguos eliminados (más de $RETENTION_DAYS días)"
} else {
    Write-Host "Error al ejecutar backup"
    exit 1
}
