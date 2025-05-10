@echo off
:: -------- ROTACIONA LOGS --------
set LOG_DATE=%DATE:~6,4%-%DATE:~3,2%-%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set LOG_DATE=%LOG_DATE: =0%

if exist websocket.log (
    rename websocket.log websocket_%LOG_DATE%.log
)
if exist consumer.log (
    rename consumer.log consumer_%LOG_DATE%.log
)

:: -------- VERIFICAÇÕES DOCKER --------
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
    echo [ERRO] O Docker não está em execução. Inicie o Docker Desktop e tente novamente.
    pause
    exit /b
)

:: -------- SUBINDO CONTAINERS COM BUILD --------
echo Subindo todos os serviços com build (Kafka, UI, WebSocket, Consumer)...
docker-compose up --build -d

echo Todos os serviços foram iniciados via Docker!
pause
