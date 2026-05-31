# Script para ejecutar migraciones de Alembic en PowerShell

Set-Location backend

# Esperar a que la base de datos esté disponible
Write-Host "Esperando a que PostgreSQL esté disponible..."
$timeout = 60
$elapsed = 0
while ($elapsed -lt $timeout) {
    try {
        $connection = Test-NetConnection -ComputerName postgres -Port 5432 -ErrorAction SilentlyContinue
        if ($connection.TcpTestSucceeded) {
            Write-Host "PostgreSQL está disponible"
            break
        }
    } catch {
        # Continuar esperando
    }
    Start-Sleep -Seconds 1
    $elapsed++
}

if ($elapsed -ge $timeout) {
    Write-Host "Timeout esperando a PostgreSQL"
    exit 1
}

# Ejecutar migraciones
Write-Host "Ejecutando migraciones..."
alembic upgrade head

Write-Host "Migraciones completadas"
