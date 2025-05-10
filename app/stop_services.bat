@echo off
echo Verificando se o Docker está instalado...

where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Docker não está instalado ou não está no PATH.
    pause
    exit /b
)

echo Verificando se o Docker está rodando...
docker info >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] O Docker não está em execução.
    pause
    exit /b
)

echo Parando containers e limpando logs...
docker-compose down

:: Limpa logs gerados
del logs\websocket.log >nul 2>nul
del logs\consumer.log >nul 2>nul

echo Serviços encerrados e logs limpos.
pause
