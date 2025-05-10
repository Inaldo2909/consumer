# app/Dockerfile

FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor porta do FastAPI WebSocket
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "websocket_server:app", "--host", "0.0.0.0", "--port", "8000"]
