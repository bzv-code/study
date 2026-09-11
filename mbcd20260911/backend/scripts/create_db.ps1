<#
Создаёт базу данных проекта в уже работающем контейнере Postgres и накатывает schema.sql.

Использование (PowerShell):
    .\create_db.ps1
    .\create_db.ps1 -ContainerName my_postgres_container -DbUser postgres

Имя своего контейнера можно посмотреть командой: docker ps
#>
param(
    [string]$ContainerName = "postgres",
    [string]$DbUser = "postgres"
)

$ErrorActionPreference = "Stop"
$DbName = "673105613811_dom_cvetov"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Контейнер: $ContainerName | Пользователь: $DbUser | База: $DbName"

$exists = (docker exec -i $ContainerName psql -U $DbUser -tAc "SELECT 1 FROM pg_database WHERE datname='$DbName'").Trim()

if ($exists -eq "1") {
    Write-Host "База $DbName уже существует — пропускаю создание."
} else {
    Write-Host "Создаю базу $DbName..."
    docker exec -i $ContainerName psql -U $DbUser -c "CREATE DATABASE `"$DbName`";"
}

Write-Host "Накатываю schema.sql..."
Get-Content "$ScriptDir\schema.sql" -Raw | docker exec -i $ContainerName psql -U $DbUser -d $DbName

Write-Host "Готово. Проверка таблиц:"
docker exec -i $ContainerName psql -U $DbUser -d $DbName -c "\dt"
